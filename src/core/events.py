from typing import Callable, List, Dict
from enum import Enum

from utils.event_emmiter import EventEmitter

class EventKind(Enum):
    UPDATED = "updated"
    ACTIVE_HANDLER_CHANGED = "active-handler-changed"

def setup_events() -> Dict[EventKind, EventEmitter]:
    return {
        EventKind.UPDATED: EventEmitter(),
        EventKind.ACTIVE_HANDLER_CHANGED: EventEmitter(),
    }
