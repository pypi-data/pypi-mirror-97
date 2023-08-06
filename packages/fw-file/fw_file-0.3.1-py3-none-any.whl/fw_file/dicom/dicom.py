"""DICOM file class and related utilities."""
import re
import typing as t

from fw_meta import MetaExtractor
from pydicom.datadict import dictionary_VR, keyword_dict, private_dictionaries
from pydicom.dataelem import DataElement
from pydicom.dataset import Dataset
from pydicom.filereader import read_partial
from pydicom.multival import MultiValue
from pydicom.sequence import Sequence
from pydicom.tag import BaseTag, Tag, TagType
from pydicom.uid import UID
from pydicom.valuerep import DA, DT, IS, TM, DSdecimal, DSfloat, PersonName

from ..collection import FileCollection
from ..common import AttrMixin, get_filepath, open_any
from ..file import AnyIO, File
from . import dcmdict, utils
from .config import CONFIG
from .fixer import Tracker, raw_elem_tracker

__all__ = ["DICOM"]

# extend TagType with (str, str)
TagType = t.Union[TagType, t.Tuple[str, str]]

# stop_when callback signature
StopWhen = t.Callable[[BaseTag, str, int], bool]

# preload custom/extended private definitions
dcmdict.load_private_dictionaries()


class DICOM(File):  # pylint: disable=too-many-ancestors
    """DICOM data-file."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        file: AnyIO,
        extractor: t.Optional[MetaExtractor] = None,
        force: bool = False,
        defer_size: t.Union[None, int, str] = 512,
        specific_tags: t.Optional[t.List[TagType]] = None,
        stop_when: t.Union[None, TagType, StopWhen] = None,
        decode: bool = False,
        track: bool = False,
    ) -> None:
        """DICOM data-file reading and parsing a file as a DICOM dataset.

        Args:
            file (str|Path|file): The file to read from as a string (filepath),
                Path or file-like object. Files opened from str and Path objects
                are automatically closed after reading. The caller is responsible
                for closing file-like objects.
            extractor (MetaExtractor, optional): MetaExtractor instance to
                customize metadata extraction with if given. Default: None.
            force (bool, optional): Flag to force reading the file as DICOM
                even if the header is missing or invalid. Defaults to False.
            defer_size (int|str, optional): Defer reading dataelements into
                memory on access if their value is larger than `defer_size`.
                Defaults to 512B.
            specific_tags: (list[tag], optional): List of tags to include if set
                when parsing while skipping all others. Defaults to None.
            stop_when (tag|callable, optional): Tag or callback function to be
                used as a stop condition when reading. Defaults to None.
            decode (bool, optional): Flag to automatically decode string values
                immediately after loading the Dataset. Defaults to False.
            track (bool, optional): Flag to enable tracking of RawDataElement decoding.
        """
        super().__init__(file, extractor)
        if stop_when and not callable(stop_when):
            stop_when = stop_at_tag(stop_when)
        tracker = Tracker() if track else None
        with raw_elem_tracker(tracker), open_any(file, mode="rb") as rfile:
            dataset = read_partial(
                rfile,
                force=force,
                defer_size=defer_size,
                specific_tags=specific_tags,
                stop_when=stop_when,
            )
        object.__setattr__(self, "dataset", DSWrap(dataset))
        object.__setattr__(self, "tracker", tracker)
        if decode:
            self.decode()

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata of the DICOM dataset."""
        firstname, lastname = utils.get_patient_name(self)
        defaults: t.Dict[str, t.Any] = {
            "subject.label": self.get("PatientID"),
            "subject.firstname": firstname,
            "subject.lastname": lastname,
            "subject.sex": self.get("PatientSex"),
            "session.uid": self.get("StudyInstanceUID"),
            "session.label": utils.get_session_label(self),
            "session.age": utils.get_session_age(self),
            "session.weight": self.get("PatientWeight"),
            "session.operator": self.get("OperatorsName"),
            "session.timestamp": utils.get_session_timestamp(self),
            "acquisition.uid": utils.get_acquisition_uid(self),
            "acquisition.label": utils.get_acquisition_label(self),
            "acquisition.timestamp": utils.get_acquisition_timestamp(self),
            "file.type": "dicom",
            "file.name": utils.get_instance_filename(self),
        }
        return {k: v for k, v in defaults.items() if v is not None and v != ""}

    @property
    def sort_key(self) -> t.Tuple[str, str, str]:
        """Return DICOM sort key."""
        meta = self.meta
        return (
            meta.get("session.uid") or meta.get("session.label") or "",
            meta.get("acquisition.uid") or meta.get("acquisition.label") or "",
            self.get("SOPInstanceUID") or "",
        )

    def save(self, file: t.Optional[AnyIO] = None) -> None:
        """Save the dataset to original or specified filepath."""
        with open_any(file or self.filepath, mode="wb") as wfile:
            self.dataset.save_as(wfile)
        if file and get_filepath(file):
            object.__setattr__(self, "filepath", get_filepath(file))

    def decode(self):
        """Decodes file."""
        self.dataset.decode()

    def dir(self, *filters: str) -> t.List[str]:
        """Return an alphabetical list of element keywords."""
        return self.dataset.dir(*filters)

    def walk(
        self, callback: t.Callable[[Dataset, DataElement], None], recursive: bool = True
    ):
        """Iterate through the dataelements of the instance and run callback on each."""
        return self.dataset.walk(callback, recursive=recursive)

    def get_dataelem(self, key: TagType) -> DataElement:
        """Get DataElement for the given tag."""
        tag = self.dataset.validate_key(key)
        return self.dataset.get_dataelem(tag)

    def __contains__(self, key: TagType) -> bool:
        """Return True if the tag/keyword is in the dataset."""
        return key in self.dataset

    def __getitem__(self, key: TagType) -> t.Any:
        """Get dataelement value by tag/keyword."""
        with raw_elem_tracker(self.tracker):
            return self.dataset[key]

    def __setitem__(self, key: TagType, value: t.Any) -> None:
        """Set dataelement value by tag/keyword."""
        self.dataset[key] = value

    def __delitem__(self, key: TagType) -> None:
        """Delete a dataelement by tag/keyword."""
        del self.dataset[key]

    def __iter__(self):
        """Return dataelement iterator."""
        # TODO yield valid keys instead of DEs
        return iter(self.dataset)

    def __len__(self) -> int:
        """Return the number of elements in the dataset."""
        return len(self.dataset)


