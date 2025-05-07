
# > Typing
from typing_extensions import TypeAlias, Iterable, Iterator, ClassVar
# > Local Imports
from dearfy.base import Item, DOMNode
from dearfy.typing import Color, FilePath
from dearfy.action import (
    Actioner, Action,
    ActionBlockMode, ActionBlockModeLiteral, 
    ActionCallMode, ActionCallModeLiteral,
    ActionName, ActionGroup
)

# ! Types

ComposeResult: TypeAlias = Iterator[Item]

# ! App Base Class

class App(DOMNode):
    _actioner: ClassVar[Actioner]

    _node_children: list[Item]

    def __init__(
        self,
        title: str = 'Dearfy Viewport',
        small_icon: FilePath | None = None,
        large_icon: FilePath | None = None,
        width: int = 1280,
        height: int = 800,
        x_pos: int = 100,
        y_pos: int = 100,
        min_width: int = 250,
        max_width: int = 10000,
        min_height: int = 250,
        max_height: int = 10000,
        resizable: bool = True,
        vsync: bool = True,
        always_on_top: bool = False,
        decorated: bool = True,
        clear_color: Color = (0, 0, 0, 255),
        disable_close: bool = False,
        minimized: bool = False,
        maximized: bool = False
    ) -> None:
        ...
    
    def compose(self) -> ComposeResult: ...

    def __dearfy_compose__(self) -> None: ...
    def __dearfy_preparing__(self) -> None: ...
    def __dearfy_preinit__(self) -> None: ...
    def __dearfy_init__(self) -> None: ...
    def __dearfy_postinit__(self) -> None: ...

    def run(self) -> None: ...

def action(
    name: str,
    group: str='main',
    callmode: ActionCallModeLiteral | ActionCallMode = ActionCallMode.MANY,
    blockmode: ActionBlockModeLiteral | ActionBlockMode = ActionBlockMode.NONE,
    blocks: Iterable[ActionName | tuple[ActionName, ActionGroup]]=[],
    threaded: bool=False,
) -> Action:
    ...