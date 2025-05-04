from dearfy.base.item import Item, ItemKwargs
# > Local Imports
from types import TracebackType
from typing_extensions import Unpack, Self

# ! Container Base Class

class Container(Item):
    __node_containerable__ = True

    def __init__(self, **kwargs: Unpack[ItemKwargs]) -> None:
        super().__init__(**kwargs)
    
    def __dearfy_reinit__(self, app: object) -> None:
        self._app = app
        for child in self._node_children:
            child.__dearfy_reinit__(app)
    
    def __dearfy_init__(self) -> None:
        for child in self._node_children:
            child.__dearfy_init__()