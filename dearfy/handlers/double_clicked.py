import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Unpack
# > Local Imports
from dearfy.typing import Tag
from dearfy.field import field
from dearfy.functions import get_method_needed
from dearfy.base.handler import ItemHandler, ItemHandlerKwargs

# ! Double Clicked Handler Class

class DoubleClickedItemHandler(ItemHandler):
    REFERENCE_METHOD = dpg.add_item_double_clicked_handler

    def __init__(
        self,
        button: int | None = None,
        **kwargs: Unpack[ItemHandlerKwargs]
    ) -> None:
        super().__init__(
            button=field(button, -1, nullable=False),
            **kwargs
        )

    def __dearfy_handler_init__(self, parent: Tag) -> None:
        with dpg.item_handler_registry() as handler:
            kwargs = get_method_needed(dpg.add_item_double_clicked_handler, **self._config)
            kwargs.pop('parent', None)
            self._config['tag'] = dpg.add_item_double_clicked_handler(**kwargs)
        dpg.bind_item_handler_registry(parent, handler)