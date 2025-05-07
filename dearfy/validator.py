import functools
from dearfy.field import field
from dearfy.action import Action

# ! Validator Kwargs Base

class ValidatorKwargsBase:
    def __init__(self, **kwargs: object) -> None:
        self._kwargs: dict[str, object] = kwargs
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def validate(self, **kwargs: object) -> dict[str, object]:
        return kwargs

# ! Validate Callbacks

class ValidateKwargsAction(ValidatorKwargsBase):
    VALIDATE_KEYS: tuple[str, ...] = (
        'callback',
        'drag_callback',
        'drop_callback',
        'on_close',
    )

    @staticmethod
    def _validate_action(
        app: object,
        action: str | tuple[str, str] | Action | None
    ) -> Action | None:
        if action is None or callable(action) or isinstance(action, Action):
            return action
        if isinstance(action, (str, tuple)):
            if not hasattr(app, '_actioner'):
                raise AttributeError("App object has no '_actioner' attribute")
            return app._actioner.get(action)
        raise ValueError(f"Invalid action type: {type(action)}")
    
    def validate(self, **kwargs: object) -> dict[str, object]:
        app = self._kwargs.get('app')
        if app is None:
            return kwargs
        validating, fargs = functools.partial(self._validate_action, app), (None, validating, True)
        for key in self.VALIDATE_KEYS:
            if key in kwargs:
                kwargs[key] = field(kwargs[key], *fargs)
        return kwargs