class DICOMCollection(FileCollection):
    """DICOM file collection for reading/writing multiple datasets."""

    filetype = DICOM


class DSWrap(AttrMixin):
    """Dataset wrapper with simplified keys and values."""

    def __init__(self, dataset: Dataset) -> None:
        """Initialize the wrapper by storing a ref to the pydicom dataset."""
        object.__setattr__(self, "raw", dataset)
        object.__setattr__(self, "getattr_proxy", dataset)

    def validate_key(self, key: TagType) -> BaseTag:
        """Return validated tag for the given key."""
        try:
            return get_tag(key, self.raw)
        except ValueError as exc:
            raise KeyError(key) from exc

    def get_dataelem(self, tag: t.Union[BaseTag, "PrivateTag"]) -> DataElement:
        """Get DataElement for the given tag."""
        if isinstance(tag, PrivateTag):
            return self.raw.get_private_item(tag.group, tag.element_offset, tag.creator)
        return self.raw[tag]

    def __contains__(self, key: TagType) -> bool:
        """Return True if the tag/keyword is in the dataset."""
        tag = self.validate_key(key)
        return tag in self.raw

    def __getitem__(self, key: TagType) -> t.Any:
        """Get dataelement value by tag/keyword."""
        # TODO repeaters
        tag = self.validate_key(key)
        if tag.group == 2:
            return get_value(self.raw.file_meta[tag].value)
        return get_value(self.get_dataelem(tag).value)

    def __setitem__(self, key: TagType, value: t.Any) -> None:
        """Set dataelement value by tag/keyword."""
        tag = self.validate_key(key)
        try:
            VR = self.get_dataelem(tag).VR
        except KeyError:
            VR = get_VR(tag)
        if isinstance(tag, PrivateTag):
            try:
                block = self.raw.private_block(tag.group, tag.creator, create=True)
            except StopIteration as exc:
                raise KeyError(key) from exc
            block.add_new(tag.element_offset, VR, value)
        elif tag.group == 2:
            self.raw.file_meta.add_new(tag, VR, value)
        else:
            self.raw.add_new(tag, VR, value)

    def __delitem__(self, key: TagType) -> None:
        """Delete a dataelement by tag/keyword."""
        tag = self.validate_key(key)
        if isinstance(tag, PrivateTag):
            block = self.raw.private_block(tag.group, tag.creator)
            del block[tag.element_offset]
        elif tag.group == 2:
            del self.raw.file_meta[tag]
        else:
            del self.raw[tag]

    def __iter__(self):
        """Return dataelement iterator."""
        return iter(self.raw)

    def __len__(self) -> int:
        """Return the number of elements in the dataset."""
        return len(self.raw)


