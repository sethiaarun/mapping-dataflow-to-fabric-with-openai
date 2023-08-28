"""util functions like logging etc."""
import logging
import os

import mdftofabric

logger = logging.getLogger("mapping-dataflow-to-fabric-with-openai")
# get log level from environment variable
log_level = os.environ.get("LOG_LEVEL","info")


def log_info(message, **params):
    """information logging"""
    msg = _logfmt(dict(message=message, **params))
    if _log_level() in ["debug", "info"]:
        print(msg)
    logger.info(msg)


def log_debug(message, **params):
    """debug log information"""
    msg = _logfmt(dict(message=message, **params))
    if _log_level() in ["debug", "info"]:
        print(msg)
    logger.debug(msg)


def log_warn(message, **params):
    """warning log information"""
    msg = _logfmt(dict(message=message, **params))
    logger.warning(msg)


def log_error(message, **params):
    """warning log information"""
    msg = _logfmt(dict(message=message, **params))
    logger.error(msg)


def _logfmt(props) -> str:
    """log format with given dict"""
    msg = "{{ {format_msg} }}"
    if len(props) > 0:
        format_msg = ",".join(["\"{k}\":\"{v}\"".format(k=key, v=str(val)) for key, val in props.items()])
        return msg.format(format_msg=format_msg)
    else:
        return msg.format(format_msg="")


def _log_level():
    """find the log level"""
    if mdftofabric.log in ["debug", "info"]:
        return mdftofabric.log
    elif log_level in ["debug", "info"]:
        return log_level
    else:
        return None
