from dearfy.base.item import Item, ItemKwargs
# > Local Imports
from typing_extensions import Unpack

# ! Container Base Class

class Container(Item):
    _node_children: list[Item]

    __node_containerable__ = True

    def __init__(self, **kwargs: Unpack[ItemKwargs] | object) -> None: # type: ignore
        super().__init__(**kwargs)
    
    def __dearfy_preparing__(self, app: object) -> None:
        self._app = app
        for child in self._node_children:
            child.__dearfy_preparing__(app)
    
    def __dearfy_preinit__(self) -> None:
        for child in self._node_children:
            child.__dearfy_preinit__()
    
    def __dearfy_init__(self) -> None:
        for child in self._node_children:
            child.__dearfy_init__()
    
    def __dearfy_postinit__(self) -> None:
        for child in self._node_children:
            child.__dearfy_postinit__()