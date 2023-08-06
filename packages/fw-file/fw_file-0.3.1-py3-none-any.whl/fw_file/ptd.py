"""Reading and writing Siemens RAW PET - aka. PTD - data (.ptd files)."""
import io
import struct
import typing as t

from .common import AnyIO, get_filepath, open_any
from .dicom.dicom import DICOM, TagType
from .file import File

MAGIC_STR = b"LARGE_PET_LM_RAWDATA"
MAGIC_LEN = len(MAGIC_STR)
INT_SIZE = struct.calcsize("i")


class PTD(File):  # pylint: disable=too-many-ancestors
    """PTD data-file class.

    Siemens RAW PET files are usually named with the extension ".ptd".
    PTD is a proprietary file format which has an embedded DICOM dataset:
        <PTD PREAMBLE> <DICOM DATASET> <DICOM SIZE> <MAGIC BYTES>
    This parser peels the wrapping bytes and exposes the embedded DICOM.
    """

    def __init__(self, file: AnyIO, **kwargs: t.Any) -> None:
        """Initialize a PTD file by extracting the embedded DICOM.

        Args:
            file (str|Path|file): The file to read from as a string (filepath),
                Path or file-like object. Files opened from str and Path objects
                are automatically closed after reading. The caller is
                responsible for closing file-like objects.
            kwargs: Extra keyword args to pass to `fw_file.dicom.dicom.DICOM`.
        """
        super().__init__(file)
        with open_any(file, mode="rb") as rfile:
            # verify PTD magic bytes at the end of the file
            rfile.seek(-MAGIC_LEN, 2)
            magic_str = rfile.read(MAGIC_LEN)
            if magic_str != MAGIC_STR:
                msg = "Invalid PTD magic bytes: {!r} (expected {!r})"
                raise ValueError(msg.format(magic_str, MAGIC_STR))

            # calculate the PTD preamble size
            rfile.seek(-INT_SIZE - MAGIC_LEN, 2)
            dcm_size = struct.unpack("i", rfile.read(INT_SIZE))[0]
            dcm_offset = dcm_size + INT_SIZE + MAGIC_LEN
            ptd_size = rfile.seek(0, 2) - dcm_offset

            # store the proprietary PTD preamble data as bytes
            rfile.seek(0)
            object.__setattr__(self, "preamble", rfile.read(ptd_size))

            # store the DICOM parsed
            dcm_buffer = io.BytesIO(rfile.read(dcm_size))
            object.__setattr__(self, "dcm", DICOM(dcm_buffer, **kwargs))

    def __getitem__(self, key: TagType) -> t.Any:
        """Get dataelement value by tag/keyword."""
        return self.dcm[key]

    def __setitem__(self, key: TagType, value: t.Any) -> None:
        """Set dataelement value by tag/keyword."""
        self.dcm[key] = value

    def __delitem__(self, key: TagType) -> None:
        """Delete a dataelement by tag/keyword."""
        del self.dcm[key]

    def __iter__(self):
        """Return dataelement iterator."""
        return iter(self.dcm)

    def __len__(self) -> int:
        """Return the number of elements in the dataset."""
        return len(self.dcm)

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata extracted from the PTD."""
        meta = self.dcm.default_meta
        meta["file.type"] = "ptd"  # TODO cross-check with core's filetypes
        meta["file.name"] = meta["file.name"].replace(".dcm", ".ptd")
        return meta

    def save(self, file: t.Optional[AnyIO] = None) -> None:
        """Save PTD file."""
        with open_any(file or self.filepath, mode="wb") as wfile:
            wfile.write(self.preamble)
            self.dcm.save(wfile)
            dcm_size = wfile.tell() - len(self.preamble)
            wfile.write(struct.pack("i", dcm_size))
            wfile.write(MAGIC_STR)
        if file and get_filepath(file):
            object.__setattr__(self, "filepath", get_filepath(file))
