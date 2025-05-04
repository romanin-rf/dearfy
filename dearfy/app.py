import dearpygui.dearpygui as dpg
from dearfy.base import Item, DOMNode
from dearfy.typing import Color

from rich.console import Console

# ! Variables

console = Console()

# ! App Base Class

class App(DOMNode[Item]):
    def __init__(
        self,
        title: str = 'Dearfy Viewport',
        small_icon: str = '',
        large_icon: str = '',
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
                'small_icon': small_icon,
                'large_icon': large_icon,
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
        pass
    
    def __dearfy_init__(self) -> None:
        for child in self._node_children:
            child.__dearfy_init__()
    
    def __dearfy_postinit__(self) -> None:
        pass

    def run(self) -> None:
        self.__dearfy_preinit__()
        dpg.create_context()
        dpg.create_viewport(**(self._gkwagrs['create_viewport']))
        self.__dearfy_preparing__()
        self.__dearfy_init__()
        self.__dearfy_postinit__()
        dpg.setup_dearpygui()
        dpg.show_viewport(**(self._gkwagrs['show_viewport']))
        console.print(self._to_rich_tree())
        dpg.start_dearpygui()
        dpg.destroy_context()
