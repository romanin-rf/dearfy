from typing_extensions import Iterable, TypeAlias

# ! DearPyGUI Typing

Tag: TypeAlias          = str | int
Position: TypeAlias     = tuple[int, int] | Iterable[int]
Size: TypeAlias         = tuple[int, int] | Iterable[int]
Color: TypeAlias        = tuple[int, int, int, int] | Iterable[int]