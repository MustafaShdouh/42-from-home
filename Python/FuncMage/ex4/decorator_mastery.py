from functools import wraps
from collections.abc import Callable

def spell_timer(func: Callable) -> Callable:

