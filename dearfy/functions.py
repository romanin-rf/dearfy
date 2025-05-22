import ctypes
import inspect
from re import I
import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import Any, Literal, Iterable, Iterator,  Callable, TypeIs, TypeVar
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
    """Waiting for a certain number of frames. Needed to initialise DearPyGUI objects on the fly, before using them.
    
    Recommended value for `count = 3`.

    Args:
        count (int): The number of frames the programme will wait before continuing execution.
        delay (int, optional): Minimum wait in milliseconds. Defaults to 1.
    """
    for i in range(count):
        dpg.split_frame(delay=delay)

def get_item_size(item: Tag, *, wait: bool=False) -> tuple[float, float]:
    """Getting the size of an object with expectation.

    Args:
        item (Tag): The tag or id of the object.
        wait (bool, optional): Whether to use the wait. Defaults to False.

    Returns:
        tuple[float, float]: Size of the object in (width, height)
    """
    if wait:
        wait_frames(3)
    return float(dpg.get_item_width(item)), float(dpg.get_item_height(item))

def match_item_position(
    item: Tag,
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
    """Get any python object, by its address (the address that is printed when the `id(object)` method is called).
    ##### !!! WARNING !!! The method is unsafe and may cause unexpected errors (`RuntimeError`).

    Args:
        __object_address (int): The address that is getted when the `id(object)` method is called.

    Returns:
        Any: Any python object.
    """
    return ctypes.cast(__object_address, ctypes.py_object).value