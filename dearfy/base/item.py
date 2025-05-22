from __future__ import annotations

import loguru

import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Any, TypedDict, Callable, ParamSpecKwargs, NotRequired, TypeAlias
# > Local Imports
from dearfy.field import field
from dearfy.base.domnode import DOMNode
from dearfy.typing import Tag
from dearfy.functions import formatting_kwargs, get_method_needed
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
    VALIDATORS_KWARGS: tuple[ValidatorKwargsType, ...] = ()
    REFERENCE_METHOD: Callable[..., Any] | None = None
    
    _node_children: list[Item]

    def __init__(
        self,
        *,
        label: str | None = None,
        user_data: Any | None = None,
        use_internal_label: bool = True,
        tag: Tag | None = None,
        **kwargs: object
    ) -> None:
        super().__init__()
        self._app = None
        self._config = {
            'tag': field(tag, 0, nullable=False),
            'label': label,
            'user_data': user_data,
            'use_internal_label': use_internal_label,
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
        return bool((self._state & 0b0100) >> 2)
    
    def __dearfy_preparing__(self, app: object) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_preparing__({app!r})')
        if bool(self._state & 0b0001):
            return
        self._app = app
        for child in self._node_children:
            child.__dearfy_preparing__(app)
        self._state |= 1
    
    def __dearfy_preinit__(self) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_preinit__()')
        if bool((self._state & 0b0010) >> 1):
            return
        for vkt in self.VALIDATORS_KWARGS:
            if issubclass(vkt, ValidatorKwargsBase):
                self._config = vkt(item=self, app=self._app).validate(**self._config)
            elif callable(vkt):
                self._config = vkt(self, **self._config)
        for child in self._node_children:
            child.__dearfy_preinit__()
        self._state |= (1 << 1)
    
    def __dearfy_init__(self) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_init__()')
        if bool((self._state & 0b0100) >> 2):
            return
        for child in self._node_children:
            child.__dearfy_init__()
        self._state |= (1 << 2)
    
    def __dearfy_postinit__(self) -> None:
        loguru.logger.trace(f'[red]Call[/red]: {self!r}.__dearfy_postinit__()')
        if bool((self._state & 0b1000) >> 3):
            return
        for child in self._node_children:
            child.__dearfy_postinit__()
        self._state |= (1 << 3)
    
    def __dearfy_destroy__(self) -> None:
        self._config['tag'] = 0
        self._state = 0
        for child in self._node_children:
            child.__dearfy_destroy__()
    
    def get_item(self, tag: Tag) -> Item:
        try:
            return self._node_main_parent._get_node_by_attr('tag', tag)
        except AttributeError:
            pass
        raise RuntimeError(
            "There is no Item with this tag.\n"
            "Advance datas:\n"
            f"\t- _node_main_parent={self._node_main_parent!r}\n"
            f"\t- _node_parent={self._node_parent!r}\n"
        )
    
    def _move_item_to(self, parent: Tag) -> None:
        loguru.logger.trace(f'Move {self} to {parent!r}')
        old_parent, new_parent = self._node_parent, self.get_item(parent)
        old_parent._remove_child(self)
        new_parent._add_child(self)
    
    def get_configuration(self) -> dict[str, Any]:
        return dpg.get_item_configuration(self._config['tag'])
    
    def configurate(self, **kwargs: object) -> None:
        if self.inited:
            dpg.configure_item(self.tag, **kwargs)
            self._config.update(**kwargs)
    
    def destroy(self) -> None:
        if self.inited:
            dpg.delete_item(self.tag)
            self._config['tag'] = 0
            self._state = 0
            if self._node_parent is not None:
                self._node_parent._remove_child(self)