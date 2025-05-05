import dearpygui.dearpygui as dpg
from typing_extensions import Any, NotRequired, TypedDict
# > Local Imports
from dearfy.base.domnode import DOMNode
from dearfy.typing import Tag, Position
from dearfy.field import field
from dearfy.functions import formatting_kwargs

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
    __node_containerable__ = False
    
    def __init__(
        self,
        *,
        label: str = '',
        user_data: Any | None = None,
        use_internal_label: bool = True,
        tag: Tag | None = None,
        indent: int = -1,
        show: bool = True,
        pos: Position = [],
        **kwargs: object
    ) -> None:
        super().__init__()
        self._app = None
        self._config = {
            'tag': field(tag, 0, nullable=False),
            'label': label,
            'user_data': user_data,
            'use_internal_label': use_internal_label,
            'indent': indent,
            'show': show,
            'pos': pos,
            **kwargs
        }
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}({formatting_kwargs(**self._config)})'
    
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
        pass
    
    def __dearfy_init__(self) -> None:
        pass
    
    def __dearfy_postinit__(self) -> None:
        pass
    
    def get_configuration(self) -> dict[str, Any]:
        configuration = dpg.get_item_configuration()
        return configuration
    
    def configurate(self, **kwargs: object) -> None:
        if self._inited:
            dpg.configure_item(self.tag, **kwargs)
            self._config.update(**kwargs)
    
    def destroy(self) -> None:
        if self._inited:
            dpg.delete_item(self.tag)
            self._inited = False
    
    def show(self) -> None:
        if self._inited:
            dpg.show_item(self.tag)
    
    def hide(self) -> None:
        if self._inited:
            dpg.hide_item(self.tag)