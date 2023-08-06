from ehelply_bootstrapper.utils.state import State
from boto3.dynamodb.types import Binary
from typing import List
from pydantic import BaseModel
from ehelply_bootstrapper.utils.db_encryption import DBEncryption


class Dynamo:
    def __init__(self, table_name: str, p_keys: List[str], encrypted_dict_keys: List[str] = None,
                 return_model=None) -> None:
        self.dynamodb = State.aws.make_resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)
        self.p_keys: List[str] = p_keys
        self.encrypted_keys: List[str] = encrypted_dict_keys
        if self.encrypted_keys is None:
            self.encrypted_keys = []
        self.model = return_model

    def __clean_empty(self, d):
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (self.__clean_empty(v) for v in d) if v]
        return {k: v for k, v in ((k, self.__clean_empty(v)) for k, v in d.items()) if v}

    def process_response(self, response):
        response_items = []
        for response_item in response['Items']:
            for key in self.encrypted_keys:
                if key in response_item and isinstance(response_item[key], Binary):
                    response_item[key] = DBEncryption.decrypt_dict(response_item[key].value)

            if self.model:
                response_item = self.model(**response_item)

            response_items.append(response_item)

        return response_items

    def query(self, **query):
        response = self.table.query(**query)
        return self.process_response(response)

    def write_batch(self, messages: list):
        with self.table.batch_writer(overwrite_by_pkeys=self.p_keys) as batch:
            for message in messages:
                if isinstance(message, BaseModel):
                    message = message.dict()

                if not isinstance(message, dict):
                    raise Exception("Message is not of type dict")

                message = self.__clean_empty(message)

                for key in self.encrypted_keys:
                    if key in message:
                        message[key] = DBEncryption.encrypt(message[key])

                try:
                    batch.put_item(Item=message)
                except:
                    pass

    def delete_batch(self, keys: list):
        with self.table.batch_writer(overwrite_by_pkeys=self.p_keys) as batch:
            for key in keys:
                if isinstance(key, BaseModel):
                    key = key.dict()

                if not isinstance(key, dict):
                    raise Exception("Message is not of type dict")

                key = self.__clean_empty(key)

                for ekey in self.encrypted_keys:
                    if ekey in key:
                        key[ekey] = DBEncryption.encrypt(key[ekey])

                try:
                    batch.delete_item(Key=key)
                except:
                    pass
