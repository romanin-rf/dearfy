import dearpygui.dearpygui as dpg
# > Dearfy
from dearfy.field import field
from dearfy.typing import Tag, Callback
from dearfy.base import Container, ItemKwargs, Enableable
from dearfy.functions import get_method_needed
from dearfy.validator import ValidateKwargsAction
# > Local Imports
from typing_extensions import Unpack

# ! Group Class

class Group(Container, Enableable):
    REFERENCE_METHOD = dpg.add_group
    VALIDATORS_KWARGS = (ValidateKwargsAction, )

    def __init__(
        self,
        *,
        width: int = 0,
        height: int = 0,
        parent: Tag | None = None,
        before: Tag | None = None,
        payload_type: str = '$$DPG_PAYLOAD',
        drag_callback: Callback | None = None,
        drop_callback: Callback | None = None,
        enabled: bool = True,
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
            parent=field(parent, 0, nullable=False),
            before=field(before, 0, nullable=False),
            payload_type=payload_type,
            drag_callback=drag_callback,
            drop_callback=drop_callback,
            enabled=enabled,
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
        if self.inited:
            return
        if self._node_children:
            kwargs = get_method_needed(dpg.add_group, **self._config)
            with dpg.group(**kwargs) as tag:
                super().__dearfy_init__()
            tag = tag
        else:
            kwargs = get_method_needed(dpg.add_group, **self._config)
            tag = dpg.add_group(**kwargs)
        self._config['tag'] = tag

