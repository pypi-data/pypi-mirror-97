from threading import RLock


class ReportStorage:
    __store: dict
    __read_lock: RLock
    __write_lock: RLock

    def __init__(self):
        self.__store = {}
        self.__write_lock = RLock()
        self.__read_lock = RLock()

    def get(self, uuid: str, clazz: type) -> object:
        with self.__read_lock:
            val = self.__store.get(uuid)
            if val is None or not isinstance(val, clazz):
                return None
            return val

    def put(self, uuid: str, item: object) -> object:
        with self.__write_lock:
            self.__store.setdefault(uuid, item)
            return item

    def remove(self, uuid: str) -> object:
        with self.__write_lock:
            return self.__store.pop(uuid)

    def clear(self):
        self.__store.clear()
