from collections import deque
# > Typing
from typing_extensions import Any, TypedDict, NotRequired, Callable, ParamSpecKwargs, ClassVar, TypeAlias
# > Local Imports
from dearfy.app import App
from dearfy.base.handler import ItemHandler
from dearfy.base.domnode import DOMNode
from dearfy.typing import Tag
from dearfy.validator import ValidatorKwargsBase

# ! Typing

ValidatorKwargsType: TypeAlias = type[ValidatorKwargsBase] | Callable[['Item', ParamSpecKwargs], dict[str, Any]]

class ItemKwargs(TypedDict):
    label: NotRequired[str]
    user_data: NotRequired[Any | None]
    use_internal_label: NotRequired[bool]
    tag: NotRequired[Tag | None]

# ! Base Widget Class

class Item(DOMNode):
    """Base class describing the element."""

    VALIDATORS_KWARGS: ClassVar[tuple[ValidatorKwargsType, ...]]
    """Iterable of validators for element settings."""
    REFERENCE_METHOD: Callable[..., Any] | None
    """A method whose arguments will be considered as default arguments."""

    _nodes: ClassVar[deque[App | Item | DOMNode]]

    _node_parent: App | Item | DOMNode
    _node_children: list[Item | ItemHandler]
    _app: App | None
    _config: dict[str, Any]
    _state: int

    def __init__(
        self,
        *,
        label: str='',
        user_data: Any | None = None,
        use_internal_label: bool = True,
        tag: Tag | None = None,
        **kwargs: object
    ) -> None:
        """Base class describing the element.

        Args:
            label (str, optional): Overrides 'name' as label. Defaults to ''.
            user_data (Any | None, optional): User data for callbacks. Defaults to None.
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends #### uuid). Defaults to True.
            tag (Tag | None, optional): Unique id used to programmatically refer to the item. If label is unused this will be the label. Defaults to None.
            indent (int, optional): Offsets the widget to the right the specified number multiplied by the indent style. Defaults to -1.
            show (bool, optional): Attempt to render widget. Defaults to True.
            pos (Position, optional): Places the item relative to window coordinates. Defaults to [].
        """
        ...

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
    def __dearfy_destroy__(self) -> None: ...

    def _move_item_to(self, parent: Tag) -> None: ...
    def get_item(self, tag: Tag, *, by_main: bool=False) -> Item: ...

    def get_configuration(self) -> dict[str, Any]: ...
    def configurate(self, **kwargs: object) -> None: ...

    def destroy(self) -> None: ...
    def show(self) -> None: ...
    def hide(self) -> None: ...