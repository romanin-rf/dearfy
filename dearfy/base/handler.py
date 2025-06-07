from __future__ import annotations

# > Typing
from typing_extensions import Any, TypedDict, NotRequired, Callable, Self, Unpack, ParamSpecKwargs
# > Local Imports
from dearfy.field import field
from dearfy.base.item import Item
from dearfy.base.spetific import Showable
from dearfy.typing import Tag, Callback
from dearfy.validator import ValidatorKwargsBase, ValidateKwargsAction

# ! Typing

class ItemHandlerKwargs(TypedDict):
    tag: NotRequired[Tag | None]
    parent: NotRequired[Tag | None]
    callback: NotRequired[Callback | None]
    show: NotRequired[bool]

# ! Handler Base Class

class ItemHandler(Item, Showable):
    NODE_CONTAINERABLE: bool = False

    REFERENCE_METHOD: Callable[..., Any] | None = None

    VALIDATORS_KWARGS: tuple[type[ValidatorKwargsBase] | Callable[[Self, ParamSpecKwargs], dict[str, Any]], ...] = (ValidateKwargsAction, )

    def __init__(
        self,
        *,
        parent: Tag | None = None,
        callback: Callback | None = None,
        show: bool = True,
        **kwargs: Unpack[ItemHandlerKwargs]
    ) -> None:
        super().__init__(
            parent=field(parent, 0, nullable=False),
            callback=callback,
            show=show,
            **kwargs
        )
    
    @property
    def inited(self) -> bool:
        return bool((self._state & 0b1000) >> 3)
    
    def __dearfy_postinit__(self) -> None:
        if self._config.get('parent', 0) != 0:
            self._move_item_to(self._config['parent'])
        if getattr(self._node_parent, 'tag', 0) != 0:
            parent: Tag = self._node_parent.tag
            self.__dearfy_handler_init__(parent)
            self._config['parent'] = parent
        else:
            raise RuntimeError(f"Fail to initialise {self} because the tag of the parent object could not be found.")
        super().__dearfy_postinit__()
    
    def __dearfy_handler_init__(self, parent: Tag) -> None:
        pass
    
    def __dearfy_destroy__(self) -> None:
        self._config['parent'] = 0
        super().__dearfy_destroy__()