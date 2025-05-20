from __future__ import annotations

import loguru

import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Any, TypedDict, NotRequired, Callable, Self, ParamSpecKwargs
# > Local Imports
from dearfy.field import field
from dearfy.base.domnode import DOMNode
from dearfy.typing import Tag, Callback
from dearfy.functions import formatting_kwargs, get_method_needed
from dearfy.validator import ValidatorKwargsBase, ValidateKwargsAction

# ! Typing

class ItemHandlerKwargs(TypedDict):
    label: NotRequired[str | None]
    user_data: NotRequired[Any | None]
    use_internal_label: NotRequired[bool]
    tag: NotRequired[Tag | None]
    parent: NotRequired[Tag | None]
    callback: NotRequired[Callback | None]
    show: NotRequired[bool]

# ! Handler Base Class

class ItemHandler(DOMNode):
    NODE_CONTAINERABLE: bool = False

    REFERENCE_METHOD: Callable[..., Any] | None = None

    VALIDATORS_KWARGS: tuple[type[ValidatorKwargsBase] | Callable[[Self, ParamSpecKwargs], dict[str, Any]], ...] = (ValidateKwargsAction, )

    def __init__(
        self,
        *,
        label: str | None = None,
        user_data: Any | None = None,
        use_internal_label: bool = True,
        tag: Tag | None = None,
        parent: Tag | None = None,
        callback: Callback | None = None,
        show: bool = True,
        **kwargs: object
    ) -> None:
        super().__init__()
        self._app = None
        self._config = {
            'tag': field(tag, 0, nullable=False),
            'label': label,
            'user_data': user_data,
            'use_internal_label': use_internal_label,
            'parent': field(parent, 0, nullable=False),
            'callback': callback,
            'show': show,
            **kwargs
        }
        self._state = 0
    
    def __str__(self) -> str:
        if self.REFERENCE_METHOD is not None:
            kwargs = get_method_needed(self.REFERENCE_METHOD, **self._config)
        else:
            kwargs = self._config
        return f'{self.__class__.__name__}({formatting_kwargs(**kwargs)})'
    
    @property
    def tag(self) -> Tag:
        return self._config['tag']
    
    @property
    def app(self) -> object | None:
        return self._app
    
    @property
    def inited(self) -> bool:
        return bool((self._state & 0b1000) >> 3)
    
    def __dearfy_preparing__(self, app: object) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_preparing__({app!r})')
        self._app = app
        self._state |= 1
    
    def __dearfy_preinit__(self) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_preinit__()')
        for vkt in self.VALIDATORS_KWARGS:
            if issubclass(vkt, ValidatorKwargsBase):
                self._config = vkt(item=self, app=self._app).validate(**self._config)
            elif callable(vkt):
                self._config = vkt(self, **self._config)
        self._state |= (1 << 1)
    
    def __dearfy_init__(self) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_init__()')
        if self._config['parent'] != 0:
            self._move_item_to(self._config['parent'])
        self._state |= (1 << 2)
    
    def __dearfy_postinit__(self) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_postinit__()')
        if getattr(self._node_parent, 'tag', 0) != 0:
            parent: Tag = self._node_parent.tag
            self.__dearfy_handler_init__(parent)
            self._config['parent'] = parent
        else:
            raise RuntimeError(f"Fail to initialise {self} because the tag of the parent object could not be found.")
        self._state |= (1 << 2)
    
    def __dearfy_handler_init__(self, parent: Tag) -> None:
        pass
    
    def __dearfy_destroy__(self) -> None:
        self._config['tag'] = 0
        self._config['parent'] = 0
        self._state = 0
    
    def get_item(self, tag: Tag, *, by_main: bool=False):
        try:
            node = self._node_main_parent if by_main else self
            return node._get_node_by_attr('tag', tag)
        except AttributeError:
            pass
        raise RuntimeError('There is no Item with this tag.')
    
    def _move_item_to(self, parent: Tag) -> None:
        new_parent = self.get_item(parent, by_main=True)
        self._node_parent._remove_child(self)
        new_parent._add_child(self)
    
    def get_configuration(self) -> dict[str, Any]:
        configuration = dpg.get_item_configuration()
        return configuration
    
    def configurate(self, **kwargs: object) -> None:
        if self.inited:
            dpg.configure_item(self.tag, **kwargs)
            self._config.update(**kwargs)
    
    def show(self) -> None:
        if self.inited:
            dpg.show_item(self.tag)
    
    def hide(self) -> None:
        if self.inited:
            dpg.hide_item(self.tag)