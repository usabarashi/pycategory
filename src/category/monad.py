"""Monad
"""
from __future__ import annotations

import inspect
from typing import Any


class Frame:
    def __init__(self, depth: int = 2):
        self.filename: str = inspect.stack()[depth].filename
        self.line: int = inspect.stack()[depth].frame.f_lineno
        self.function: str = inspect.stack()[depth].function
        self.args: dict[str, Any] = inspect.getargvalues(
            inspect.stack()[depth].frame
        ).locals
        self.stack: list[inspect.FrameInfo] = inspect.stack()
