"""Common data-file interface."""
import functools
import typing as t
from abc import abstractmethod
from collections.abc import MutableMapping

from fw_meta import MetaData, MetaExtractor

from .common import AnyIO, AttrMixin, get_filepath


# TODO: remove type ignore when solved: https://github.com/python/mypy/issues/8539
@functools.total_ordering  # type: ignore
class File(AttrMixin, MutableMapping):  # pylint: disable=too-many-ancestors
    """Data-file base class defining the common interface for parsed files."""

    def __init__(
        self,
        file: AnyIO,
        extractor: t.Optional[MetaExtractor] = None,
        **_: t.Any,
    ) -> None:
        """Read the data-file - subclasses are expected to add parsing."""
        # NOTE using object.__setattr__ to side-step AttrMixin
        object.__setattr__(self, "filepath", get_filepath(file))
        object.__setattr__(self, "extractor", extractor or MetaExtractor())

    @property
    @abstractmethod
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata extracted from the file."""

    @property
    def meta(self) -> MetaData:
        """Return the customized Flywheel metadata extracted from the file."""
        return self.extractor.extract(self)

    def save(self, file: t.Optional[AnyIO] = None) -> None:
        """Save (potentially modified) data file."""
        raise NotImplementedError  # pragma: no cover

    @property
    def sort_key(self) -> t.Any:
        """Return sort key used for comparing/ordering instances."""
        return self.filepath  # pragma: no cover

    def __eq__(self, other: object) -> bool:
        """Return that file equals other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key == other.sort_key

    def __lt__(self, other: object) -> bool:
        """Return that file is before other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key < other.sort_key

    def __repr__(self):
        """Return string representation of the data-file."""
        return f"{type(self).__name__}({self.filepath!r})"
