import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import TypeAlias, Iterator
# > Local Imports
from dearfy.base import Item, DOMNode
from dearfy.typing import Color, FilePath
from dearfy.field import field
from dearfy.action import Actioner
from dearfy.functions import formatting_kwargs

from rich.console import Console

# ! Variables

console = Console()

# ! Types

ComposeResult: TypeAlias = Iterator[Item]

# ! App Base Class

class App(DOMNode):
    _node_children: list[Item]
    _actioner: Actioner = Actioner()

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
        super().__init__()
        self._gkwagrs = {
            'create_viewport': {
                'title': title,
                'small_icon': field(small_icon, '', nullable=False),
                'large_icon': field(large_icon, '', nullable=False),
                'width': width,
                'height': height,
                'x_pos': x_pos,
                'y_pos': y_pos,
                'min_width': min_width,
                'max_width': max_width,
                'min_height': min_height,
                'max_height': max_height,
                'resizable': resizable,
                'vsync': vsync,
                'always_on_top': always_on_top,
                'decorated': decorated,
                'clear_color': clear_color,
                'disable_close': disable_close,
            },
            'show_viewport': {
                'minimized': minimized,
                'maximized': maximized,
            }
        }
        self.__dearfy_compose__()
        self._nodes.clear()
    
    def __str__(self) -> str:
        kwargs = {}
        for item_kwargs in self._gkwagrs.values():
            kwargs.update(item_kwargs)
        return f'{self.__class__.__name__}({formatting_kwargs(**kwargs)})'

    def __dearfy_compose__(self) -> None:
        self._nodes.append(self)
        for child in self.compose():
            if self._current_node:
                self._current_node._add_child(child)
        self._nodes.clear()
    
    def __dearfy_preparing__(self) -> None:
        for child in self._node_children:
            child.__dearfy_preparing__(self)

    def __dearfy_preinit__(self) -> None:
        for child in self._node_children:
            child.__dearfy_preinit__()
    
    def __dearfy_init__(self) -> None:
        for child in self._node_children:
            child.__dearfy_init__()
    
    def __dearfy_postinit__(self) -> None:
        for child in self._node_children:
            child.__dearfy_postinit__()

    def run(self) -> None:
        self.__dearfy_preparing__()
        dpg.create_context()
        dpg.create_viewport(**(self._gkwagrs['create_viewport']))
        self.__dearfy_preinit__()
        self.__dearfy_init__()
        self.__dearfy_postinit__()
        dpg.setup_dearpygui()
        dpg.show_viewport(**(self._gkwagrs['show_viewport']))
        console.print(self._to_rich_tree())
        dpg.start_dearpygui()
        dpg.destroy_context()

action = App._actioner.action