from typing import List, Union
from fastapi import WebSocket
from ehelply_bootstrapper.sockets.backbones import SocketConnectionBackbone, SCBRedis
from ehelply_bootstrapper.drivers.aws_utils.aws_apigateway import APIGateway
from ehelply_bootstrapper.sockets.schemas import *
from time import sleep
from ehelply_bootstrapper.events.events import EventController
import asyncio


class SocketConnectionManager(EventController):
    """
    SocketConnectionManager manaqes a bunch of socket connections
    """

    def __init__(self, socket_connection_backbone: SocketConnectionBackbone):
        super().__init__()

        self.socket_connection_backbone: SocketConnectionBackbone = socket_connection_backbone

        # Register each event we expect to receive from a websocket client
        # This allows us to proc an event using the action string defined below, rather than creating Events manually
        self.register_events()

        # Register listeners which handle proc'd actions
        self.register_event_listeners()

    def register_events(self):
        """
        Override this method to register events
        """
        pass

    def register_event_listeners(self):
        """
        Override this method to register event listeners
        """
        pass

    async def on_receive(self, identifier: str, message: ChannelSocketMessage):
        """
        Call when a message is received from a client.

        Currently, this proc's a new event using an action. Alternatively, we could forego actions and simply create
            a new Event based on the message coming in. This method just reduces the amount of code to write at the
            cost of a bit of magic.

        :param identifier:
        :param message:
        :return:
        """

        # TODO: Verify that the identifier has joined the channel in the message

        await self.trigger_action(
            connection_manager=self,
            action=message.action,
            identifier=identifier,
            **message.data
        )

    async def connect(self, identifier: str, connection):
        """
        Call when a new SocketConnection is connected

        **NOTE:** Only call this method if the connection is AUTHORIZED
        """
        await self.socket_connection_backbone.add_connection(identifier, connection)

    async def disconnect(self, identifier: str = None, connection=None):
        """
        Forefully disconnect a SocketConnection
        """
        await self.socket_connection_backbone.remove_connection(identifier, connection)

    async def send(self, identifier: str, message: SocketMessage):
        """
        Sends a new message to a specific identifier
        """
        await self.socket_connection_backbone.send(identifier, message)

    async def channel_join(self, channel: str, identifier: str):
        """
        Join a channel
        """
        await self.socket_connection_backbone.add_channel_identifier(channel, identifier)

    async def channel_leave(self, channel: str, identifier: str):
        """
        Leave a channel
        """
        await self.socket_connection_backbone.remove_channel_identifier(channel, identifier)

    async def channel_send(self, channel: str, identifier: str, message: SocketMessage):
        """
        Send to an identifier within a channel
        """
        await self.socket_connection_backbone.channel_send(channel, identifier, message)

    async def channel_broadcast(self, channel: str, message: SocketMessage):
        """
        Broadcast to all identifier's in a channel
        """
        await self.socket_connection_backbone.channel_broadcast(channel, message)

    async def forward_messages(self, identifier: str, connection, blocking: bool = True) -> bool:
        """
        Take a message which is coming from the SocketBackbone and send it to the client
        """
        pass

    async def get_message(self, identifier: str, connection, blocking: bool = True) -> Union[
        None, ChannelSocketMessage]:
        """
        Take a message off the socket connection and return it
        """
        pass


class SCMFastApi(SocketConnectionManager):
    """
    SCMFastApi is a SocketConnectionManager that is powered via clients connecting to FastApi endpoints directly
         using websockets. In other words, the websocket connections terminate on the microservices themselves
    """

    def __init__(self, socket_connection_backbone: SocketConnectionBackbone):
        super().__init__(socket_connection_backbone)

    async def connect(self, identifier: str, connection):
        """
        When a socket connects, any authorization processing should be done PRIOR to calling this method. A code example
        is shown at the bottom of this comment.
        """
        from fastapi.websockets import WebSocketDisconnect

        connection: WebSocket = connection

        connection_string: str = str(connection)

        await super().connect(identifier, connection_string)

        try:
            while True:
                try:
                    is_forwarded: bool = await asyncio.wait_for(self.forward_messages(identifier=identifier, connection=connection, blocking=False), timeout=0.01)
                    message: ChannelSocketMessage = await asyncio.wait_for(self.get_message(identifier=identifier, connection=connection, blocking=False), timeout=0.01)
                    if message:
                        await self.on_receive(identifier=identifier, message=message)

                    if not is_forwarded and not message:
                        sleep(0.01)
                except:
                    pass
        except WebSocketDisconnect:
            await self.disconnect(identifier=identifier, connection=connection_string)

    async def disconnect(self, identifier: str = None, connection=None):
        if connection:
            connection: WebSocket = connection
            await connection.close(1008)

            connection: str = str(connection)

        return await super().disconnect(identifier, connection)

    async def forward_messages(self, identifier: str, connection, blocking: bool = True) -> bool:
        """
        Takes a message out of the socket backbone and sends it to the connection
        """
        connection: WebSocket = connection

        if blocking:
            while True:
                message: ChannelSocketMessage = await self.socket_connection_backbone.get_message(identifier=identifier,
                                                                                                  blocking=blocking)
                if message:
                    await connection.send_text(message.json())
                    return True
                else:
                    return False
        else:
            message: ChannelSocketMessage = await self.socket_connection_backbone.get_message(identifier=identifier,
                                                                                              blocking=blocking)
            if message:
                await connection.send_text(message.json())
                return True
            else:
                return False

    async def get_message(self, identifier: str, connection, blocking: bool = True) -> Union[
        None, ChannelSocketMessage]:
        """
        Gets a message from the socket connection and returns it
        """
        connection: WebSocket = connection

        if blocking:
            while True:
                message: dict = await connection.receive_json(mode='binary')
                if message:
                    return ChannelSocketMessage(**message)
        else:
            message: dict = await connection.receive_json(mode='binary')

            if message:
                try:

                    return ChannelSocketMessage(**message)
                except:
                    print("Invalid message:", message)
                    return None


