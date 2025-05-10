import re
from io import StringIO
from rich.logging import *
from rich.console import Console, RenderableType
# > Typing
from typing_extensions import Iterable, Iterator
# > Local Imports
from dearfy.functions import get_object_by_address

__all__ = [ 'LoguruRichHandler' ]

# ? Functions

def format_time(time: datetime) -> Text:
    return Text("[{0.day:02}.{0.month:02}.{0.year:04} {0.hour:02}:{0.minute:02}.{0.second:02}]".format(time), end='')

# ? Модификация класса RichHandler для более гибкой настройки форматирования

class LoguruRichHandler(RichHandler):
    def __init__(
        self,
        level: int | str = logging.NOTSET,
        console: Console | None = None,
        *,
        show_time: bool = True,
        omit_repeated_times: bool = True,
        show_level: bool = True,
        show_path: bool = True,
        enable_link_path: bool = True,
        highlighter: Highlighter | None = None,
        markup: bool = True,
        rich_tracebacks: bool = True,
        tracebacks_width: int | None= None,
        tracebacks_code_width: int = 88,
        tracebacks_extra_lines: int = 3,
        tracebacks_theme: str | None = None,
        tracebacks_word_wrap: bool = True,
        tracebacks_show_locals: bool = True,
        tracebacks_suppress: Iterable[str | ModuleType] = (),
        tracebacks_max_frames: int = 100,
        locals_max_length: int = 10,
        locals_max_string: int = 80,
        log_time_format: str | FormatTimeCallable | None = None,
        keywords: list[str] | None = None,
        level_justing_size: int = 12,
    ) -> None:
        super().__init__(
            level=level,
            console=console,
            show_time=show_time,
            omit_repeated_times=omit_repeated_times,
            show_level=show_level,
            show_path=show_path,
            enable_link_path=enable_link_path,
            highlighter=highlighter,
            markup=markup,
            rich_tracebacks=rich_tracebacks,
            tracebacks_width=tracebacks_width,
            tracebacks_code_width=tracebacks_code_width,
            tracebacks_extra_lines=tracebacks_extra_lines,
            tracebacks_theme=tracebacks_theme,
            tracebacks_word_wrap=tracebacks_word_wrap,
            tracebacks_show_locals=tracebacks_show_locals,
            tracebacks_suppress=tracebacks_suppress,
            tracebacks_max_frames=tracebacks_max_frames,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            log_time_format=log_time_format or format_time,
            keywords=keywords
        )
        self.level_justing_size = level_justing_size
    
    def get_level_text(self, record: LogRecord) -> Text:
        level_name = record.levelname
        level_text = Text.styled(
            f'{level_name.center(self.level_justing_size)}', f"logging.level.{level_name.lower()}"
        )
        return Text('[') + level_text + Text(']')

# ! Richer Class

class Richer:
    REGEX_SEARCH_ADDR_OBJECT = r'<{}.* object at (?P<addr>0x[\da-zA-Z]*)>'

    def __init__(self) -> None:
        self.__console = Console(record=True, markup=False, emoji=True, highlighter=None)
        self.__regex_cache = {}
    
    def render_rich_objects(self, objs: Iterable[RenderableType]) -> Iterator[str]:
        yield from ()
        for obj in objs:
            with StringIO() as sio:
                self.__console.file = sio
                self.__console.print(obj, sep='', end='')
                yield sio.getvalue()
    
    def render_rich_object(self, obj: RenderableType) -> str:
        with StringIO() as sio:
            self.__console.file = sio
            self.__console.print(obj, sep='', end='')
            return sio.getvalue()
    
    def replace_addr_objects(self, message: str, module_import_name: str = r'') -> str:
        if module_import_name not in self.__regex_cache:
            pattern = self.__regex_cache[module_import_name] = re.compile(self.REGEX_SEARCH_ADDR_OBJECT.format(module_import_name))
        else:
            pattern = self.__regex_cache[module_import_name]
        for result in pattern.finditer(message):
            try:
                rendered = self.render_rich_object(get_object_by_address(int(result.group('addr'), 16)))
                message = message[:result.start()] + rendered + message[result.end():]
            except:
                pass
        return message

# ! Variables

richer = Richer()

# ! Spetific Methods

def spetific_format_log(record: LogRecord) -> str:
    return richer.replace_addr_objects(record['message'], 'rich')