class PrivateTag:  # pylint: disable=too-few-public-methods
    """Private tag with creator."""

    def __init__(self, group: int, creator: str, element_offset: int):
        self.group = group
        self.creator = creator
        self.element_offset = element_offset
        elem = f"{self.element_offset:04x}"[2:]
        self.xtag = f"{self.group:04x}xx{elem}"


def get_tag(
    key: TagType, dataset: t.Optional[Dataset] = None
) -> t.Union[BaseTag, PrivateTag]:
    """Return BaseTag/PrivateTag from a tag key and an optional dataset context."""
    # try basic public tags first (eg. "PatientID", "ggggeeee", etc.)
    try:
        return Tag(key)
    except ValueError:
        pass
    # canonize keywords and tags ("Patient's Id"->patientid, 6789XXAB->6789xxab)
    if isinstance(key, str):
        key = canonize_key(key)
    # enable case-insensitive public tag keywords (eg. patientid)
    for keyword, tag in keyword_dict.items():
        if canonize_key(keyword) == key:
            return Tag(tag)
    # privates beyond (or invalid keys)
    if isinstance(key, str):
        creator, xtag = None, key
    if isinstance(key, (list, tuple)):
        creator, xtag = key
    return get_private_tag(xtag, creator=creator, dataset=dataset)


def get_private_tag(
    kw_or_xtag: str,
    creator: t.Optional[str] = None,
    dataset: t.Optional[Dataset] = None,
) -> PrivateTag:
    """Return PrivateTag from a private keyword or xtag.

    Args:
        kw_or_xtag (str): Private tag keyword - the canonized tag name from the
            private dictionary - or an xtag like "ggggxxee".
        creator (str, optional): Private creator string to filter matching
            private dictionary entries with if given.
        dataset (Dataset, optional): Dataset to use as context for the private
            tag lookup - if `kw_or_xtag` does not uniquely identify a specific
            tag in the dictionary but exactly one of the candidates is present
            in the dataset then that candidate is returned.
    """
    if not creator and not dataset:
        raise ValueError("Either creator or dataset required")

    if not creator and not CONFIG.implicit_creator:
        raise ValueError("Explicit creator required")

    kw_or_xtag_ = canonize_key(kw_or_xtag)
    if re.match(r"[0-9a-f]{4}xx[0-9a-f]{2}", kw_or_xtag_):
        keyword, xtag = None, kw_or_xtag_
    else:
        keyword, xtag = kw_or_xtag_, None  # type: ignore
    dataset = dataset or Dataset()
    dataset_creators = {de.value for de in dataset if de.tag.is_private_creator}
    if creator and creator in dataset_creators and xtag:
        group, elem = xtag[:4], xtag[6:]
        return PrivateTag(int(group, 16), creator, int(elem, 16))
    matches = filter_private_tags(creator, xtag, keyword)
    context = f"{kw_or_xtag!r} (creator {creator!r})"
    if not matches:
        raise ValueError(f"No private tags found for {context}")
    if len(matches) > 1:
        # narrow down potential creators based on those present in the dataset
        matches = {k: v for k, v in matches.items() if k in dataset_creators}
    if len(matches) != 1:
        # could not narrow down to one creator (either multiple left or none)
        raise ValueError(f"Multiple private creators found for {context}")
    # creator is now uniquely identified
    creator, xtags = list(matches.items())[0]
    if len(xtags) > 1:
        # narrow down potential xtags based on those present in the dataset
        xtags = {t for t in xtags if has_private_tag(dataset, creator, t)}
    if len(xtags) > 1:
        # could not narrow down to one xtag (multiple left)
        raise ValueError(f"Multiple private tags found for {context}")
    if len(xtags) == 0:
        # could not narrow down to one xtag (none)
        raise ValueError(f"No private tag found for {context}")
    # xtag is now uniquely identified
    xtag = list(xtags)[0]
    group, elem = xtag[:4], xtag[6:]
    return PrivateTag(int(group, 16), creator, int(elem, 16))


def filter_private_tags(
    creator: t.Optional[str] = None,
    xtag: t.Optional[str] = None,
    keyword: t.Optional[str] = None,
) -> t.Dict[str, t.Set[str]]:
    """Return filtered {creator: {xtag}} dictionary."""
    matches: t.Dict[str, t.Set[str]] = {}
    for creator_, private_dict in private_dictionaries.items():
        # TODO creator fuzzyness
        if creator and creator != creator_:
            continue
        for xtag_, entry in private_dict.items():
            if xtag and xtag != xtag_:
                continue
            keyword_ = entry[2]
            if keyword and keyword != canonize_key(keyword_):
                continue
            matches.setdefault(creator_, set()).add(xtag_)
    return matches


def has_private_tag(
    dataset: Dataset,
    creator: str,
    xtag: str,
) -> bool:
    """Return True if the given private creator/xtag exists in the dataset."""
    group = int(xtag[:4], 16)
    element_offset = int(xtag[6:], 16)
    try:
        dataset.get_private_item(group, element_offset, creator)
        return True
    except KeyError:
        return False


def get_value(value: t.Any) -> t.Any:
    """Return 'simplified' value for given DataElement value."""
    if isinstance(value, IS):
        value = int(value)
    elif isinstance(value, (DA, DT, PersonName, TM, UID)):
        value = str(value)
    elif isinstance(value, (DSfloat, DSdecimal)):
        value = float(value)
    elif isinstance(value, Sequence):
        value = [DSWrap(v) for v in value]
    elif isinstance(value, MultiValue):
        value = [get_value(v) for v in value]
    elif isinstance(value, bytes):
        try:
            # TODO encoding and/or heuristic
            value = value.decode().strip("\x00 ")
            if "\\" in value:
                value = value.split("\\")
        except UnicodeDecodeError:
            pass
    return value


def get_VR(tag: t.Union[BaseTag, PrivateTag]) -> str:
    """Get VR for a known tag."""
    if isinstance(tag, PrivateTag):
        return private_dictionaries[tag.creator][tag.xtag][0]
    return dictionary_VR(tag)


def stop_at_tag(tag: TagType) -> StopWhen:
    """Return stop_when function for given tag."""
    stop_tag = Tag(tag)

    # pylint: disable=invalid-name,unused-argument
    def stop_when(current_tag: Tag, VR: str, length: int) -> bool:
        """Return True if the current tag equals the stop_tag."""
        return current_tag == stop_tag

    return stop_when


def canonize_key(key: str) -> str:
    """Return canonized string form for a given tag name or description."""
    return re.sub(r"[^a-z0-9]", "", key.lower().replace("'s", ""))
