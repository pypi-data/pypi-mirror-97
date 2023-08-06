"""Reading Bruker ParaVision data (subject, acqp and method files)."""
import datetime as dt
import re
import typing as t

from .common import AnyIO, FieldsMixin, open_any
from .file import File

ARRAY_RE = re.compile(r"\( \d+(, \d+)* \)")
VERSION_RE = re.compile(r"(PV|ParaVision) ?(?P<ver>\d+(\.\d+)+)")


class ParaVision(FieldsMixin, File):  # pylint: disable=too-many-ancestors
    """ParaVision parameters data-file."""

    def __init__(self, file: AnyIO) -> None:
        """Load and parse ParaVision parameters files.

        Args:
            file (str|Path|file): The file to read from as a string (filepath),
                Path or file-like object. Files opened from str and Path objects
                are automatically closed after reading. The caller is responsible
                for closing file-like objects.
        """
        super().__init__(file)
        object.__setattr__(self, "fields", parse_pv_file(file))

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata of ParaVision file."""
        session_ts = get_timestamp(self.get("subject_abs_date", ""))
        acq_ts = get_timestamp(self.get("acq_abs_time", ""))
        session_label = [self.get("subject_study_name")]
        if session_ts:
            session_label.append(session_ts.strftime("%Y%m%d%H%M%S"))
        meta = {
            "subject.label": self.get("subject_id"),
            "subject.sex": self.get("subject_sex"),
            "session.uid": self.get("subject_study_instance_uid"),
            "session.label": " - ".join([p for p in session_label if p]),
            "session.timestamp": session_ts,
            "acquisition.label": self.get("acq_protocol_name"),
            "acquisition.timestamp": acq_ts,
            "file.type": "ParaVision",
        }
        return {k: v for k, v in meta.items() if v is not None and v != ""}

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Set field value by name."""
        raise NotImplementedError("Read-only file")

    def __delitem__(self, key: str) -> None:
        """Delete a field by name."""
        raise NotImplementedError("Read-only file")


def parse_pv_file(file: AnyIO) -> t.Dict[str, t.Any]:
    """Parse ParaVision parameters file as a dictionary."""
    fields: t.Dict[str, t.Any] = dict()
    with open_any(file, "r") as file_obj:
        key = None
        for line in file_obj:
            if not fields.get("version") and (match := VERSION_RE.search(line)):
                fields["version"] = match.group("ver")
            if line.startswith("$$"):
                continue
            if line.startswith("##"):
                key, _, value = line.partition("=")
                key = key.lstrip("##$").lower()
                if ARRAY_RE.match(value):
                    value = ""
            else:
                value = line
            if key:
                value = value.strip(" <>\n")
                fields[key] = fields.get(key, "") + value
    return fields


def get_timestamp(value: str) -> t.Optional[dt.datetime]:
    """Return iso timestamp from bruker epoch value."""
    abs_time, *_ = value.strip("()").partition(",")
    if not abs_time:
        return None
    return dt.datetime.utcfromtimestamp(int(abs_time))
