"""Local storage module."""
import functools
import os
import re
import shutil
import typing as t
from pathlib import Path

from fw_utils import AnyFile, BinFile

from .. import FileNotFound, PermError, Storage
from ..fileinfo import FileInfo
from ..filters import Filter, PathFilter
from ..storage import AnyPath

__all__ = ["FileSystem"]

CHUNKSIZE = 8 << 20


def translate_error(func):
    """Raise storage errors from built-in filesystem errors."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as exc:
            msg = re.sub(r"\[.*\]\s*(.*)", r"\1", str(exc))
            raise FileNotFound(msg) from exc
        except PermissionError as exc:
            msg = re.sub(r"\[.*\]\s*(.*)", r"\1", str(exc))
            raise PermError(msg) from exc

    return wrapper


class FileSystem(Storage):
    """Storage class for locally mounted filesystems."""

    url_re = re.compile(r"fs://(?P<path>[^?]*)(\?(?P<query>[^#]+))?")

    def __init__(self, path: t.Union[str, Path] = "", write: bool = False) -> None:
        """Init FileSystem storage from a path (default: cwd)."""
        path = Path(path) if path else Path.cwd()
        self.prefix = path.expanduser().resolve()
        self.check_perms(write=write)

    def abspath(self, path: AnyPath) -> str:
        """Return absolute path for a given path."""
        return str(self.prefix / self.relpath(path))

    def check_access(self):
        """Check that root folder exists."""
        if not self.prefix.exists():
            raise FileNotFound(f"Root dir not found: {self.prefix!r}")

    @translate_error
    def ls(  # pylint: disable=arguments-differ
        self,
        path: str = "",
        *,
        include: t.Optional[t.List[str]] = None,
        exclude: t.Optional[t.List[str]] = None,
        followlinks: bool = False,
        **_,
    ) -> t.Iterator[FileInfo]:
        """Yield each item under prefix matching the include/exclude filters."""
        # pylint: disable=too-many-locals
        # TODO consider adding in some retries/tolerance for network mounts
        start = (self.prefix / path).resolve()
        filt = Filter(include=include, exclude=exclude, factory={"dir": PathFilter})
        info_types = ["size", "created", "modified"]
        info_match = functools.partial(filt.match, types=info_types)
        root_files = []

        for root, dirs, files in os.walk(start, followlinks=followlinks):

            def rel(name: str) -> str:
                """Return path relative to prefix for given file/dir-name."""
                # pylint: disable=cell-var-from-loop
                return re.sub(fr"^{self.prefix}", "", f"{root}/{name}").strip("/")

            # sort the dirs to enforce deterministic walk order
            # apply the dir filters to efficiently prune the walk tree
            dirs.sort()
            dirs[:] = [d for d in dirs if filt.match(rel(d), types=["dir"])]

            # sort the files to enforce deterministic behavior and yield order
            # apply the path filters before using os.stat for efficiency
            files.sort()
            files = [rel(f) for f in files if filt.match(rel(f), types=["path"])]

            # root level files need special treatment to achieve full ordering
            # eg. 'zfile' would come before 'adir/afile' by default - store and
            # yield them interleaved with the other files as appropriate
            if root == str(self.prefix):
                root_files = files
                continue

            for file in files:
                # root file interleaving according to sort order
                while root_files and root_files[0] < file:
                    info = self.stat(root_files.pop(0))
                    if info_match(info):
                        yield info

                # yield the matching files from this dir
                info = self.stat(file)
                if info_match(info):
                    yield info

        # yield any remaining root files
        for file in root_files:
            info = self.stat(file)
            if info_match(info):
                yield info

    @translate_error
    def stat(self, path: str) -> FileInfo:
        """Return FileInfo using os.stat for a single file."""
        stat = (self.prefix / path).stat()
        return FileInfo(
            path=path,
            size=stat.st_size,
            created=stat.st_ctime,
            modified=stat.st_mtime,
        )

    @translate_error
    def get(self, path: AnyPath, **_) -> BinFile:
        """Open file for reading in binary mode."""
        return BinFile(self.abspath(path), metapath=self.relpath(path))

    @translate_error
    def set(self, path: AnyPath, file: t.Union[AnyFile, bytes]) -> None:
        """Write file to the given storage path."""
        path_ = Path(self.abspath(path))
        path_.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(file, bytes):
            path_.write_bytes(file)
            return
        with BinFile(file) as r_file, BinFile(path_, write=True) as w_file:
            while data := r_file.read(CHUNKSIZE):
                w_file.write(data)

    @translate_error
    def rm(self, path: AnyPath, recurse: bool = False) -> None:
        """Remove a file at the given path."""
        path_ = Path(self.abspath(path))
        if path_.is_dir():
            if not recurse:
                raise ValueError("Cannot remove dir (use recurse=True)")
            shutil.rmtree(path_)
        else:
            path_.unlink()

    def __repr__(self) -> str:
        """Return string representation of the storage."""
        return f"{type(self).__name__}('{self.prefix}')"
