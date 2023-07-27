import time

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
import logging

last_called = None

class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists.
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno

                # Find caller from where originated the logged message.
                frame, depth = sys._getframe(6), 6
                
                while frame and frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1

                logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

console = Console()
logger.remove()
logger.add(
    RichHandler(),
    format="{message}",
    colorize=True,
)

logger.configure({"extra": {"markup": True}})