class SCMApiGateway(SocketConnectionManager):
    """
    SCMFastApi is a SocketConnectionManager that is powered via clients connecting to AWS API Gateway directly and
        then having API Gateway forward events as HTTP requests. In other words, the socket terminates on API Gateway
        and the communication from API Gateway to a microservice is purely REST

    Limitations:
    - Cannot be used with the Redis SCB. There is a comment in SCBRedis with details of how this can be fixed.
    """

    def __init__(self, socket_connection_backbone: SocketConnectionBackbone, api_gateway: APIGateway):
        if isinstance(socket_connection_backbone, SCBRedis):
            raise Exception("Due to limitations in SCBRedis, it cannot be used with SCMApiGateway at this time.")

        super().__init__(socket_connection_backbone)
        self.api_gateway: APIGateway = api_gateway

    async def connect(self, identifier: str, connection):
        identifier_connections: List[str] = await self.socket_connection_backbone.get_identifier_connections(identifier=identifier)

        if connection in identifier_connections:
            return

        await super().connect(identifier=identifier, connection=connection)

    async def disconnect(self, identifier: str = None, connection=None):
        if identifier:
            await super().disconnect(identifier, connection)

        if connection:
            try:
                self.api_gateway.delete_connection(connection=connection)
            except:
                pass

    async def on_receive(self, identifier: str, message: ChannelSocketMessage):
        await super().on_receive(identifier, message)

    async def send(self, identifier: str, message: SocketMessage):
        """
        Sends a message via API Gateway to the identifier
        """
        connections: List[str] = await self.socket_connection_backbone.get_identifier_connections(identifier=identifier)
        channel = self.socket_connection_backbone.make_global_subscription_str(identifier=identifier)
        for connection in connections:
            try:
                self.api_gateway.post_to_connection(connection=connection, message=ChannelSocketMessage(
                    **message.dict(),
                    channel=channel
                ))
            except:
                await self.socket_connection_backbone.remove_connection(identifier=identifier, connection=connection)

    async def channel_send(self, channel: str, identifier: str, message: SocketMessage):
        """
        Sends a message via API Gateway to the identifier within a channel
        """
        if identifier not in await self.socket_connection_backbone.get_channel_identifiers(channel=channel):
            return

        connections: List[str] = await self.socket_connection_backbone.get_identifier_connections(identifier=identifier)
        channel = self.socket_connection_backbone.make_channel_subscription_str(channel=channel, identifier=identifier)
        for connection in connections:
            try:
                self.api_gateway.post_to_connection(connection=connection, message=ChannelSocketMessage(
                    **message.dict(),
                    channel=channel
                ))
            except:
                await self.socket_connection_backbone.remove_connection(identifier=identifier, connection=connection)

    async def channel_broadcast(self, channel: str, message: SocketMessage):
        """
        Broadcasts a message via API Gateway to the identifiers within a channel
        """
        for identifier in await self.socket_connection_backbone.get_channel_identifiers(channel=channel):
            connections: List[str] = await self.socket_connection_backbone.get_identifier_connections(
                identifier=identifier)
            channel = self.socket_connection_backbone.make_channel_subscription_str(channel=channel,
                                                                                    identifier=identifier)
            for connection in connections:
                try:
                    self.api_gateway.post_to_connection(connection=connection, message=ChannelSocketMessage(
                        **message.dict(),
                        channel=channel
                    ))
                except:
                    await self.socket_connection_backbone.remove_connection(identifier=identifier,
                                                                            connection=connection)

    async def forward_messages(self, identifier: str, connection, blocking: bool = True) -> bool:
        """
        Since API Gateway handles all of the socket connections, clients don't connect directly to a microservice.
            Thus, this method is not needed, required, or logical. Therefore it will throw an exception if it used.
            This is because we cannot pull a message out of a queue and send it to a connection. This SCM does not add
            messages to a queue nor does it manage the socket connections.
        """
        raise Exception("SCMApiGateway does not support polling")

    async def get_message(self, identifier: str, connection, blocking: bool = True) -> Union[
        None, ChannelSocketMessage]:
        """
        Since API Gateway handles all of the socket connections, clients don't connect directly to a microservice.
            Thus, this method is not needed, required, or logical. Therefore it will throw an exception if it used.
            This is because we cannot pull a message from a socket connection since there are no connections. Instead,
            API Gateway will issue HTTP requests which we can then use to call on_receive directly.
        """
        raise Exception("SCMApiGateway does not support polling")
