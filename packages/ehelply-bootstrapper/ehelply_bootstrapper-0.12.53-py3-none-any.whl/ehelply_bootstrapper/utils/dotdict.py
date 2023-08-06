from types import SimpleNamespace
import json


class DotDict:
    """
    Converting between dict/json and SimpleNamespaces

    This essentially takes in a dict or JSON and lets you utilize dot notation on the object
    """
    @staticmethod
    def from_dict(data: dict) -> SimpleNamespace:
        return SimpleNamespace(**data)

    @staticmethod
    def from_json(data: str) -> SimpleNamespace:
        return SimpleNamespace(**json.loads(data))

    @staticmethod
    def to_dict(data: SimpleNamespace) -> dict:
        return vars(data)

    @staticmethod
    def to_json(data: SimpleNamespace) -> str:
        return json.dumps(vars(data))