
# > Typing
from typing_extensions import Unpack

# > Local Imports
from dearfy.base.item import Item, ItemKwargs

# ! Container Base Class

class Container(Item):
    """Base class describing the object to be сontainerable."""

    _node_children: list[Item]
    
    def __init__(self, **kwargs: Unpack[ItemKwargs]) -> None: ...
    
    def __dearfy_preparing__(self, app: object) -> None: ...
    def __dearfy_preinit__(self) -> None: ...
    def __dearfy_init__(self) -> None: ...
    def __dearfy_postinit__(self) -> None: ...
    def __dearfy_destroy__(self) -> None: ...