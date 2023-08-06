"""Generic file collection class."""
import abc
import logging
import pathlib
import shutil
import tempfile
import typing as t
import zipfile

from .common import AnyIO, AnyPath
from .file import File

__all__ = ["FileCollection"]

log = logging.getLogger(__name__)


class FileCollection(list):
    """Abstract class for handling multiple files of the same type in a DIR/ZIP."""

    @property
    @abc.abstractmethod
    def filetype(self) -> t.Type[File]:
        """The File subclass to instantiate files with."""

    def __init__(self, **file_kw: t.Any) -> None:
        """Initialize an empty FileCollection.

        Args:
            **file_kw: Keyword arguments to use when loading files.
        """
        super().__init__()
        self.file_kw = file_kw
        self.errors: t.Dict[str, str] = {}
        self.dirpath: t.Optional[pathlib.Path] = None
        self.is_tmp = False

    @classmethod
    def from_dir(
        cls,
        dirpath: AnyPath,
        pattern: str = "*",
        recurse: bool = True,
        **file_kw: t.Any,
    ) -> "FileCollection":
        """Return collection from a directory.

        Args:
            dirpath (str|Path): Directory path to load files from.
            pattern (str, optional): Glob pattern to match files on. Default: "*".
            recurse (bool, optional): Toggle for enabling recursion. Default: True.
            **file_kw: Keyword arguments to initialize data-files with.
        """
        self = cls(**file_kw)
        self.dirpath = pathlib.Path(dirpath)
        for path in fileglob(dirpath, pattern=pattern, recurse=recurse):
            try:
                self.append(path)
            except Exception as exc:  # pylint: disable=broad-except
                msg = f"{type(exc).__name__}: {exc}"
                log.error(f"Cannot load {self.filetype.__name__} {path}: {msg}")
                relpath = str(path.relative_to(dirpath))
                self.errors[relpath] = msg
        return self

    @classmethod
    def from_zip(
        cls,
        archive: AnyIO,
        pattern: str = "*",
        recurse: bool = True,
        **file_kw: t.Any,
    ) -> "FileCollection":
        """Return FileCollection from a ZIP archive.

        Args:
            archive (str|Path|file): The ZIP archive path or readable to extract
                into a temporary directory and read all files from.
            pattern (str, optional): Glob pattern to match files on. Default: "*".
            recurse (bool, optional): Toggle for enabling recursion. Default: True.
            **file_kw: Keyword arguments to initialize data-files with.
        """
        tempdir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, mode="r") as zfile:
            zfile.extractall(tempdir)
        coll = cls.from_dir(tempdir, pattern=pattern, recurse=recurse, **file_kw)
        coll.is_tmp = True
        return coll

    def __setitem__(  # type: ignore[override]
        self,
        index: int,
        value: t.Union[AnyIO, File],
    ):
        """Add a file to the collection."""
        if isinstance(index, slice):
            raise KeyError("Slice is not supported")
        if not isinstance(value, self.filetype):
            value = self.filetype(t.cast(AnyIO, value), **self.file_kw)
        super().__setitem__(index, value)

    def insert(self, index: int, value: t.Union[AnyIO, File]) -> None:
        """Insert file before the given index."""
        if not isinstance(value, self.filetype):
            value = self.filetype(t.cast(AnyIO, value), **self.file_kw)
        super().insert(index, value)

    def append(self, value: t.Union[AnyIO, File]) -> None:
        """Append new file to the end of the collection."""
        self.insert(len(self), value)

    def bulk_get(self, key: str, default: t.Any = None) -> t.List[t.Any]:
        """Get attribute across collection."""
        return [file.get(key, default) for file in self]

    def bulk_set(self, key: str, value: t.Any) -> None:
        """Set attribute across collection."""
        for file in self:
            file[key] = value

    def bulk_del(self, key: str) -> None:
        """Delete attribute across collection."""
        for file in self:
            del file[key]

    def bulk_save(self) -> None:
        """Save files across collection to their original location."""
        for file in self:
            file.save()

    @staticmethod
    def name_fn(file: File) -> str:
        """Return filename (basename) for a given file."""
        return pathlib.Path(file.filepath).name

    def to_dir(
        self, dirpath: AnyPath, name_fn: t.Optional[t.Callable[[File], str]] = None
    ) -> None:
        """Save all files to the given directory.

        Args:
            dirpath (str|Path): Destination directory. Create if not exists.
            name_fn (callable, optional): Custom callable to name the files before save.
        """
        if not name_fn:
            name_fn = self.name_fn
        if isinstance(dirpath, str):
            dirpath = pathlib.Path(dirpath)
        dirpath.resolve()
        for file in self:
            filepath = dirpath / pathlib.Path(name_fn(file))
            filepath.parent.mkdir(parents=True, exist_ok=True)
            file.save(filepath)

    def to_zip(
        self,
        archive: AnyIO,
        comment: t.Optional[t.AnyStr] = None,
        name_fn: t.Optional[t.Callable[[File], str]] = None,
        **zip_kw: t.Any,
    ) -> None:
        """Save all files to the given ZIP archive.

        Args:
            archive (str|Path|file): The ZIP archive path or writable to save files to.
            comment (str|bytes, optional): ZIP comments to save with. Default: None.
            name_fn (callable, optional): Custom callable to name the files before save.
                Use filepath by default.
            **zip_kw: Additional keyword arguments to pass to zipfile.ZipFile.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            self.to_dir(tempdir, name_fn)
            zip_kw.setdefault("allowZip64", True)
            with zipfile.ZipFile(archive, mode="w", **zip_kw) as zfile:
                for path in fileglob(tempdir, recurse=True):
                    relpath = path.relative_to(tempdir)
                    zfile.write(str(path), arcname=relpath)
                if isinstance(comment, str):
                    zfile.comment = comment.encode("utf8")
                elif isinstance(comment, bytes):
                    zfile.comment = comment

    def cleanup(self) -> None:
        """Remove the tempdir extracted to via 'from_zip()'."""
        if self.is_tmp and self.dirpath:
            shutil.rmtree(self.dirpath)
            self.is_tmp = False

    def __contains__(self, file: object) -> bool:
        """Return True IFF the given file is in the collection."""
        if isinstance(file, self.filetype):
            return super().__contains__(file)
        return any(f.filepath == file for f in self)

    def __enter__(self):
        """Return self for 'with' context usage (auto-removing temp files)."""
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        """Remove any temp files when exiting the 'with' context."""
        self.cleanup()

    def __del__(self) -> None:
        """Remove any temp files when the collection is GC'd."""
        self.cleanup()


def fileglob(
    dirpath: AnyPath,
    pattern: str = "*",
    recurse: bool = False,
) -> t.List[pathlib.Path]:
    """Return the list of files under a given directory.

    Args:
        dirpath (str|Path): The directory path to glob in.
        pattern (str, optional): The glob pattern to match files on. Default: "*".
        recurse (bool, optional): Toggle for enabling recursion. Default: False.

    Returns:
        list[Path]: The file paths that matched the glob within the directory.
    """
    if isinstance(dirpath, str):
        dirpath = pathlib.Path(dirpath)
    glob_fn = getattr(dirpath, "rglob" if recurse else "glob")
    return list(sorted(f for f in glob_fn(pattern) if f.is_file()))
