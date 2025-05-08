import loguru
import inspect
import datetime
import threading
from enum import Enum, Flag, auto
# > Typing
from typing_extensions import (
    Any,
    Iterable,
    Callable,
    Literal,
    TypeAlias, TypeVar,
)
# > Local Imports
from dearfy.typing import Tag

# ! Types

T = TypeVar('T')

ReturnType = TypeVar('ReturnType')

ActionName: TypeAlias = str
ActionGroup: TypeAlias = str
ActionIndeficator: TypeAlias = tuple[ActionName, ActionGroup]
ActionMethod: TypeAlias = \
    Callable[[Tag, dict[str, Any] | str, Any | None], ReturnType] | \
    Callable[[Tag, dict[str, Any] | str], ReturnType] | \
    Callable[[Tag], ReturnType] | \
    Callable[[], ReturnType]

class ActionState(Flag):
    RUNNING = auto()
    ENABLED = auto()

class ActionCallMode(Enum):
    ONE = 0
    MANY = 1

class ActionBlockMode(Enum):
    NONE = 0
    ALL = 1
    GROUP = 2
    SPETIFIC = 3

ActionCallModeLiteral: TypeAlias = Literal['one', 'many'] | Literal[0, 1]
ActionBlockModeLiteral: TypeAlias = Literal['none', 'all', 'group', 'spetific'] | Literal[0, 1, 2, 3]

def __sample_action_method__(sender: Tag, app_data: dict[str, Any] | str, user_data: Any | None) -> Any: ...

def _match_call_args(method: ActionMethod, *args: object) -> Any:
    return args[:len(list(inspect.signature(method).parameters.keys()))]

# ! Methods

def validate_enum(enum_type: type[T], value: ActionBlockMode | str | int) -> T:
    if isinstance(value, str):
        value: T = getattr(enum_type, value.upper())
    elif isinstance(value, int):
        value: T = enum_type(value)
    return value

# ! Action Class

class Action:
    def __init__(
        self,
        parent: 'Actioner',
        name: str,
        method: ActionMethod,
        group: str='main',
        callmode: ActionCallModeLiteral | ActionCallMode = ActionCallMode.MANY,
        blockmode: ActionBlockModeLiteral | ActionBlockMode = ActionBlockMode.NONE,
        blocks: Iterable[ActionName | tuple[ActionName, ActionGroup]]=[],
        threaded: bool=False,
        /
    ) -> None:
        self.actions = parent
        self.__name = name
        self.__method = method
        self.__group = group
        self.__indeficator: tuple[str, str] = (name, group)
        self.__threaded = threaded
        self.__thread: threading.Thread | None = None
        self.callmode = validate_enum(ActionCallMode, callmode)
        self.blockmode = validate_enum(ActionBlockMode, blockmode)
        self.blocks = list(blocks)
        self.state = ActionState.ENABLED
        self.last_call = None
    
    # ^ Dunder Methods
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}(<{self.__name!r}, {self.__group!r}>)'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__indeficator)
    
    def __eq__(self, other: 'Action | tuple[ActionName, ActionGroup]') -> bool:
        if not (isinstance(other, Action) or isinstance(other, tuple)):
            return False
        return hash(self) == hash(other)
    
    def __ne__(self, other: 'Action | tuple[ActionName, ActionGroup]') -> bool:
        return not self.__eq__(other)
    
    def __getattr__(self, name: str):
        return getattr(__sample_action_method__, name)
    
    # ^ Propetyes

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def group(self) -> str:
        return self.__group
    
    @property
    def indeficator(self) -> tuple[ActionName, ActionGroup]:
        return self.__indeficator
    
    @property
    def method(self) -> ActionMethod:
        return self.__method
    
    @property
    def blocked(self) -> bool:
        for block_mode, owner, blocks in self.actions.blocks.copy():
            if block_mode == ActionBlockMode.NONE:
                continue
            elif block_mode == ActionBlockMode.ALL:
                return True
            elif block_mode == ActionBlockMode.GROUP:
                return owner[1] == self.__group
            elif block_mode == ActionBlockMode.SPETIFIC:
                for blocked_iderficator in blocks:
                    if isinstance(blocked_iderficator, str):
                        if blocked_iderficator == self.__name:
                            return True
                    elif isinstance(blocked_iderficator, tuple):
                        if blocked_iderficator == self.__indeficator:
                            return True
        return False
    
    @property
    def enabled(self) -> bool:
        return ActionState.ENABLED in self.state
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        if value:
            self.state |= ActionState.ENABLED
        else:
            self.state &= ~ActionState.ENABLED
    
    @property
    def threaded(self) -> bool:
        return self.__threaded
    
    # ^ Action Methods

    def can_call(self) -> bool:
        return (not ((ActionCallMode.ONE == self.callmode) and (ActionState.RUNNING in self.state))) or self.blocked
    
    # ^ Call Methods

    def __call_main__(
        self,
        sender: Tag,
        app_data: dict[str, Any] | str | None,
        user_data: Any | None=None
    ) -> Any | None:
        if not self.can_call():
            return
        self.state |= ActionState.RUNNING
        self.last_call = datetime.datetime.now()
        self.actions.set_block(True, self.indeficator, self.blockmode, self.blocks)
        try:
            result = self.method(*_match_call_args(self.method, sender, app_data, user_data))
        except:
            result = None
            loguru.logger.exception('An error has occurred in action!')
        self.actions.set_block(False, self.indeficator, self.blockmode, self.blocks)
        self.state &= ~ActionState.RUNNING
        return result
    
    def __call_thread__(
        self,
        sender: Tag,
        app_data: dict[str, Any] | str | None,
        user_data: Any | None=None
    ) -> None:
        self.state |= ActionState.RUNNING
        self.last_call = datetime.datetime.now()
        self.actions.set_block(True, self.indeficator, self.blockmode, self.blocks)
        try:
            self.method(*_match_call_args(self.method, sender, app_data, user_data))
        except:
            loguru.logger.exception('An error has occurred in action!')
        self.actions.set_block(False, self.indeficator, self.blockmode, self.blocks)
        self.state &= ~ActionState.RUNNING

    def __call__(
        self,
        sender: Tag,
        app_data: dict[str, Any] | str | None,
        user_data: Any | None=None
    ) -> Any | None:
        loguru.logger.trace(f"[red]Call[/red]: {self!r}.__call__({sender!r}, {app_data!r}, {user_data!r})")
        if not self.enabled:
            return
        if not self.__threaded:
            loguru.logger.trace(f"[green]Starting[/green] action <{self.__indeficator}> in [gray bold]simple mode[/gray bold].")
            return self.__call_main__(sender, app_data, user_data)
        else:
            if not self.can_call():
                return
            if self.__thread is not None:
                if self.__thread.is_alive():
                    return
            loguru.logger.trace(f"[green]Starting[/green] action <{self.__indeficator}> in [gray bold]thread mode[/gray bold].")
            self.__thread = threading.Thread(target=self.__call_thread__, args=(sender, app_data, user_data))
            self.__thread.start()
            loguru.logger.trace(f"[yellow]Stopped[/yellow] action <{self.__indeficator}> in [gray bold]thread mode[/gray bold].")
            return

