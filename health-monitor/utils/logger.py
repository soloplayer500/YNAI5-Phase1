import logging
import sys
from pathlib import Path


def get_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a logger writing structured JSON-like lines to file + stdout.
    Idempotent — safe to call multiple times with the same name.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        '{"time":"%(asctime)s","logger":"%(name)s","level":"%(levelname)s","msg":%(message)s}'
    )

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger
