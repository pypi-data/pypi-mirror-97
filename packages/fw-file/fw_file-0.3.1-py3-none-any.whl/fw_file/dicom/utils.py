"""DICOM file Flywheel utils."""
import datetime as dt
import functools
import re
import typing as t

import pydicom.uid

from .config import UID_PREFIX

# See: https://github.com/pydicom/pydicom/blob/v2.1.2/pydicom/uid.py#L382
generate_uid = functools.partial(pydicom.uid.generate_uid, prefix=f"{UID_PREFIX}.2.")


def parse_datetime_str(timestamp: str) -> t.Optional[dt.datetime]:
    """Parse datetime string.

    Args:
        timestamp (str): DICOM DT formatted timestamp: YYYYMMDDHHMMSS.FFFFFF&ZZXX
            The year is required, but everything else has defaults:
              - month, day: 1
              - hour: 12
              - minute, second, microsecond: 0

    Reference:
      http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """
    # pylint: disable=too-many-locals
    match = re.match(r"((\d{4,14})(\.(\d{1,6}))?)([+-]\d{4})?", timestamp)
    if not match:
        return None
    dt_match = match.group(2)
    year = int(dt_match[0:4])
    month = day = 1
    hour = 12
    minute = second = microsecond = 0
    tzinfo = None
    if len(dt_match) >= 6:
        month = int(dt_match[4:6])
    if len(dt_match) >= 8:
        day = int(dt_match[6:8])
    if len(dt_match) >= 10:
        hour = int(dt_match[8:10])
    if len(dt_match) >= 12:
        minute = int(dt_match[10:12])
    if len(dt_match) >= 14:
        second = int(dt_match[12:14])
        ms_match = match.group(4)
        if ms_match:
            microsecond = int(ms_match.rstrip().ljust(6, "0"))
    tz_match = match.group(5)
    if tz_match:
        offset1 = int(tz_match[1:3]) * 60
        offset2 = int(tz_match[3:5])
        offset = (offset1 + offset2) * 60
        if tz_match[0] == "-":
            offset = -offset
        tzinfo = dt.timezone(dt.timedelta(seconds=offset), tz_match)

    try:
        dt_obj = dt.datetime(
            year, month, day, hour, minute, second, microsecond, tzinfo
        )
    except ValueError:
        return None

    return dt_obj


def get_timestamp(
    dcm: t.Mapping[str, t.Any], tag_prefix: str
) -> t.Optional[dt.datetime]:
    """Get timezone aware timestamp.

    Use *Date, *Time, *DateTime, TimezoneOffsetFromUTC fields.

    References:
    - DA/TM/DT VR types:
      http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html

    Args:
        tag_prefix (str): Dicom tag prefix - "Study", "Series", "Acquisition".
        dcm (dicom.DICOM): DICOM instance to use
    """
    datetime_str = ""
    if dcm.get(f"{tag_prefix}DateTime"):
        datetime_str = dcm.get(f"{tag_prefix}DateTime")  # type: ignore
    else:
        date = dcm.get(f"{tag_prefix}Date")
        if not date:
            # if no date then just return
            return None
        time = dcm.get(f"{tag_prefix}Time", "")
        datetime_str = f"{date}{time}"
    # get offset from TimezoneOffsetFromUTC if not in the datetime string yet
    if not re.match(r"[+-]\d{4}$", datetime_str):
        offset = dcm.get("TimezoneOffsetFromUTC", "")
        if offset and offset[0] not in "+-":
            # make sure offset is sign-prefixed (sign optional in this tag)
            offset = f"+{offset}"
        datetime_str = f"{datetime_str}{offset}"
    return parse_datetime_str(datetime_str)


def get_patient_name(
    dcm: t.Mapping[str, t.Any]
) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """Return firstname, lastname tuple."""
    name = dcm.get("PatientName")
    if not name:
        return None, None
    if "^" in name:
        lastname, _, firstname = name.partition("^")
    else:
        firstname, _, lastname = name.rpartition(" ")
    return (firstname.strip().title() or None, lastname.strip().title() or None)


def get_session_age(dcm: t.Mapping[str, t.Any]) -> t.Optional[int]:
    """Return patient age in seconds."""
    if dcm.get("PatientAge"):
        age_str = dcm.get("PatientAge", "")
        match = re.match(r"(?P<value>[0-9]+)(?P<scale>[dwmyDWMY])?", age_str)
        if not match:
            return None

        conversion = {  # conversion to days
            "Y": 365.25,
            "M": 30,
            "W": 7,
            "D": 1,
        }
        value = match.group("value")
        scale = (match.group("scale") or "Y").upper()
        return int(int(value) * conversion[scale] * 86400)

    birth_date = parse_datetime_str(dcm.get("PatientBirthDate", ""))  # type: ignore
    acq_timestamp = get_acquisition_timestamp(dcm)
    if not (birth_date and acq_timestamp):
        return None

    age_in_seconds = acq_timestamp.timestamp() - birth_date.timestamp()
    if age_in_seconds < 0:
        return None

    return int(age_in_seconds)


def get_session_label(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return session label.

    1. StudyDescription
    2. Session timestamp
    3. StudyInstanceUID
    """
    label = dcm.get("StudyDescription")
    if not label and (timestamp := get_session_timestamp(dcm)):
        label = timestamp.isoformat()
    return label or dcm.get("StudyInstanceUID")


def get_session_timestamp(dcm: t.Mapping[str, t.Any]) -> t.Optional[dt.datetime]:
    """Return session timestamp.

    1. StudyDate + Time
    2. SeriesDate + Time
    3. AcquisitionDateTime
    4. AcquisitionDate + Time
    """
    return (
        get_timestamp(dcm, "Study")
        or get_timestamp(dcm, "Series")
        or get_timestamp(dcm, "Acquisition")
    )


def get_acquisition_uid(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return acquisition UID."""
    # TODO GE: separate UID per AcquisitionNumber
    return dcm.get("SeriesInstanceUID")


def get_acquisition_label(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return acquisition label.

    Add "SeriesNumber - " prefix if set in case of SeriesDescription
    and ProtocolName.

    1. SeriesDescription
    2. ProtocolName
    3. Acquisition timestamp
    4. SeriesInstanceUID
    """
    label = dcm.get("SeriesDescription") or dcm.get("ProtocolName")
    if not label:
        timestamp = get_acquisition_timestamp(dcm)
        return timestamp.isoformat() if timestamp else dcm.get("SeriesInstanceUID")
    series_number = dcm.get("SeriesNumber")
    if series_number:
        label = f"{series_number} - {label}"
    return label


def get_acquisition_timestamp(dcm: t.Mapping[str, t.Any]) -> t.Optional[dt.datetime]:
    """Return acquisition timestamp.

    1. AcquisitionDateTime
    2. AcquisitionDate + Time
    3. SeriesDate + Time
    4. StudyDate + Time
    """
    return (
        get_timestamp(dcm, "Acquisition")
        or get_timestamp(dcm, "Series")
        or get_timestamp(dcm, "Study")
    )


def get_instance_filename(dcm: t.Mapping[str, t.Any]) -> str:
    """Return recommended DICOM instance filename."""
    instance_uid = dcm.get("SOPInstanceUID")
    modality = dcm.get("Modality") or "NA"
    return f"{instance_uid}.{modality}.dcm"
