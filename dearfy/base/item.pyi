from collections import deque
from typing_extensions import Any, TypedDict, NotRequired, Callable, ParamSpecKwargs, ClassVar
# > Local Imports
from dearfy.app import App
from dearfy.base.domnode import DOMNode
from dearfy.typing import Tag, Position
from dearfy.validator import ValidatorKwargsBase

# ! Typing

class ItemKwargs(TypedDict):
    label: NotRequired[str]
    user_data: NotRequired[Any | None]
    use_internal_label: NotRequired[bool]
    tag: NotRequired[Tag | None]
    indent: NotRequired[int]
    show: NotRequired[bool]
    pos: NotRequired[Position]

# ! Base Widget Class

class Item(DOMNode):
    VALIDATORS_KWARGS: ClassVar[tuple[type[ValidatorKwargsBase] | Callable[['Item', ParamSpecKwargs[object]], Any], ...]]

    _nodes: ClassVar[deque[App | Item | DOMNode]]

    _node_parent: App | Item | DOMNode
    _node_children: list
    _app: App | None
    _config: dict[str, Any]

    def __init__(
        self,
        *,
        label: str='',
        user_data: Any | None = None,
        use_internal_label: bool = True,
        tag: Tag | None = None,
        indent: int = -1,
        show: bool = True,
        pos: Position = [],
        **kwargs: object
    ) -> None: ...

    @property
    def tag(self) -> Tag: ...

    @property
    def app(self) -> App | None: ...

    @property
    def inited(self) -> bool: ...

    def __dearfy_preparing__(self, app: App) -> None: ...
    def __dearfy_preinit__(self) -> None: ...
    def __dearfy_init__(self) -> None: ...
    def __dearfy_postinit__(self) -> None: ...

    def get_configuration(self) -> dict[str, Any]: ...
    def configurate(self, **kwargs: object) -> None: ...

    def destroy(self) -> None: ...
    def show(self) -> None: ...
    def hide(self) -> None: ...