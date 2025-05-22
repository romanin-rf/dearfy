from __future__ import annotations

# > Typing
from typing_extensions import Literal, Callable, overload, TypeVar

# ! Type Vars

VT = TypeVar('VT')
DT = TypeVar('DT')
WT = TypeVar('WT')

# ! Field Function Overloads

@overload
def field(value: VT | None) -> VT: ...

@overload
def field(value: VT | None, default: DT, *, nullable: Literal[False] = False) -> VT | DT: ...
@overload
def field(value: VT | None, *, default_factory: Callable[[], DT], nullable: Literal[False] = False) -> VT | DT: ...

@overload
def field(value: VT | None, default: DT, *, nullable: Literal[True]) -> VT | DT | None: ...
@overload
def field(value: VT | None, *, default_factory: Callable[[], DT], nullable: Literal[True]) -> VT | DT | None: ...

@overload
def field(
    value: VT | None,
    default: DT,
    *,
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[False] = False,
    nullable: Literal[False] = False
) -> WT | DT: ...
@overload
def field(
    value: VT | None,
    *,
    default_factory: Callable[[], DT],
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[False] = False,
    nullable: Literal[False] = False
) -> WT | DT: ...

@overload
def field(
    value: VT | None,
    default: DT,
    *,
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[True],
    nullable: Literal[False] = False
) -> WT: ...
@overload
def field(
    value: VT | None,
    *,
    default_factory: Callable[[], DT],
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[True],
    nullable: Literal[False] = False
) -> WT: ...

@overload
def field(
    value: VT | None,
    default: DT,
    *,
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[False] = False,
    nullable: Literal[True]
) -> WT | DT | None: ...
@overload
def field(
    value: VT | None,
    *,
    default_factory: Callable[[], DT],
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[False] = False,
    nullable: Literal[True]
) -> WT | DT | None: ...

@overload
def field(
    value: VT | None,
    default: DT,
    *,
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[True],
    nullable: Literal[True]
) -> WT | None: ...
@overload
def field(
    value: VT | None,
    *,
    default_factory: Callable[[], DT],
    wrap: Callable[[VT | None], WT],
    default_wrapped: Literal[True],
    nullable: Literal[True]
) -> WT | None: ...

# ! Field Function

def field(
    value: VT | None,
    default: DT = None,
    default_factory: Callable[[], DT] | None = None,
    default_wrapped: bool = False,
    wrap: Callable[[VT | None], WT] | None = None,
    nullable: bool = False
) -> VT | DT | WT | None:
    """
    Checks a value and returns it in its original or transformed form, or returns the default value.
    
    Args:
        value: Original value
        default: Default value if value is `None`
        default_factory: Callable that returns default value when needed
        default_wrapped: Should default value be wrapped if wrap is provided
        wrap: Function to convert value
        nullable: Is `None` allowed as a valid value
    
    Returns:
        The checked value (possibly converted) or the default value
    
    Raises:
        ValueError: If the value is None but not nullable and there is no default
        AssertionError: If the `default` and `default_factory` arguments are specified at the same time
    """
    
    assert not ((default is not None) and (default_factory is not None)), "You cannot specify \'default\' and \'default_factory\' at the same time."
    if value is None:
        if default is not None:
            if (wrap is not None) and default_wrapped:
                return wrap(default)
            return default
        if default_factory is not None:
            default_value = default_factory()
            if (wrap is not None) and default_wrapped:
                return wrap(default_value)
            return default_value
        if nullable:
            return None
        raise ValueError("Value cannot be None")
    
    if wrap is not None:
        return wrap(value)
    return value