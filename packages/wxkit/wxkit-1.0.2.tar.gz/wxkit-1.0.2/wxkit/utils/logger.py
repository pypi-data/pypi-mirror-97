import logging
import threading
import wxkit
from collections import defaultdict


_LOGGERS = defaultdict(dict)


def get_logger():
    tid = threading.get_ident()
    if _LOGGERS[tid]:
        return _LOGGERS[tid]

    _logger = logging.getLogger(name=wxkit.__name__)
    _logger.setLevel("DEBUG")
    if not _logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s][%(levelno)s]"
            " - %(message)s"
        )
        _hdr = logging.StreamHandler()
        _hdr.setFormatter(formatter)
        _logger.addHandler(_hdr)

    _LOGGERS[tid] = _logger
    return _logger
