import dearpygui.dearpygui as dpg
# > Dearfy
from dearfy.field import field
from dearfy.typing import Tag, Color, Callback, Position
from dearfy.base import Item, ItemKwargs
from dearfy.functions import get_method_needed
from dearfy.validator import ValidateKwargsAction
# > Local Imports
from typing_extensions import Unpack

# ! Text Class

class Text(Item):
    REFERENCE_METHOD = dpg.add_text
    VALIDATORS_KWARGS = (ValidateKwargsAction, )

    def __init__(self,
        default_value: str='',
        *,
        indent: int = -1,
        show: bool = True,
        pos: Position | None = None,
        parent: Tag | None = None,
        before: Tag | None = None,
        source: Tag | None = None,
        payload_type: str = '$$DPG_PAYLOAD',
        drag_callback: Callback = None,
        drop_callback: Callback = None,
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
            indent=indent,
            show=show,
            pos=field(pos, default_factory=list, nullable=False),
            default_value=default_value,
            parent=field(parent, 0, nullable=False),
            before=field(before, 0, nullable=False),
            source=field(source, 0, nullable=False),
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
        kwargs = get_method_needed(dpg.add_text, **self._config)
        self._config['tag'] = dpg.add_text(**kwargs)
        super().__dearfy_init__()
