from __future__ import annotations

# > Typing
from typing_extensions import Any, Literal, Callable, overload, TypeVar

# ! Type Vars

VT = TypeVar('VT')
DT = TypeVar('DT')
WT = TypeVar('WT')

# ! Field Function

@overload
def field(value: VT) -> VT: ...
@overload
def field(value: VT, *, default: DT) -> VT | DT: ...
@overload
def field(value: VT, *, default_factory: Callable[[], DT]) -> VT | DT: ...
@overload
def field(value: VT, *, wrap: Callable[[VT], WT]) -> WT: ...
@overload
def field(value: None, default: DT) -> DT: ...
@overload
def field(value: None, default_factory: Callable[[], DT]) -> DT: ...
@overload
def field(value: None, *, default: DT, wrap: Callable[[DT], WT]) -> WT: ...
@overload
def field(value: None, *, default_factory: Callable[[], DT], wrap: Callable[[DT], WT]) -> WT: ...
@overload
def field(value: VT, *, nullable: Literal[True]) -> VT | None: ...
@overload
def field(value: VT, *, nullable: Literal[False]) -> VT: ...
@overload
def field(value: VT, *, wrap: Callable[[VT], WT], nullable: Literal[True]) -> WT | None: ...
@overload
def field(value: VT, *, wrap: Callable[[VT], WT], nullable: Literal[False]) -> WT: ...
@overload
def field(value: VT, *, default: DT, default_wrapped: Literal[True], wrap: Callable[[VT], WT]) -> WT | DT: ...
@overload
def field(value: VT, *, default: DT, default_wrapped: Literal[False], wrap: Callable[[VT], WT]) -> WT | DT: ...
@overload
def field(value: VT, *, default_factory: Callable[[], DT], default_wrapped: Literal[True], wrap: Callable[[VT], WT]) -> WT | DT: ...
@overload
def field(value: VT, *, default_factory: Callable[[], DT], default_wrapped: Literal[False], wrap: Callable[[VT], WT]) -> WT | DT: ...

def field(
    value: Any,
    default: Any = None,
    default_factory: Callable[[], Any] | None = None,
    default_wrapped: bool = False,
    wrap: Callable[[Any], Any] | None = None,
    nullable: bool = False
) -> Any:
    """
    Checks a value and returns it in its original or transformed form, or returns the default value.
    
    Args:
        value: Original value
        default: Default value if value is None
        default_factory: Callable that returns default value when needed
        default_wrapped: Should default value be wrapped if wrap is provided
        wrap: Function to convert value
        nullable: Is None allowed as a valid value
    
    Returns:
        The checked value (possibly converted) or the default value
    
    Raises:
        ValueError: If the value is None but not nullable and there is no default
    """
    if value is None:
        if default is not None:
            return default
        if default_factory is not None:
            default_value = default_factory()
            if wrap is not None and default_wrapped:
                return wrap(default_value)
            return default_value
        if nullable:
            return None
        raise ValueError("Value cannot be None")
    
    if wrap is not None:
        return wrap(value)
    return value