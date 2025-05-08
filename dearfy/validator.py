import functools
# > Local Imports
from dearfy.field import field
from dearfy.action import Action
from dearfy.functions import formatting_kwargs

# ! Validator Kwargs Base

class ValidatorKwargsBase:
    VALIDATE_KWARGS_KEYS: tuple[str, ...] = ()
    VALIDATE_ERRORS_IGNORE: bool = False

    def __init__(self, **kwargs: object) -> None:
        self.kwargs: dict[str, object] = kwargs
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}({formatting_kwargs(**self.kwargs)})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def validate_value(self, value: object) -> object:
        return value
    
    def validate(self, **kwargs: object) -> dict[str, object]:
        for key, value in kwargs.copy().items():
            if key in self.VALIDATE_KWARGS_KEYS:
                kwargs[key] = self.validate_value(value)
        return kwargs

# ! Validate Callbacks

class ValidateKwargsAction(ValidatorKwargsBase):
    VALIDATE_KWARGS_KEYS: tuple[str, ...] = (
        'callback',
        'drag_callback',
        'drop_callback',
        'on_close',
    )

    def __init__(self, *, app: object | None=None, **kwargs: object) -> None:
        super().__init__(app=app, **kwargs)

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
    
    def validate_value(self, value: str | tuple[str, str] | Action | None) -> Action | None:
        app: object | None = self.kwargs.get('app', None)
        if app is None:
            if self.VALIDATE_ERRORS_IGNORE:
                return None
            else:
                raise RuntimeError('Argument of validator \'app\' not be `None`.')
        return field(
            value,
            default=None,
            wrap=functools.partial(self._validate_action, app),
            nullable=True
        )