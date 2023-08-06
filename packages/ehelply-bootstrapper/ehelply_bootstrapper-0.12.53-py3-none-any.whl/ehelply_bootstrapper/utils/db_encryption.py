from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.utils.cryptography import Encryption
import ast
import json
from typing import Any, Union


class DBEncryption:
    """
    Convienent access to DB encryption
    """
    encryption: Encryption = None

    def __init__(self) -> None:
        if DBEncryption.encryption is None:
            DBEncryption.encryption = Encryption(State.secrets.get("database"))

    @staticmethod
    def update_keys():
        DBEncryption.encryption = Encryption(State.secrets.get("database"))

    @staticmethod
    def encrypt(data) -> bytes:
        return DBEncryption.encryption.encrypt(data)

    @staticmethod
    def decrypt(data, enc_type: str = None) -> Union[bytes, str, int, float, list, dict]:
        if not enc_type:
            return DBEncryption.encryption.decrypt(data)
        
        if enc_type == 'str':
            return DBEncryption.encryption.decrypt_str(data)
        
        if enc_type == 'int':
            return DBEncryption.encryption.decrypt_int(data)
        
        if enc_type == 'float':
            return DBEncryption.encryption.decrypt_float(data)
        
        if enc_type == 'list':
            return DBEncryption.encryption.decrypt_list(data)
        
        if enc_type == 'dict':
            return DBEncryption.encryption.decrypt_dict(data)

    @staticmethod
    def decrypt_str(data) -> str:
        return DBEncryption.encryption.decrypt_str(data)

    @staticmethod
    def decrypt_int(data) -> int:
        return DBEncryption.encryption.decrypt_int(data)

    @staticmethod
    def decrypt_float(data) -> float:
        return DBEncryption.encryption.decrypt_float(data)

    @staticmethod
    def decrypt_list(data) -> list:
        return DBEncryption.encryption.decrypt_list(data)

    @staticmethod
    def decrypt_dict(data) -> dict:
        return DBEncryption.encryption.decrypt_dict(data)
