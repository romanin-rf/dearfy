import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Unpack
# > Local Imports
from dearfy.field import field
from dearfy.functions import get_method_needed
from dearfy.base.handler import Handler, HandlerKwargs

# ! Clicked Handler Class

class ClickedHandler(Handler):
    REFERENCE_METHOD = dpg.add_item_clicked_handler

    def __init__(
        self,
        button: int | None = None,
        **kwargs: Unpack[HandlerKwargs]
    ) -> None:
        super().__init__(
            button=field(button, -1, nullable=False),
            **kwargs
        )

    def __dearfy_postinit__(self) -> None:
        if self._config['parent'] != 0:
            with dpg.item_handler_registry() as handler:
                kwargs = get_method_needed(dpg.add_item_clicked_handler, **self._config)
                self._config['tag'] = dpg.add_item_clicked_handler(**kwargs)
            dpg.bind_item_handler_registry(self._config['parent'], handler)
            return
        elif self._node_parent is not None:
            if hasattr(self._node_parent, 'tag'):
                if self._node_parent.tag != 0:
                    with dpg.item_handler_registry() as handler:
                        kwargs = get_method_needed(dpg.add_item_clicked_handler, **self._config)
                        self._config['tag'] = dpg.add_item_clicked_handler(**kwargs)
                    dpg.bind_item_handler_registry(self._node_parent.tag, handler)
                    return
        raise RuntimeError(f"Fail to initialise {self} because the tag of the parent object could not be found.")