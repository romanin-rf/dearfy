import dearpygui.dearpygui as dpg
from dearfy.typing import Color
from dearfy.base import Item, ItemKwargs
from dearfy.functions import get_method_needed
from typing_extensions import Any, Callable, Unpack

# ! Text Item Class

class Text(Item):
    def __init__(self,
        default_value: str='',
        *,
        parent: int | str = 0,
        before: int | str = 0,
        source: int | str = 0,
        payload_type: str = '$$DPG_PAYLOAD',
        drag_callback: Callable[..., Any] = None,
        drop_callback: Callable[..., Any] = None,
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        wrap: int = -1,
        bullet: bool = False,
        color: Color = (-255, 0, 0, 255),
        show_label: bool = False,
        **kwargs: Unpack[ItemKwargs]
    ) -> None:
        super().__init__(
            default_value=default_value,
            parent=parent,
            before=before,
            source=source,
            payload_type=payload_type,
            drag_callback=drag_callback,
            drop_callback=drop_callback,
            filter_key=filter_key,
            tracked=tracked,
            track_offset=track_offset,
            wrap=wrap,
            bullet=bullet,
            color=color,
            show_label=show_label,
            **kwargs
        )
    
    def __dearfy_init__(self) -> None:
        if self.inited:
            return
        kwargs = get_method_needed(dpg.add_text, **self._config)
        self._config['tag'] = dpg.add_text(**kwargs)
