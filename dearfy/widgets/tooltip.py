import dearpygui.dearpygui as dpg
import loguru
# > Dearfy
from dearfy.field import field
from dearfy.typing import Tag
from dearfy.base import Item, ItemKwargs, Showable
from dearfy.functions import get_method_needed
from dearfy.validator import ValidateKwargsAction
# > Local Imports
from typing_extensions import Unpack

# ! Text Class

class Tooltip(Item, Showable):
    REFERENCE_METHOD = dpg.add_tooltip
    VALIDATORS_KWARGS = (ValidateKwargsAction, )

    def __init__(self,
        *,
        parent: Tag | None = None,
        show: bool = True,
        delay: float | None = None,
        hide_on_activity: bool = False,
        **kwargs: Unpack[ItemKwargs]
    ) -> None:
        super().__init__(
            parent=field(parent, 0),
            show=show,
            delay=field(delay, 0.0),
            hide_on_activity=hide_on_activity,
            **kwargs
        )
    
    @property
    def inited(self) -> bool:
        return bool((self._state & 0b1000) >> 3)
    
    def __dearfy_init__(self) -> None:
        if self._config.get('parent', 0) != 0:
            self._move_item_to(self._config['parent'])
        elif getattr(self._node_parent, 'tag', 0) != 0:
            self._config['parent'] = self._node_parent.tag
        else:
            raise RuntimeError('The parent object to which the object should have been bound is not initialised or is not specified.')
    
    def __dearfy_postinit__(self) -> None:
        kwargs = get_method_needed(dpg.add_tooltip, **self._config)
        if self._node_children:
            with dpg.tooltip(**kwargs) as tooltip:
                super().__dearfy_init__()
                super().__dearfy_postinit__()
            self._config['tag'] = tooltip
        else:
            self._config['tag'] = dpg.add_tooltip(**kwargs)
            super().__dearfy_init__()
            super().__dearfy_postinit__()
    
    def __dearfy_destroy__(self) -> None:
        self._config['parent'] = 0
        super().__dearfy_destroy__()