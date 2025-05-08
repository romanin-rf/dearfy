from os import PathLike
from pathlib import Path, PosixPath, WindowsPath, PurePath, PurePosixPath, PureWindowsPath
from typing_extensions import Any, Iterable, Callable, TypeAlias

# ! Typing

FilePath: TypeAlias     = str | PathLike[str] | Path | PosixPath | WindowsPath | PurePath | PurePosixPath | PureWindowsPath

# ! DearPyGUI Typing

Tag: TypeAlias          = str | int
Position: TypeAlias     = tuple[int, int] | Iterable[int]
Size: TypeAlias         = tuple[int, int] | Iterable[int]
Color: TypeAlias        = tuple[int, int, int, int] | Iterable[int]

Callback: TypeAlias     = \
    Callable[[str], Any] | \
    Callable[[str], Any] | \
    Callable[[str, Any | None], Any] | \
    Callable[[str, Any | None, Any | None], Any] | \
    str | tuple[str, str]