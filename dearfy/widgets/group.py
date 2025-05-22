import dearpygui.dearpygui as dpg
# > Dearfy
from dearfy.field import field
from dearfy.typing import Tag, Callback, Position
from dearfy.base import Item, ItemKwargs, Enableable, Showable
from dearfy.functions import get_method_needed
from dearfy.validator import ValidateKwargsAction
# > Local Imports
from typing_extensions import Unpack

# ! Group Class

class Group(Item, Enableable, Showable):
    REFERENCE_METHOD = dpg.add_group
    VALIDATORS_KWARGS = (ValidateKwargsAction, )

    def __init__(
        self,
        *,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        parent: Tag | None = None,
        before: Tag | None = None,
        payload_type: str = '$$DPG_PAYLOAD',
        drag_callback: Callback | None = None,
        drop_callback: Callback | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: Position | None = None,
        filter_key: str = '',
        delay_search: bool = False,
        tracked: bool = False,
        track_offset: float = 0.5,
        horizontal: bool = False,
        horizontal_spacing: float = -1,
        xoffset: float = 0,
        **kwargs: Unpack[ItemKwargs]
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            indent=indent,
            parent=field(parent, 0),
            before=field(before, 0),
            payload_type=payload_type,
            drag_callback=drag_callback,
            drop_callback=drop_callback,
            show=show,
            enabled=enabled,
            pos=field(pos, default_factory=list),
            filter_key=filter_key,
            delay_search=delay_search,
            tracked=tracked,
            track_offset=track_offset,
            horizontal=horizontal,
            horizontal_spacing=horizontal_spacing,
            xoffset=xoffset,
            **kwargs
        )
    
    def __dearfy_init__(self) -> None:
        if self._node_children:
            kwargs = get_method_needed(dpg.add_group, **self._config)
            with dpg.group(**kwargs) as tag:
                super().__dearfy_init__()
            tag = tag
        else:
            kwargs = get_method_needed(dpg.add_group, **self._config)
            tag = dpg.add_group(**kwargs)
        self._config['tag'] = tag

