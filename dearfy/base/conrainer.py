from dearfy.base.item import Item

# ! Container Base Class

class Container(Item):
    NODE_CONTAINERABLE = True
    NODE_CONTAINER_FOR = None

    _node_children: list[Item]
