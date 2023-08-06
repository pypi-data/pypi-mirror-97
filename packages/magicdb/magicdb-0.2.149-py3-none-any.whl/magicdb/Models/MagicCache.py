from typing import Dict, Any, Union


class MagicCache:
    def __init__(self):
        self._class_cache: [Dict[str, Dict[str, Any]]] = {}

    def get(self, cls: type, id: str) -> Union[Any, None]:
        if cls.__name__ not in self._class_cache:
            return None
        return self._class_cache[cls.__name__].get(id, None)

    def add(self, cls: type, id: str, val: Any) -> None:
        if cls.__name__ not in self._class_cache:
            self._class_cache[cls.__name__] = {}
        self._class_cache[cls.__name__][id] = val

    def remove(self, cls: type, id: str) -> bool:
        if cls.__name__ not in self._class_cache:
            return False
        if id not in self._class_cache[cls.__name__]:
            return False
        del self._class_cache[cls.__name__][id]
        return True

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return self._class_cache
