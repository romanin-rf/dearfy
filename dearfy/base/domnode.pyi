from rich.tree import Tree
from collections import deque
# > Typing
from types import TracebackType
from typing_extensions import Any, Iterator, Self, TypeVar, ClassVar

# ! Type Vars

T = TypeVar('T')

# ! DOM Node Class

class DOMNode:
    NODE_CONTAINERABLE: ClassVar[bool]
    """Is the node a container."""
    NODE_CONTAINER_FOR: tuple[type, ...] | None = None
    """Types or types inherited from these types that the object can containerise."""
    
    _nodes: ClassVar[deque[DOMNode]]
    _node_parent: DOMNode | None
    _node_children: list[DOMNode]

    def __init__(self) -> None: ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    
    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None: ...
    
    @property
    def node_uuid(self) -> str: ...
    
    @property
    def _current_node(self) -> DOMNode | None: ...
    @property
    def _node_main_parent(self) -> DOMNode: ...
    
    def _add_child(self, __child: DOMNode, /) -> None: ...
    def _remove_child(self, __child: DOMNode, /) -> None: ...
    def _get_by_attr(self, __attr_name: str, __attr_value: Any, /) -> DOMNode: ...
    
    def _to_rich_tree(self) -> Tree: ...
    
    def _build_rich_tree_recursive(self, node: DOMNode, parent_tree: Tree) -> None: ...
    
    def compose(self) -> Iterator[DOMNode]: ...