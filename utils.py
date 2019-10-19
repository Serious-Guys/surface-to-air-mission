from __future__ import annotations
from typing import Optional
import os


class Singleton(type):

    _instance: Optional[Singleton] = None

    def __call__(cls) -> Singleton:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


def format_datetime(datetime):
    return str(datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]) + 'Z'


def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

