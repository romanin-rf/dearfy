
# > Typing
from typing_extensions import TypeAlias, Iterable, Iterator, ClassVar
# > Local Imports
from dearfy.base import Item, DOMNode
from dearfy.typing import Color, FilePath, Tag
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
    """Base class for describing an application."""

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
        """Base class for describing an application.

        Args:
            title (str, optional): Sets the title of the viewport. Defaults to 'Dearfy Viewport'.
            small_icon (FilePath | None, optional): Sets the small icon that is found in the viewport's decorator bar. Must be \*.ico on Windows and either \*.ico or \*.png on Mac. Defaults to None.
            large_icon (FilePath | None, optional): Sets the large icon that is found in the task bar while the app is running. Must be \*.ico on Windows and either \*.ico or \*.png on Mac. Defaults to None.
            width (int, optional): Sets the width of the drawable space on the viewport. Defaults to 1280.
            height (int, optional): Sets the height of the drawable space on the viewport. Defaults to 800.
            x_pos (int, optional): Sets X position the viewport will be drawn in screen coordinates. Defaults to 100.
            y_pos (int, optional): Sets Y position the viewport will be drawn in screen coordinates. Defaults to 100.
            min_width (int, optional): Applies a minimuim limit to the width of the viewport. Defaults to 250.
            max_width (int, optional): Applies a maximum limit to the width of the viewport. Defaults to 10000.
            min_height (int, optional): Applies a minimuim limit to the height of the viewport. Defaults to 250.
            max_height (int, optional): Applies a maximum limit to the height of the viewport. Defaults to 10000.
            resizable (bool, optional): Enables and Disables user ability to resize the viewport. Defaults to True.
            vsync (bool, optional): Enables and Disables the renderloop vsync limit. Vsync frame value is set by refresh rate of display. Defaults to True.
            always_on_top (bool, optional): Forces the viewport to always be drawn ontop of all other viewports. Defaults to False.
            decorated (bool, optional): Enabled and disabled the decorator bar at the top of the viewport. Defaults to True.
            clear_color (Color, optional): Sets the color of the back of the viewport. Defaults to (0, 0, 0, 255).
            disable_close (bool, optional): Disables the viewport close button. Can be used with set_exit_callback. Defaults to False.
            minimized (bool, optional): Sets the state of the viewport to minimized. Defaults to False.
            maximized (bool, optional): Sets the state of the viewport to maximized. Defaults to False.
        """
        ...
    
    def compose(self) -> ComposeResult: ...

    def __dearfy_compose__(self) -> None: ...
    def __dearfy_preparing__(self) -> None: ...
    def __dearfy_preinit__(self) -> None: ...
    def __dearfy_init__(self) -> None: ...
    def __dearfy_postinit__(self) -> None: ...

    def get_item(self, tag: Tag, *, by_main: bool=False) -> Item: ...

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