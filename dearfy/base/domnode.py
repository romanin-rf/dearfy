from rich.tree import Tree
from collections import deque
from types import TracebackType
from typing_extensions import Iterator, Self

# ! DOM Node Class

class DOMNode:
    __node_containerable__: bool = True

    _nodes: deque['DOMNode'] = deque()

    def __init__(self) -> None:
        self._node_children: list[DOMNode] = []
        self._node_parent: DOMNode | None = None
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __enter__(self) -> Self:
        if not self.__node_containerable__:
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
        if not self.__node_containerable__:
            raise NotImplementedError('This object type is not a container.')
        if self._nodes:
            self._nodes.pop()
    
    @property
    def _current_node(self):
        return self._nodes[-1] if self._nodes else None
    
    def _add_child(self, __child: 'DOMNode', /) -> None:
        if not self.__node_containerable__:
            raise NotImplementedError('This object type is not a container.')
        __child._node_parent = self
        self._node_children.append(__child)
    
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