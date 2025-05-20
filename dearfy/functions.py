import time
import ctypes
import inspect
import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Any, Literal, Iterable, Callable, TypeVar
# > Local Imports
from dearfy.typing import Tag

# ! Types

T = TypeVar('T')

# ! String Formatting

def formatting_kwargs(**kwargs: object) -> str:
    return ', '.join(f'{key}={value!r}' for key, value in kwargs.items())

# ! Object Works

def get_method_needed(method: Callable[..., Any], **kwargs: T) -> dict[str, T]:
    if inspect.ismethod(method):
        func = method.__func__
    else:
        func = method
    params, sig = {}, inspect.signature(func)
    for name, param in sig.parameters.items():
        params[name] = param.default if (param.default is not param.empty) else NotImplemented
    new_kwargs, needed = {}, func.__code__.co_varnames
    for key, value in kwargs.items():
        if (key in needed) and (params.get(key, NotImplemented) != value):
            new_kwargs[key] = value
    return new_kwargs

# ! For DearPyGUI Methods

def wait_frames(count: int, *, delay: int=1) -> None:
    for i in range(count):
        dpg.split_frame(delay=delay)

def get_item_size(item: str | int, *, wait: bool=False) -> tuple[float, float]:
    if wait:
        wait_frames(3)
    return float(dpg.get_item_width(item)), float(dpg.get_item_height(item))

def match_item_position(
    item: str | int,
    x_justing: Literal['left', 'center', 'right']='center',
    y_justing: Literal['top', 'center', 'bottom']='center',
    padding: tuple[int, int, int, int] | Iterable[int] = (0, 0, 0, 0),
    *,
    wait: bool=False
) -> tuple[float, float]:
    # * Checking
    assert isinstance(padding, Iterable), TypeError(padding)
    padding = tuple(padding)
    assert len(padding) >= 4, ValueError(padding)
    padding = padding[:4]
    # * Getting
    item_width, item_height = get_item_size(item, wait=wait)
    vp_width, vp_height = dpg.get_viewport_width(), dpg.get_viewport_height()
    if (item_width >= 1) and (item_height >= 1):
        pass
    else:
        if dpg.does_item_exist(item):
            item_width, item_height = get_item_size(item, wait=True)
            match x_justing:
                case 'center':
                    pass
                case 'left':
                    pass
                case 'right':
                    pass
                case _:
                    raise ValueError(f'{x_justing=!r}')
        else:
            raise RuntimeError(f'There is no object with this tag/id: {item!r}')
    return 0., 0.

# ! Low-level Methods

def get_object_by_address(__object_address: int) -> Any:
    return ctypes.cast(__object_address, ctypes.py_object).value

"""Calculates the position of an object relative to the size of the viewport

:param item: Tag or id of DearPyGUI object
:type item: str | int
:param wait: Waiting for the window to be fully prepared, defaults to False
:type wait: bool, optional
:return: Object position
:rtype: tuple[float, float]
"""