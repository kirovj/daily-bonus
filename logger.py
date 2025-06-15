from loguru import logger

logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "[<magenta>{extra[key]}</magenta>] - <level>{message}</level>"
    ),
)

logger.add(
    "./logs/app_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} [{extra[key]}] - {message}",
    retention="1 days"
)