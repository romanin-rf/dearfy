
# > Typing
from typing_extensions import Unpack

# > Local Imports
from dearfy.base.item import Item, ItemKwargs

# ! Container Base Class

class Container(Item):
    NODE_CONTAINERABLE = True
    NODE_CONTAINER_FOR = None

    _node_children: list[Item]

    def __init__(self, **kwargs: Unpack[ItemKwargs]) -> None:
        super().__init__(**kwargs)
