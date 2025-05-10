from __future__ import annotations

from typing_extensions import Any, TypeVar

# ! Types

T = TypeVar('T')

# ! Require Bases Metaclass

class RequireBasesMeta(type):
    """A metaclass that requires inheritance from the specified base classes.
    
    ### Using
    >>> class Object(metaclass=RequireBasesMeta):
    >>>     __required_bases__: tuple[type, ...] = (object, )

    or

    >>> @require_bases(int)
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

def require_bases(*required: type[T]) -> type[T]:
    """A decorator that adds requirements to base classes.
    Requires use of the `RequireBasesMeta` metaclass.

    :return: A modified class with requirements to inherit other metaclasses.
    :rtype: type[T]
    """
    def wrapper(cls: type[T]) -> type[T]:
        cls.__required_bases__ = required
        return cls
    return wrapper