# ! Actioner Class

class Actioner:
    def __init__(self) -> None:
        self.__set_block_semaphore = threading.Semaphore(1)
        self.actions: dict[tuple[ActionName, ActionGroup], Action] = {}
        self.blocks: list[
            tuple[ActionBlockMode, tuple[ActionName, ActionGroup], list[ActionName | tuple[ActionName, ActionGroup]]]
        ] = []
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}({list(self.actions.values())})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def set_block(
        self,
        value: bool,
        blocker_action: tuple[ActionName, ActionGroup],
        blockmode: ActionBlockMode,
        blocks: list[ActionName | tuple[ActionName, ActionGroup]],
        /
    ) -> None:
        self.__set_block_semaphore.acquire()
        if value:
            self.blocks.append((blockmode, blocker_action, blocks))
        else:
            indexs_needed_remove = [index for index, block in enumerate(self.blocks) if (block[1] == blocker_action)]
            for index_needed_remove in indexs_needed_remove:
                self.blocks.pop(index_needed_remove)
        self.__set_block_semaphore.release()
    
    def get(self, key: ActionIndeficator | ActionName, default: T=None) -> Action | T:
        if isinstance(key, str):
            for action_indeficator in self.actions.copy().keys():
                if action_indeficator[0] == key:
                    return self.actions[action_indeficator]
        elif isinstance(key, tuple):
            return self.actions[key]
        return default
    
    def action(
        self,
        name: str,
        group: str='main',
        callmode: ActionCallModeLiteral | ActionCallMode = ActionCallMode.MANY,
        blockmode: ActionBlockModeLiteral | ActionBlockMode = ActionBlockMode.NONE,
        blocks: Iterable[ActionName | tuple[ActionName, ActionGroup]]=[],
        threaded: bool=False,
    ):
        def wrapper(method: ActionMethod):
            action = Action(self, name, method, group, callmode, blockmode, blocks, threaded)
            self.actions[action.indeficator] = action
            return action
        return wrapper
    
    def add_action(
        self,
        method: ActionMethod,
        name: str,
        group: str='main',
        callmode: ActionCallModeLiteral | ActionCallMode = ActionCallMode.MANY,
        blockmode: ActionBlockModeLiteral | ActionBlockMode = ActionBlockMode.NONE,
        blocks: Iterable[ActionName | tuple[ActionName, ActionGroup]]=[],
        threaded: bool=False,
    ) -> None:
        action = Action(self, name, method, group, callmode, blockmode, blocks, threaded)
        if action.indeficator in self.actions:
            self.actions[action.indeficator].enabled = False
        self.actions[action.indeficator] = action
