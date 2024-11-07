class EventEmitter:
    def __init__(self):
        self._listeners: List[Callable[..., None]] = []

    def add_listener(self, listener: Callable[..., None]):
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[..., None]):
        self._listeners.remove(listener)

    def emit(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)

    def reset(self):
        self._listeners.clear()