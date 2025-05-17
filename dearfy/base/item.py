from __future__ import annotations

import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Any, TypedDict, Callable, ParamSpecKwargs, NotRequired, TypeAlias
# > Local Imports
from dearfy.field import field
from dearfy.base.domnode import DOMNode
from dearfy.base.handler import Handler
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
    NODE_CONTAINERABLE = True
    NODE_CONTAINER_FOR = (Handler, )
    
    VALIDATORS_KWARGS: tuple[ValidatorKwargsType, ...] = ()
    REFERENCE_METHOD: Callable[..., Any] | None = None
    
    _node_children: list[Item]

    def __init__(
        self,
        *,
        label: str = '',
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
        return self._config['tag'] != 0
    
    def __dearfy_preparing__(self, app: object) -> None:
        self._app = app
        for child in self._node_children:
            child.__dearfy_preparing__(app)
    
    def __dearfy_preinit__(self) -> None:
        for vkt in self.VALIDATORS_KWARGS:
            if issubclass(vkt, ValidatorKwargsBase):
                self._config = vkt(item=self, app=self._app).validate(**self._config)
            elif callable(vkt):
                self._config = vkt(self, **self._config)
        for child in self._node_children:
            child.__dearfy_preinit__()
    
    def __dearfy_init__(self) -> None:
        for child in self._node_children:
            child.__dearfy_init__()
    
    def __dearfy_postinit__(self) -> None:
        for child in self._node_children:
            child.__dearfy_postinit__()
    
    def __dearfy_destroy__(self) -> None:
        self._config['tag'] = 0
        for child in self._node_children:
            child.__dearfy_destroy__()
    
    def get_item(self, tag: Tag, *, by_main: bool=False) -> Item:
        if self.inited:
            try:
                if by_main:
                    return self._node_main_parent._get_by_attr('tag', tag)
                else:
                    return self._get_by_attr('tag', tag)
            except AttributeError:
                pass
        raise RuntimeError('There is no Item with this tag.')
    
    def get_configuration(self) -> dict[str, Any]:
        configuration = dpg.get_item_configuration()
        return configuration
    
    def configurate(self, **kwargs: object) -> None:
        if self.inited:
            dpg.configure_item(self.tag, **kwargs)
            self._config.update(**kwargs)
    
    def destroy(self) -> None:
        if self.inited:
            dpg.delete_item(self.tag)
            self._config['tag'] = 0
            if self._node_parent is not None:
                self._node_parent._remove_child(self)
    
    def show(self) -> None:
        if self.inited:
            dpg.show_item(self.tag)
    
    def hide(self) -> None:
        if self.inited:
            dpg.hide_item(self.tag)