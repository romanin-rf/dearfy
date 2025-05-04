from collections import deque
from types import TracebackType
from rich.tree import Tree
from typing_extensions import Iterator, Self, Generic, TypeVar, ClassVar

# ! Type Vars

T = TypeVar('T')

# ! DOM Node Class

class DOMNode(Generic[T]):
    __node_containerable__: ClassVar[bool]

    _nodes: ClassVar[deque[DOMNode[T] | T]]

    _node_parent: DOMNode[T] | T | None
    _node_children: list[DOMNode[T] | T]

    def __init__(self) -> None: ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    
    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None: ...
    
    @property
    def node_uuid(self) -> str: ...
    
    @property
    def _current_node(self) -> 'DOMNode[T]' | T | None: ...
    
    def _add_child(self, __child: 'DOMNode[T]' | T, /) -> None: ...
    
    def _to_rich_tree(self) -> Tree: ...
    
    def _build_rich_tree_recursive(self, node: 'DOMNode[T]' | T, parent_tree: Tree) -> None: ...
    
    def compose(self) -> Iterator['DOMNode[T]' | T]:
        yield from ()