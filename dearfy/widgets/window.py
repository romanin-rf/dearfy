import dearpygui.dearpygui as dpg
from dearfy.functions import get_method_needed
from dearfy.base import Container, ItemKwargs
from dearfy.typing import Size, Callback
from typing_extensions import Unpack

# ! Window Class

class Window(Container):
    def __init__(
        self,
        *,
        width: int = 0,
        height: int = 0,
        delay_search: bool = False,
        min_size: Size = [100, 100],
        max_size: Size = [30000, 30000],
        menubar: bool = False,
        collapsed: bool = False,
        autosize: bool = False,
        no_resize: bool = False,
        unsaved_document: bool = False,
        no_title_bar: bool = False,
        no_move: bool = False,
        no_scrollbar: bool = False,
        no_collapse: bool = False,
        horizontal_scrollbar: bool = False,
        no_focus_on_appearing: bool = False,
        no_bring_to_front_on_focus: bool = False,
        no_close: bool = False,
        no_background: bool = False,
        modal: bool = False,
        popup: bool = False,
        no_saved_settings: bool = False,
        no_open_over_existing_popup: bool = True,
        no_scroll_with_mouse: bool = False,
        on_close: Callback | None = None,
        **kwargs: Unpack[ItemKwargs]
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            delay_search=delay_search,
            min_size=min_size,
            max_size=max_size,
            menubar=menubar,
            collapsed=collapsed,
            autosize=autosize,
            no_resize=no_resize,
            unsaved_document=unsaved_document,
            no_title_bar=no_title_bar,
            no_move=no_move,
            no_scrollbar=no_scrollbar,
            no_collapse=no_collapse,
            horizontal_scrollbar=horizontal_scrollbar,
            no_focus_on_appearing=no_focus_on_appearing,
            no_bring_to_front_on_focus=no_bring_to_front_on_focus,
            no_close=no_close,
            no_background=no_background,
            modal=modal,
            popup=popup,
            no_saved_settings=no_saved_settings,
            no_open_over_existing_popup=no_open_over_existing_popup,
            no_scroll_with_mouse=no_scroll_with_mouse,
            on_close=on_close,
            **kwargs
        )
    
    def __dearfy_init__(self) -> None:
        if self.inited:
            return
        if self._node_children:
            kwargs = get_method_needed(dpg.add_window, **self._config)
            with dpg.window(**kwargs) as tag:
                super().__dearfy_init__()
            tag = tag
        else:
            kwargs = get_method_needed(dpg.add_window, **self._config)
            tag = dpg.add_window(**kwargs)
        self._config['tag'] = tag