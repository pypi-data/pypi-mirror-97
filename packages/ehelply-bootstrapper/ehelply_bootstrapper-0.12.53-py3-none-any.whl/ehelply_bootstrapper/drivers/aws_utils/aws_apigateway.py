from pydantic import BaseModel
from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.sockets.schemas import *


class APIConfig(BaseModel):
    """
    API Configuration. This is required to manage socket connections.
    """
    api_uuid: str
    stage: str
    region: str = 'ca-central-1'


class APIGateway:
    def __init__(self, api_config: APIConfig = None, is_websockets: bool = False) -> None:
        self.api_config: APIConfig = api_config

        self.api_url = self.make_apigateway_url()

        self.is_websockets: bool = is_websockets

        if self.is_websockets:
            self.websocket = State.aws.make_client(name='apigatewaymanagementapi', endpoint_url=self.api_url)

    def make_apigateway_url(self) -> str:
        return "https://{api_uuid}.execute-api.{region}.amazonaws.com/{stage}".format(
            api_uuid=self.api_config.api_uuid,
            region=self.api_config.region,
            stage=self.api_config.stage
        )

    def post_to_connection(self, connection: str, message: ChannelSocketMessage):
        if self.is_websockets:
            self.websocket.post_to_connection(
                ConnectionId=connection,
                Data=message.json().encode('utf-8')
            )

    def delete_connection(self, connection: str):
        if self.is_websockets:
            self.websocket.delete_connection(
                ConnectionId=connection,
            )