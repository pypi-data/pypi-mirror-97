from cryptography.fernet import Fernet, MultiFernet
import math
import time
import bcrypt
from typing import List, Tuple, Union
import json


class Encryption:
    """
    Provides a small wrapper over the cryptography fernet library
    """

    STRING_ENCODING: str = "utf-8"

    def __init__(self, keys: List[bytes]) -> None:
        """
        Takes in byte keys, translates them to Fernet keys, and creates a MultiFernet instance
        :param keys:
        """
        self.keys: List[Fernet] = []

        for key in keys:
            self.keys.append(Fernet(key))

        self.multi_fernet: MultiFernet = MultiFernet(self.keys)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    def add_key(self, key: bytes):
        """
        Adds a new key to our MultiFernet instance. This key will become the encryption key
        :param key:
        :return:
        """
        fernet_key: Fernet = Fernet(key)
        self.multi_fernet = MultiFernet([fernet_key] + self.keys)
        self.keys.append(fernet_key)

    def remove_key(self, key: bytes):
        """
        Removes all instances of a key. Decryptions with this key will no longer be valid
        :param key:
        :return:
        """
        target: Fernet = Fernet(key)
        for key in self.keys:
            if target._signing_key == key._signing_key and target._encryption_key == key._encryption_key:
                self.keys.remove(key)

    def rotate(self, data: bytes) -> bytes:
        """
        Rotate data encrypted using an old key to the latest key
        :param data:
        :return:
        """
        return self.multi_fernet.rotate(data)

    def encrypt(self, data) -> Union[None, bytes]:
        """
        Encrypts any data that can be casted to bytes
        :param data:
        :return:
        """
        if data is None:
            return None

        if isinstance(data, list) or isinstance(data, dict):
            data: str = json.dumps(data)
        data: bytes = str(data).encode(Encryption.STRING_ENCODING)
        return self.multi_fernet.encrypt(data)

    def decrypt(self, data: bytes, ttl_seconds: int = None) -> Union[None, bytes]:
        """
        Decrypts data and returns bytes.
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return self.multi_fernet.decrypt(data, ttl=ttl_seconds)

    def decrypt_str(self, data, ttl_seconds: int = None) -> Union[None, str]:
        """
        Decrypts a string
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        if data is None:
            return None
        return str(self.decrypt(data, ttl_seconds).decode(Encryption.STRING_ENCODING))

    def decrypt_int(self, data, ttl_seconds: int = None) -> Union[None, int]:
        """
        Decrypts an int
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        if data is None:
            return None
        return int(self.decrypt_str(data, ttl_seconds))

    def decrypt_float(self, data, ttl_seconds: int = None) -> Union[None, float]:
        """
        Decrypts a float
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        if data is None:
            return None
        return float(self.decrypt_str(data, ttl_seconds))

    def decrypt_list(self, data, ttl_seconds: int = None) -> Union[None, list]:
        """
        Decrypts a list
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        if data is None:
            return None
        return list(json.loads(self.decrypt_str(data, ttl_seconds)))

    def decrypt_dict(self, data, ttl_seconds: int = None) -> Union[None, dict]:
        """
        Decrypts a dict
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        if data is None:
            return None
        return dict(json.loads(self.decrypt_str(data, ttl_seconds)))


class Hashing:
    """
    Hashing utility.

    Today it is backended by bcrypt, but that could change in the future
    """
    COST_FACTOR: int = 10

    def __init__(self, cost_factor: int = None) -> None:
        self.cost_factor = Hashing.COST_FACTOR
        if cost_factor:
            self.cost_factor = cost_factor

    def hash_timed(self, data) -> Tuple[bytes, float]:
        """
        Returns the hash and the length of time it took to compute the hash
        """
        start = time.time()
        myhash = self.hash(data)
        end = time.time()
        return myhash, end - start

    def hash(self, data) -> bytes:
        """
        Returns a hash
        """
        salt = bcrypt.gensalt(rounds=self.cost_factor)
        if isinstance(data, str):
            data = data.encode(Encryption.STRING_ENCODING)
        return bcrypt.hashpw(data, salt)

    def check(self, data, myhash) -> bool:
        """
        Verifies that data matches a hash
        """
        if isinstance(data, str):
            data = data.encode(Encryption.STRING_ENCODING)
        if isinstance(myhash, str):
            myhash = myhash.encode(Encryption.STRING_ENCODING)
        try:
            return bcrypt.checkpw(data, myhash)
        except:
            return False
