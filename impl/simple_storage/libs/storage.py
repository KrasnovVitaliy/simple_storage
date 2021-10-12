import rocksdb
from typing import List
from simple_storage.libs.singleton import MetaSingleton

DATA_KEY_PREFIX = "data/"
TOKEN_KEY_PREFIX = "token/"


class Storage(metaclass=MetaSingleton):
    def __init__(self):
        self._db = rocksdb.DB("data.db", rocksdb.Options(create_if_missing=True))

    def get_data(self, key: str) -> bytes:
        return self._db.get(f"{DATA_KEY_PREFIX}{key}".encode())

    def put_data(self, key: str, data: bytes) -> None:
        return self._db.put(f"{DATA_KEY_PREFIX}{key}".encode(), data)

    def delete_data(self, key: str) -> None:
        return self._db.delete(f"{DATA_KEY_PREFIX}{key}".encode())

    def get_data_keys(self) -> List:
        return [k.decode().replace(DATA_KEY_PREFIX, '') for k in self.__get_keys() if
                k.decode().startswith(DATA_KEY_PREFIX)]

    def put_access_token(self, token: str) -> None:
        return self._db.put(f"{TOKEN_KEY_PREFIX}{token}".encode(), b'')

    def delete_access_token(self, token: str) -> None:
        return self._db.delete(f"{TOKEN_KEY_PREFIX}{token}".encode())

    def get_all_tokens(self):
        return [k.decode().replace(TOKEN_KEY_PREFIX, '') for k in self.__get_keys() if
                k.decode().startswith(TOKEN_KEY_PREFIX)]

    def __get_keys(self):
        it = self._db.iterkeys()
        it.seek_to_first()
        return list(it)
