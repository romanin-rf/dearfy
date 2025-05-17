from __future__ import annotations

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

class HandlerKwargs(TypedDict):
    label: NotRequired[str | None]
    user_data: NotRequired[Any | None]
    use_internal_label: NotRequired[bool]
    tag: NotRequired[Tag | None]
    parent: NotRequired[Tag | None]
    callback: NotRequired[Callback | None]
    show: NotRequired[bool]

# ! Handler Base Class

class Handler(DOMNode):
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
    
    def __dearfy_preinit__(self) -> None:
        for vkt in self.VALIDATORS_KWARGS:
            if issubclass(vkt, ValidatorKwargsBase):
                self._config = vkt(item=self, app=self._app).validate(**self._config)
            elif callable(vkt):
                self._config = vkt(self, **self._config)
    
    def __dearfy_init__(self) -> None:
        pass
    
    def __dearfy_postinit__(self) -> None:
        pass
    
    def __dearfy_destroy__(self) -> None:
        self._config['tag'] = 0
    
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