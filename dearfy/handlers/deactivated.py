import dearpygui.dearpygui as dpg
# > Local Imports
from dearfy.typing import Tag
from dearfy.functions import get_method_needed
from dearfy.base.handler import ItemHandler

# ! Clicked Handler Class

class DeactivatedItemHandler(ItemHandler):
    REFERENCE_METHOD = dpg.add_item_deactivated_handler

    def __dearfy_handler_init__(self, parent: Tag) -> None:
        with dpg.item_handler_registry() as handler:
            kwargs = get_method_needed(dpg.add_item_deactivated_handler, **self._config)
            kwargs.pop('parent', None)
            self._config['tag'] = dpg.add_item_deactivated_handler(**kwargs)
        dpg.bind_item_handler_registry(parent, handler)

class DeactivatedAfterEditItemHandler(ItemHandler):
    REFERENCE_METHOD = dpg.add_item_deactivated_after_edit_handler

    def __dearfy_handler_init__(self, parent: Tag) -> None:
        with dpg.item_handler_registry() as handler:
            kwargs = get_method_needed(dpg.add_item_deactivated_after_edit_handler, **self._config)
            kwargs.pop('parent', None)
            self._config['tag'] = dpg.add_item_deactivated_after_edit_handler(**kwargs)
        dpg.bind_item_handler_registry(parent, handler)