#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
import sys
import os

from logging.handlers import RotatingFileHandler
from pathlib import Path

from pythonjsonlogger import jsonlogger  # noqa: I900


def _setup_logging(where_level):
    logger = logging.getLogger(__name__)

    # Simple print logger
    tracing = os.environ.get('DLI_TRACE')
    if tracing and tracing.lower() == 'true':
        trace_logger = logging.getLogger('trace_logger')
        trace_logger.setLevel(logging.DEBUG)

        if not trace_logger.hasHandlers():
            s_handler = logging.StreamHandler(stream=sys.stderr)
            s_handler.setLevel(logging.DEBUG)
            trace_logger.addHandler(s_handler)

    json_format = jsonlogger.JsonFormatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        json_indent=2
    )

    switcher = {
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "debug": logging.DEBUG,
        "info": logging.INFO
    }

    to, _, level = str(where_level).partition(":")
    chosen_level = switcher.get(level.lower(), logging.DEBUG)
    logger.setLevel(chosen_level)

    s_handler_formatter = logging.Formatter(
        '%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if to == "stdout":
        s_handler = logging.StreamHandler(stream=sys.stdout)
        s_handler.setLevel(chosen_level)
        s_handler.setFormatter(s_handler_formatter)
        logger.addHandler(s_handler)
    if to == "stderr":
        s_handler = logging.StreamHandler(stream=sys.stderr)
        s_handler.setLevel(chosen_level)
        s_handler.setFormatter(s_handler_formatter)

        if not logger.hasHandlers():
            logger.addHandler(s_handler)
    else:
        logging.StreamHandler(stream=None)



    log_folder = "logs/"
    Path(log_folder).mkdir(parents=True, exist_ok=True)

    r_handler = RotatingFileHandler(
        f'{log_folder}sdk.log', mode='w', backupCount=3)
    r_handler.setLevel(logging.DEBUG)
    r_handler.setFormatter(json_format)

    if len(logger.handlers) == 1:
        logger.addHandler(r_handler)

    return logger
