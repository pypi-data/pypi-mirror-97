"""Reading and writing Philips PAR/REC MR image header data (.PAR files)."""
import datetime as dt
import re
import typing as t
from decimal import Decimal, InvalidOperation

import dateutil.parser as dt_parser
from fw_meta import MetaExtractor

from .common import FieldsMixin, get_filepath, open_any
from .file import AnyIO, File

GENERAL_INFO_LINE_RE = re.compile(r"^\.\s+(?P<name>\w[^:]+).*?:\s*(?P<value>.*)$")
GENERAL_INFO_KEY_RE = re.compile(r"^(?P<key>[-\.\w\s/]+).*$")


class PAR(FieldsMixin, File):  # pylint: disable=too-many-ancestors
    """Philips PAR MR image header file."""

    def __init__(
        self,
        file: AnyIO,
        extractor: t.Optional[MetaExtractor] = None,
    ) -> None:
        """PAR file reading and writing.

        Args:
            file (str|Path|file): The file to read from as a string (filepath),
                Path or file-like object. Files opened from str and Path objects
                are automatically closed after reading. The caller is responsible
                for closing file-like objects.
            extractor (MetaExtractor, optional): MetaExtractor instance to
                customize metadata extraction with if given. Default: None.
        """
        super().__init__(file, extractor)
        object.__setattr__(self, "fields", parse_par_file(file))

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata."""
        meta: t.Dict[str, t.Any] = {
            "subject.label": self.get("patient_name"),
            "session.label": self.get("examination_name"),
            "acquisition.label": get_acquisition_label(self),
            "acquisition.timestamp": get_acquisition_timestamp(self),
            "file.type": "parrec",
        }
        return {k: v for k, v in meta.items() if v is not None and v != ""}

    @staticmethod
    def canonize_key(key: str) -> str:
        """Return canonized string form for a given field name."""
        return canonize_key(key)

    def save(self, file: t.Optional[AnyIO] = None) -> None:
        """Save modified data file."""
        lines = []
        just_len = max(
            len(f["name"]) for f in self.fields.values() if isinstance(f, dict)
        )
        for val in self.fields.values():
            if isinstance(val, str):
                lines.append(val)
                continue
            name = val["name"].ljust(just_len)
            val = val["value"]
            if isinstance(val, list):
                # double space used in most of the example PAR files
                val = "  ".join([str(v) for v in val])
            if val is None:
                val = ""
            lines.append(f".    {name}:   {val}\n")
        with open_any(file or self.filepath, "w") as file_obj:
            file_obj.writelines(lines)
        if file and get_filepath(file):
            object.__setattr__(self, "filepath", get_filepath(file))

    def __getitem__(self, key: str) -> t.Any:
        """Get field value by tag/keyword."""
        return self.fields[canonize_key(key)]["value"]

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Set field value by tag/keyword."""
        key = canonize_key(key)
        if key not in self.fields:
            raise KeyError("Invalid key")
        self.fields[key]["value"] = value


def parse_par_file(file: AnyIO) -> t.Dict[t.Union[int, str], t.Any]:
    """Parse PAR file.

    Return parsed PAR file as a dictionary. General info fields are parsed
    as name/value and available via a canonized key. For other lines we just store
    the raw line and use the line number as key.
    """
    parsed: t.Dict[t.Union[int, str], t.Any] = {}
    with open_any(file, "r") as file_obj:
        line_no = 0
        for line in file_obj:
            match = GENERAL_INFO_LINE_RE.match(line)
            if match:
                name = match.group("name").strip()
                value = match.group("value").strip()
                value = parse_value(value) if value else None
                key = canonize_key(name)
                parsed[key] = dict(name=name, value=value)
            else:
                parsed[line_no] = line
            line_no += 1
    return parsed


def parse_value(value: str) -> t.Any:
    """Parse field value.

    Try parse value string as list of integers and decimals,
    fallback to the original str. Return single value if the
    list contains only one item.
    """
    parsed_val: t.Any = None
    parts = value.split()
    # try as integer
    try:
        parsed_val = [int(v) for v in parts]
    except ValueError:
        pass
    # try as decimal
    if not parsed_val:
        try:
            parsed_val = [Decimal(v) for v in parts]
        except InvalidOperation:
            pass
    # fallback to the original value
    if not parsed_val:
        return value
    if isinstance(parsed_val, list) and len(parsed_val) == 1:
        parsed_val = parsed_val[0]
    return parsed_val


def canonize_key(key: str) -> str:
    """Return canonized string form for a given field name."""
    match = GENERAL_INFO_KEY_RE.match(key)
    if not match:
        raise KeyError("Invalid key")
    return re.sub(r"[^a-zA-Z0-9]", "_", match.group("key").strip().lower())


def get_acquisition_label(par: PAR) -> t.Optional[str]:
    """Return acquisition label.

    Combination of Protocol name, Acquisition nr and Reconstruction nr.
    """
    fields = ("protocol_name", "acquisition_nr", "reconstruction_nr")
    parts = [str(par[field]) for field in fields if par.get(field)]
    if not parts:
        return None
    return "_".join(parts)


def get_acquisition_timestamp(par: PAR) -> t.Optional[dt.datetime]:
    """Return acquisition timestamp extracted from Examination date/time field."""
    timestamp = par.get("examination_date_time")
    if not timestamp:
        return None
    try:
        return dt_parser.parse(timestamp)
    except dt_parser.ParserError:  # type: ignore
        return None
