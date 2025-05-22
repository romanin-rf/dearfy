import dearpygui.dearpygui as dpg
# > Dearfy
from dearfy.field import field
from dearfy.typing import Tag, Callback, Position
from dearfy.base import Item, ItemKwargs, Enableable, Showable
from dearfy.functions import get_method_needed
from dearfy.validator import ValidateKwargsAction
# > Local Imports
from typing_extensions import Unpack

# ! Button Class

class Button(Item, Enableable, Showable):
    REFERENCE_METHOD = dpg.add_button
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
        callback: Callback | None = None,
        drag_callback: Callback | None = None,
        drop_callback: Callback | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: Position | None = None,
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        small: bool = False,
        arrow: bool = False,
        direction: int = 0,
        repeat: bool = False,
        **kwargs: Unpack[ItemKwargs]
    ) -> None:
        """Button item.

        Args:
            indent (int, optional): Overrides 'name' as label. Defaults to -1.
            show (bool, optional): Width of the item. Defaults to True.
            pos (Position | None, optional): Places the item relative to window coordinates, [0,0] is top left. Defaults to None.
            width (int, optional): Width of the item. Defaults to 0.
            height (int, optional): Height of the item. Defaults to 0.
            parent (Tag | None, optional): Parent to add this item to. Defaults to None.
            before (Tag | None, optional): This item will be displayed before the specified item in the parent. Defaults to None.
            payload_type (str, optional): Sender string type must be the same as the target for the target to run the payload_callback. Defaults to '$'.
            callback (Callback | None, optional): Registers a callback. Defaults to None.
            drag_callback (Callback | None, optional): Registers a drag callback for drag and drop. Defaults to None.
            drop_callback (Callback | None, optional): Registers a drop callback for drag and drop. Defaults to None.
            enabled (bool, optional): Turns off functionality of widget and applies the disabled theme. Defaults to True.
            filter_key (str, optional): Used by filter widget. Defaults to ''.
            tracked (bool, optional): Scroll tracking. Defaults to False.
            track_offset (float, optional): 0.0f: top, 0.5f: center, 1.0f: bottom. Defaults to 0.5.
            small (bool, optional): Shrinks the size of the button to the text of the label it contains. Useful for embedding in text. Defaults to False.
            arrow (bool, optional): Displays an arrow in place of the text string. This requires the direction keyword. Defaults to False.
            direction (int, optional): Sets the cardinal direction for the arrow by using constants mvDir_Left, mvDir_Up, mvDir_Down, mvDir_Right, mvDir_None. Defaults to 0.
            repeat (bool, optional): Hold to continuosly repeat the click. Defaults to False.
        """
        super().__init__(
            width=width,
            height=height,
            indent=indent,
            parent=field(parent, 0),
            before=field(before, 0),
            payload_type=payload_type,
            callback=callback,
            drag_callback=drag_callback,
            drop_callback=drop_callback,
            show=show,
            enabled=enabled,
            pos=field(pos, default_factory=list),
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
        kwargs = get_method_needed(dpg.add_button, **self._config)
        self._config['tag'] = dpg.add_button(**kwargs)
        super().__dearfy_init__()