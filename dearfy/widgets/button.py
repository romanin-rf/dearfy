import dearpygui.dearpygui as dpg
# > Dearfy
from dearfy.field import field
from dearfy.typing import Tag, Callback
from dearfy.base import Item, ItemKwargs, Enablable
from dearfy.functions import get_method_needed
from dearfy.validator import ValidateKwargsAction
# > Local Imports
from typing_extensions import Unpack

# ! Button Class

class Button(Item, Enablable):
    REFERENCE_METHOD = dpg.add_button
    VALIDATORS_KWARGS = (ValidateKwargsAction, )

    def __init__(
        self,
        *,
        width: int = 0,
        height: int = 0,
        parent: Tag | None = None,
        before: Tag | None = None,
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
            parent=field(parent, 0, nullable=False),
            before=field(before, 0, nullable=False),
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