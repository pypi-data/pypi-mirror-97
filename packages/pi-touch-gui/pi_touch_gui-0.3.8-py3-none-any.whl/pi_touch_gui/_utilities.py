# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Utility functions that don't fit in any particular class or module.
"""
import logging
import traceback
from datetime import datetime
from pathlib import Path

LOG = logging.getLogger(__name__)

BACKLOG = logging.getLogger('_backlog')
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
BACKLOG.addHandler(handler)
BACKLOG.propagate = False


def snapped_value_string(value, snap) -> str:
    """ Round (snap) a value for clean display, against a given resolution.

    Parameters
    ----------
    value : float
        Value to snap
    snap : float
        An example of the resolution to snap to.  Current supports .001, .1,
        and "other" (e.g. 1)

    Returns
    -------
    str
        Formatted string of the value, at the snap resolution.
    """
    if snap < 0.1:
        val_str = f"{value:0.2f}"
    elif snap < 1:
        val_str = f"{value:0.1f}"
    else:
        val_str = f"{int(value)}"
    return val_str


def clock_indicator_function():
    """ An indicator function to provide a clock.
    """
    return False, datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def backlog_error(exc, message):
    frame = traceback.extract_tb(exc.__traceback__)[-1]
    BACKLOG.error(f"[{Path(frame.filename).stem}.{frame.lineno}] "
                  f"{message}: {type(exc).__name__}: {exc}")
