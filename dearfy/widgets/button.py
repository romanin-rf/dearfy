import dearpygui.dearpygui as dpg
from dearfy.typing import Color, Callback
from dearfy.base import Item, ItemKwargs
from dearfy.functions import get_method_needed
from typing_extensions import Unpack

# ! Button Class

class Button(Item):
    def __init__(
        self,
        *,
        width: int = 0,
        height: int = 0,
        parent: int | str = 0,
        before: int | str = 0,
        payload_type: str = '$$DPG_PAYLOAD',
        callback: Callback | None = None,
        drag_callback: Callback | None = None,
        drop_callback: Callback | None = None,
        enabled: bool = True,
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        small: bool = False,
        arrow: bool = False,
        direction: int = 0,
        repeat: bool = False,
        **kwargs: Unpack[ItemKwargs]
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            parent=parent,
            before=before,
            payload_type=payload_type,
            callback=callback,
            drag_callback=drag_callback,
            drop_callback=drop_callback,
            enabled=enabled,
            filter_key=filter_key,
            tracked=tracked,
            track_offset=track_offset,
            small=small,
            arrow=arrow,
            direction=direction,
            repeat=repeat,
            **kwargs
        )
    
    def __dearfy_init__(self) -> None:
        if self.inited:
            return
        kwargs = get_method_needed(dpg.add_button, **self._config)
        self._config['tag'] = dpg.add_button(**kwargs)