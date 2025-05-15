from rich.tree import Tree
from collections import deque
# > Typing
from types import TracebackType
from typing_extensions import Iterator, Self

# ! DOM Node Class

class DOMNode:
    NODE_CONTAINERABLE: bool = True
    NODE_CONTAINER_FOR: tuple[type, ...] | None = None

    _nodes: deque['DOMNode'] = deque()

    def __init__(self) -> None:
        self._node_children: list[DOMNode] = []
        self._node_parent: DOMNode | None = None
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __enter__(self) -> Self:
        if not self.NODE_CONTAINERABLE:
            raise NotImplementedError('This object type is not a container.')
        if self._nodes:
            self._nodes[-1]._add_child(self)
        self._nodes.append(self)
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        if not self.NODE_CONTAINERABLE:
            raise NotImplementedError('This object type is not a container.')
        if self._nodes:
            self._nodes.pop()
    
    @property
    def _current_node(self):
        return self._nodes[-1] if self._nodes else None
    
    def _add_child(self, __child: 'DOMNode', /) -> None:
        if not self.NODE_CONTAINERABLE:
            raise NotImplementedError('This object type is not a container.')
        if self.NODE_CONTAINER_FOR is not None:
            if not (isinstance(__child, self.NODE_CONTAINER_FOR) or issubclass(type(__child), self.NODE_CONTAINER_FOR)):
                raise NotImplementedError(
                    f"This node cannot containerise an object type: {__child.__class__.__qualname__!r}. "
                    "Only allowed (inherited from these types are not specified here, but they are allowed): "
                    f"{', '.join([repr(t.__qualname__) for t in self.NODE_CONTAINER_FOR])}."
                )
        __child._node_parent = self
        self._node_children.append(__child)
    
    def _remove_child(self, __child: 'DOMNode', /) -> None:
        if __child in self._node_children:
            __child._node_parent = None
            self._node_children.remove(__child)
    
    def _to_rich_tree(self) -> Tree:
        tree = Tree(repr(self), highlight=True)
        self._build_rich_tree_recursive(self, tree)
        return tree
    
    def _build_rich_tree_recursive(self, node: 'DOMNode', parent_tree: Tree) -> None:
        for child in node._node_children:
            branch = parent_tree.add(repr(child))
            self._build_rich_tree_recursive(child, branch)
    
    def compose(self) -> Iterator['DOMNode']:
        yield from ()