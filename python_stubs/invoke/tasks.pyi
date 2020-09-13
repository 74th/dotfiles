from typing import Callable, Any, List, TypeVar
import mypy_extensions as mx
from .context import Context

TASK = TypeVar("TASK", bound=Callable[[Context], Any])

def task(task: TASK, default:bool=False)->TASK:...
