from __future__ import annotations

from rich.tree import Tree
from collections import deque
# > Typing
from types import TracebackType
from typing_extensions import Any, Iterator, Self

# ! DOM Node Class

class DOMNode:
    NODE_CONTAINERABLE: bool = True

    _nodes: deque[DOMNode] = deque()

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
    def _current_node(self) -> DOMNode | None:
        return self._nodes[-1] if self._nodes else None
    
    @property
    def _node_main_parent(self) -> DOMNode:
        if self._node_parent is None:
            return self
        main_parent = self._node_parent
        while main_parent._node_parent is not None:
            main_parent = main_parent._node_parent
        return main_parent
    
    def _add_child(self, __child: DOMNode, /) -> None:
        if not self.NODE_CONTAINERABLE:
            raise NotImplementedError('This object type is not a container.')
        __child._node_parent = self
        self._node_children.append(__child)
    
    def _remove_child(self, __child: DOMNode, /) -> None:
        if __child in self._node_children:
            __child._node_parent = None
            self._node_children.remove(__child)
    
    def _pop_child(self, __index: int=-1, /) -> DOMNode:
        return self._node_children.pop(__index)
    
    def _get_node_by_attr(self, __attr_name: str, __attr_value: Any, /) -> DOMNode:
        if hasattr(self, __attr_name):
            if getattr(self, __attr_name) == __attr_value:
                return self
        for node in self._node_children:
            if hasattr(node, __attr_name):
                if getattr(node, __attr_name) == __attr_value:
                    return node
        for node in self._node_children:
            try:
                return node._get_node_by_attr(__attr_name, __attr_value)
            except AttributeError:
                pass
        raise AttributeError('Node with this attribute value does not exist.')
    
    def _to_rich_tree(self) -> Tree:
        if self.NODE_CONTAINERABLE:
            s = '▼' if self._node_children else '►'
        else:
            s = '•'
        tree = Tree(f"{s} {self!r}", highlight=True)
        self._build_rich_tree_recursive(self, tree)
        return tree
    
    def _build_rich_tree_recursive(self, node: DOMNode, parent_tree: Tree) -> None:
        for child in node._node_children:
            if child.NODE_CONTAINERABLE:
                s = '▼' if child._node_children else '►'
            else:
                s = '•'
            branch = parent_tree.add(f"{s} {child!r}")
            self._build_rich_tree_recursive(child, branch)
    
    def compose(self) -> Iterator[DOMNode]:
        yield from ()