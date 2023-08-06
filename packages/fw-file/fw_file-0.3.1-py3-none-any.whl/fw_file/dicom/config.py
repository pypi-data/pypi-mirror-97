"""DICOM config module."""
# pylint: disable=too-few-public-methods
import functools
import re

from pydantic import BaseSettings
from pydicom import config as pydicom_config

from .. import __version__
from .fixer import backslash_in_VM1_string_callback, converter_exception_callback

# Flywheel DICOM UID Management Plan:
# https://docs.google.com/document/d/1HcMcWBrDsYIFOkMgGL8W7Hzt7I2tl4UbeC40R5HH99A
# UID root for ANSI registered numeric organization name 114570 (Flywheel)
UID_ROOT = "2.16.840.1.114570"
# UID prefix and version of product fw-file
UID_PREFIX = f"{UID_ROOT}.4"
VERSION = re.split(r"[^\d]+", __version__)

# fw-file (0002,0012) ImplementationClassUID
IMPLEMENTATION_CLASS_UID: str = f"{UID_PREFIX}.1.{'.'.join(VERSION)}"
# fw-file (0002,0013) ImplementationVersionName
IMPLEMENTATION_VERSION_NAME: str = f"FWFILE_{'_'.join(VERSION)}"


class DICOMConfig(BaseSettings):
    """DICOM config."""

    class Config:
        """Enable envvars with prefix `FW_DCM_`."""

        env_prefix = "fw_dcm_"

    # allow private tag access without specifying private creator like dcm["0019xx10"]
    # when enabled dataset/private dict will be used to figure out the private creator
    implicit_creator: bool = False

    # RawDataElement callbacks configuration
    replace_un_with_known_vr: bool = True
    fix_vm1_strings: bool = True
    fix_vr_mismatch: bool = False

    @staticmethod
    def add_VM1_strings_callback():  # pylint: disable=invalid-name
        r"""Add data element callback to fix ``\`` in VM=1 string like data element."""
        pydicom_config.data_element_callback = functools.partial(
            backslash_in_VM1_string_callback,
            data_element_callback=pydicom_config.data_element_callback,
        )

    @staticmethod
    def add_vr_mismatch_callback():
        """Add data element callback to fix corrupted VR.

        By default ``pydicom.config.replace_un_with_known_vr=True`` and pydicom attempts
        to replace UN VR with known VR which enables decoding all possible data
        elements. This is an helpful attempt but it sometimes bumps into
        some issue with certain "corrupted" data element. For example, if a data element
        comes with VR = UN and gets inferred as SQ, we found instances where pydicom
        struggles decoding the nested data elements because of various issue such as:
        additional sequence delimiter which has no VR, non compliant VR or plain unknown
        public tag.

        The following callback pre-processed the RawDataElement object based on some
        heuristic so that ``pydicom.datalement.DataElement_from_raw`` do not raise.

        This callback follows the following heuristic:

            1. If VR is None,
                a. if private or public but not in public dictionary, set VR to UN,
                   else set VR based on public dictionary
                b. Test decoding does not raise with inferred VR, if not set VR to OB
                   (so that pydicom do not longer attempt to infer the VR)
            2. If tag = SpecificCharacterSet, which defines the string encoding, VR is
               UN, set VR to CS.
            3. Run pydicom ``fix_mismatch_callback`` on data element to fix mismatch VR.
            4. If VR is invalid, ``fix_mismatch_callback`` raises
               ``NotImplementedError`` and exception is handled as follow:
                a. if tag is an extra sequence delimiter with VR=None, setting its VR
                   to OB to avoid decoding (setting it to UN or None will raise because
                   VR inference happens downstream in
                   ``pydicom.datalement.DataElement_from_raw``)
                b. else set VR to UN.
                c. if VR = UN and replace_un_with_known_vr == True and tag is not
                   private, inferred VR from public dictionary, try decoding, if
                   exception raises set VR to OB (so that pydicom do not longer
                   attempt to infer the VR)
        """
        pydicom_config.data_element_callback = functools.partial(
            converter_exception_callback,
            data_element_callback=pydicom_config.data_element_callback,
        )
        pydicom_config.data_element_callback_kwargs.update(
            {"with_VRs": ["PN", "DS", "IS"]}
        )

    def configure_pydicom(self):
        """Configure pydicom.config module."""
        pydicom_config.reset_data_element_callback()

        # see https://github.com/pydicom/pydicom/blob/c8f98eba/pydicom/config.py#L171
        pydicom_config.replace_un_with_known_vr = self.replace_un_with_known_vr

        if self.fix_vr_mismatch:
            self.add_vr_mismatch_callback()

        if self.fix_vm1_strings:
            self.add_VM1_strings_callback()


CONFIG = DICOMConfig()
CONFIG.configure_pydicom()
