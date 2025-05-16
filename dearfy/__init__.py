import loguru
import logging as std_logging
# > Local Imports
from dearfy.logging import LoguruRichHandler, spetific_format_log

# ! Logging

loguru.logger.configure(
    handlers=[
        {
            'sink': LoguruRichHandler(
                markup=True,
                show_path=False,
            ),
            'format': spetific_format_log,
            'level': std_logging.NOTSET,
        }
    ]
)