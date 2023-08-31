"""util functions like logging etc."""
import logging
import os

import mdftofabric

logger = logging.getLogger("mapping-dataflow-to-fabric-with-openai")
# get log level from environment variable , else default value from package log
log_level = os.environ.get("LOG_LEVEL", mdftofabric.LOG_DEFAULT)


def log_info(message, **params):
    """information logging"""
    msg = _logfmt({"message": message, **params})
    if _is_print_log_level() in ["debug", "info"]:
        print(msg)
    logger.info(msg)


def log_debug(message, **params):
    """debug log information"""
    msg = _logfmt({"message": message, **params})
    if _is_print_log_level() in ["debug", "info"]:
        print(msg)
    logger.debug(msg)


def log_warn(message, **params):
    """warning log information"""
    msg = _logfmt({"message": message, **params})
    logger.warning(msg)


def log_error(message, **params):
    """warning log information"""
    msg = _logfmt({"message": message, **params})
    logger.error(msg)


def _logfmt(props) -> str:
    """log format with given dict"""
    msg = "{{ {format_msg} }}"
    if len(props) > 0:
        # pylint: disable=line-too-long
        format_msg = ",".join([f"\"{key}\":\"{str(val)}\"" for key, val in props.items()])
        # pylint: enable=line-too-long
    else:
        format_msg = ""
    return msg.format(format_msg=format_msg)


def _is_print_log_level():
    """
        find the log level is debug or infor
    """
    if log_level in ["debug", "info"]:
        return log_level
    return None
