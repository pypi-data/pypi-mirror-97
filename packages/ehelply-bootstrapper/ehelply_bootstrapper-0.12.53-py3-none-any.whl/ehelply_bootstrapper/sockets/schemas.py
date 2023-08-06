from pydantic import BaseModel
from typing import Any


class SocketMessage(BaseModel):
    """
    SocketMessage represents the action and data that is passed in and passed out of a socket connection
    """
    action: str
    data: dict = {}


class ChannelSocketMessage(SocketMessage):
    """
    SocketMessage represents the action and data that is passed in and passed out of a socket connection
    """
    channel: str = None


class APIGatewayMessage(BaseModel):
    """
    APIGatewayMessage represents a message coming in from an API Gateway $default VPC integration
    """
    connection_id: str
    event: str
    message: ChannelSocketMessage

    def __init__(self, **data: Any) -> None:
        """
        Adds in a default (blank) action if one does not exist in the incoming data. For example, on a DISCONNECT event
            from API Gateway, an action wouldn't be sent
        """
        data: dict = dict(data)
        if 'action' not in data['message']:
            data['message']['action'] = ""
        super().__init__(**data)

