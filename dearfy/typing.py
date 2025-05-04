from typing_extensions import Iterable, TypeAlias

# ! DearPyGUI Typing

Tag: TypeAlias = str | int
Position: TypeAlias = tuple[int, int] | tuple[int, ...] | list[int] | Iterable[int]