from __future__ import annotations

# > Typing
from typing_extensions import Any, Callable, TypeVar, get_type_hints, Annotated

# ! Types

T = TypeVar('T')
CT = TypeVar('CT')

# ! Require Bases Metaclass

class RequireBasesMeta(type):
    """A metaclass that requires inheritance from the specified base classes.
    
    ### Using
    >>> class Object(metaclass=RequireBasesMeta):
    >>>     __required_bases__: tuple[type, ...] = (object, )

    or

    >>> @require_bases(object)
    >>> class Object(metaclass=RequireBasesMeta):
    >>>     pass
    """
    
    def __new__(
        mcls, 
        name: str, 
        bases: tuple[type, ...], 
        namespace: dict[str, Any],
        **kwargs
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        if '__required_bases__' in namespace:
            required_bases: tuple[type, ...] = namespace['__required_bases__']
            missing = [
                rb.__name__
                for rb in required_bases 
                if not any(issubclass(b, rb) for b in bases)
            ]
            if missing:
                raise TypeError(
                    f"Class '{name}' must also inherit from: {', '.join(missing)}"
                )
        return cls

def require_bases(*required: type[T]) -> Callable[[type[CT]], Annotated[type[CT], type[T]]]:
    """A decorator that adds requirements to base classes.
    Requires use of the `RequireBasesMeta` metaclass.

    Returns:
        type[T]: A modified class with requirements to inherit other metaclasses.
    """
    def wrapper(cls: type[CT]) -> type[CT]:
        cls.__required_bases__ = required
        if not hasattr(cls, '__annotations__'):
            cls.__annotations__ = {}
        for base in required:
            cls.__annotations__.update(get_type_hints(base))
        return cls
    return wrapper