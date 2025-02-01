from enum import Enum


class Status(str, Enum):
    new = 'new'
    old = 'old'
    damaged = 'damaged'