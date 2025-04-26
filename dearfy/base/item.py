from turtle import tiltangle
import dearpygui.dearpygui as dpg
from typing_extensions import Any
# > Local Imports
from dearfy.typing import Tag, Position

# ! Base Widget Class

class Item:
    def __init__(
        self,
        label: str='',
        user_data: Any | None = None,
        use_internal_label: bool = True,
        tag: Tag | None = None,
        indent: int = -1,
        show: bool = True,
        pos: Position = [],
        **kwargs: object
    ) -> None:
        self.__tag: Tag = tag if tag is not None else 0
        self.__config = {
            'label': label,
            'user_data': user_data,
            'use_internal_label': use_internal_label,
            'indent': indent,
            'show': show,
            'pos': pos,
            **kwargs
        }
        self.__inited = False
    
    @property
    def tag(self) -> Tag:
        return self.__tag
    
    def __dearfy_init__(self) -> None:
        raise NotImplementedError
    
    def get_configurations(self) -> dict[str, Any]:
        return self.__config.copy()
    
    def configurate(self, **kwargs: object) -> None:
        if self.__inited:
            dpg.configure_item(self.tag, **kwargs)
            self.__config.update(**kwargs)
    
    def destroy(self) -> None:
        if self.__inited:
            dpg.delete_item(self.__tag)
            self.__inited = False
    
    def show(self) -> None:
        if self.__inited:
            dpg.show_item(self.__tag)

    def hide(self) -> None:
        if self.__inited:
            dpg.hide_item(self.__tag)