from typing import Dict, List, Union
from ehelply_bootstrapper.drivers.redis import Redis
from ehelply_bootstrapper.drivers.aws_utils.aws_dynamo import Dynamo
from ehelply_bootstrapper.sockets.schemas import *
from redis.client import PubSub
from boto3.dynamodb.conditions import Key
from ehelply_bootstrapper.utils.state import State
from time import sleep
import json


class SocketConnectionBackbone:
    def __init__(self, connection_limit_per_identifier: int = -1) -> None:
        self.connection_limit_per_identifier: int = connection_limit_per_identifier
        self.service: str = State.bootstrapper.service_meta.key

    def is_connections_limited(self) -> bool:
        """
        Returns whether or not there is a limit to socket connections
        """
        if self.connection_limit_per_identifier != -1:
            return True
        return False

    """
    HELPERS
    """

    def make_global_subscription_str(self, identifier: str) -> str:
        """
        Returns a channel subscription string for global connections
        """
        return "{service}.sockets.global.{identifier}".format(service=self.service, identifier=identifier)

    def make_channel_subscription_str(self, channel: str, identifier: str = None) -> str:
        """
        Returns a channel subscription string for channel connections
        """
        if identifier:
            return "{service}.sockets.channel.{channel}.{identifier}".format(service=self.service, channel=channel,
                                                                             identifier=identifier)
        else:
            return "{service}.sockets.channel.{channel}".format(service=self.service, channel=channel)

    """
    GLOBAL CONNECTIONS
    """

    async def add_connection(self, identifier: str, connection: str) -> bool:
        """
        Adds a new connection to the connection manager
        """
        pass

    async def remove_connection(self, identifier: str, connection: str = None) -> bool:
        """
        Removes a connection to the connection manager
        """
        pass

    async def get_identifier_connections(self, identifier: str) -> List[str]:
        """
        Retrieves a connection from the connection manager
        """
        pass

    """
    CHANNEL IDENTIFIERS
    """

    async def add_channel_identifier(self, channel: str, identifier: str) -> bool:
        """
        Adds a new connection to the connection manager
        """
        pass

    async def remove_channel_identifier(self, channel: str, identifier: str) -> bool:
        """
        Removes a connection to the connection manager
        """
        pass

    async def get_channel_identifiers(self, channel: str) -> List[str]:
        """
        Gets identifiers who are in a channel
        """
        pass

    """
    BACKBONE EVENTS
    """

    async def send(self, identifier: str, message: SocketMessage):
        """
        Sends a message to all of an identifier's global connections
        """
        pass

    async def channel_send(self, channel: str, identifier: str, message: SocketMessage):
        """
        Sends a message to all of an identifier's connections if that identifier is subscribed to the given channel
        """
        pass

    async def channel_broadcast(self, channel: str, message: SocketMessage):
        """
        Broadcasts a message to all identifier's subscribed to a channel
        """
        pass

    async def get_message(self, identifier: str, blocking: bool = True) -> Union[None, ChannelSocketMessage]:
        """
        Returns the next available message for an identifier

        If blocking mode is enabled, this will block until a message is available

        If blocking mode is disabled, this will return None if no message is available
        """
        pass


class SCBDict(SocketConnectionBackbone):
    """
    SocketConnectionBackbone powered by dicts.

    Great for:
     - Single instance use cases (like a game server)
     - Prototypes
     - Low latency

    Weak for:
     - HA models (multiple instance use cases)
     - Use cases that need connection management to survive reboots
     - Large amounts of identifiers or connections
    """

    def __init__(self, connection_limit_per_identifier: int = -1) -> None:
        super().__init__(connection_limit_per_identifier)

        # Maps identifier to connections
        self.global_connections: Dict[str, List[str]] = {}

        # Maps identifier to channels. This is required for channel send,
        self.channels: Dict[str, List[str]] = {}

        # Maps channel to identifiers. This is required for channel broadcast.
        self.channel_identifiers: Dict[str, List[str]] = {}

        # Maps identifier to new messages
        self.message_queue: Dict[str, List[ChannelSocketMessage]] = {}

    async def add_connection(self, identifier: str, connection: str) -> bool:
        if self.is_connections_limited() \
                and identifier in self.global_connections \
                and len(self.global_connections[identifier]) == self.connection_limit_per_identifier:
            return False

        if identifier in self.global_connections:
            self.global_connections[identifier].append(connection)
        else:
            self.global_connections[identifier] = [connection]

            channel: str = self.make_global_subscription_str(identifier=identifier)
            self.channels[identifier] = [channel]
            self.message_queue[identifier] = []

        return True

    async def remove_connection(self, identifier: str, connection: str = None) -> bool:
        if not identifier:
            return False

        if connection:
            (await self.get_identifier_connections(identifier)).remove(connection)
        else:
            del self.global_connections[identifier]

            for channel in self.channels[identifier]:
                if channel in self.channel_identifiers:
                    self.channel_identifiers[channel].remove(identifier)
                    if len(self.channel_identifiers[channel]) == 0:
                        del self.channel_identifiers[channel]

            del self.channels[identifier]
            del self.message_queue[identifier]

        return True

    async def get_identifier_connections(self, identifier: str) -> List[str]:
        if identifier in self.global_connections:
            return self.global_connections[identifier]
        return []

    async def add_channel_identifier(self, channel: str, identifier: str) -> bool:
        channel_name: str = channel
        channel = self.make_channel_subscription_str(channel=channel_name)
        channel_sends = self.make_channel_subscription_str(channel=channel_name, identifier=identifier)

        if identifier in self.global_connections and channel not in self.channels[identifier]:
            self.channels[identifier].append(channel)
            self.channels[identifier].append(channel_sends)

            if channel in self.channel_identifiers:
                self.channel_identifiers[channel].append(identifier)
            else:
                self.channel_identifiers[channel] = [identifier]
            return True
        return False

    async def remove_channel_identifier(self, channel: str, identifier: str) -> bool:
        channel_name: str = channel
        channel = self.make_channel_subscription_str(channel=channel_name)
        channel_sends = self.make_channel_subscription_str(channel=channel_name, identifier=identifier)

        if identifier in self.global_connections and channel in self.channels[identifier]:
            self.channels[identifier].remove(channel)
            self.channels[identifier].remove(channel_sends)

            self.channel_identifiers[channel].remove(identifier)
            if len(self.channel_identifiers[channel]) == 0:
                del self.channel_identifiers[channel]

            return True
        return False

    async def get_channel_identifiers(self, channel: str) -> List[str]:
        channel = self.make_channel_subscription_str(channel=channel)
        if channel not in self.channel_identifiers:
            return []
        return self.channel_identifiers[channel]

    async def send(self, identifier: str, message: SocketMessage):
        channel = self.make_global_subscription_str(identifier=identifier)
        if identifier in self.global_connections and channel in self.channels[identifier]:
            self.message_queue[identifier].append(
                ChannelSocketMessage(
                    **message.dict(),
                    channel=channel
                )
            )

    async def channel_send(self, channel: str, identifier: str, message: SocketMessage):
        channel = self.make_channel_subscription_str(channel=channel, identifier=identifier)
        if identifier in self.global_connections and channel in self.channels[identifier]:
            self.message_queue[identifier].append(
                ChannelSocketMessage(
                    **message.dict(),
                    channel=channel
                )
            )

    async def channel_broadcast(self, channel: str, message: SocketMessage):
        channel = self.make_channel_subscription_str(channel=channel)
        if channel in self.channel_identifiers:
            for identifier in self.channel_identifiers[channel]:
                self.message_queue[identifier].append(
                    ChannelSocketMessage(
                        **message.dict(),
                        channel=channel
                    )
                )

    async def get_message(self, identifier: str, blocking: bool = True) -> Union[None, ChannelSocketMessage]:
        if identifier not in self.message_queue:
            return None

        if blocking:
            while True:
                if len(self.message_queue[identifier]) > 0:
                    return self.message_queue[identifier].pop(0)
                sleep(0.1)
        else:
            if len(self.message_queue[identifier]) > 0:
                return self.message_queue[identifier].pop(0)
            else:
                return None


class SCBRedis(SocketConnectionBackbone):
    """
    SocketConnectionBackbone powered by Redis

    Great for:
     - HA models (Where more than one instance can be alive at any one time)
     - Single instance models
     - Medium amounts of identifiers or connections
     - Use cases that need connection management to survive reboots
     - Low latency

    Weak for:
     - Prototypes (Requires having a Redis cluster/instance somewhere)
     - Large amounts of identifiers or connections (Redis lives in RAM)

     Limitations:
      - Cannot be used with API Gateway implementations.
        - TODO: To fix this limitations, we would need to store channel state in Redis like we do for dict and dynamo.
                We would also need to add a special flag to this class for disabling pub/sub functionality.
    """

    def __init__(self, redis: Redis, connection_limit_per_identifier: int = -1) -> None:
        super().__init__(connection_limit_per_identifier)
        self.redis: Redis = redis
        self.pubsubs: Dict[str, PubSub] = {}  # Maps identifier to it's Redis PubSub object

    def make_pubsub(self, subscriptions: List[str]) -> PubSub:
        pubsub: PubSub = self.redis.session.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(*subscriptions)
        return pubsub

    def redis_get(self, key: str):
        response = self.redis.session.get("{service}.sockets.{key}".format(service=self.service, key=key))
        if response:
            return json.loads(response)
        return None

    def redis_set(self, key: str, data):
        self.redis.session.set("{service}.sockets.{key}".format(service=self.service, key=key), json.dumps(data))

    def redis_delete(self, key: str):
        self.redis.session.delete("{service}.sockets.{key}".format(service=self.service, key=key))

    async def add_connection(self, identifier: str, connection: str) -> bool:
        """
        TODO:
            - **Verify that we arent breaking connections limit
            - Store key, val into Redis of {identifier: [connection]}.
            if it already exists, pull it, add the new connection, and push back
            - Create Redis pubsub and store into self.pubsubs with the key identifier
            - Subscribe the identifier to 'ehelply.<service>.sockets.global.<identifier>'
        """
        connections: List[str] = await self.get_identifier_connections(identifier=identifier)
        if self.is_connections_limited() and len(connections) == self.connection_limit_per_identifier:
            if len(connections) > 0:
                connections.pop(0)
            else:
                return False

        if connection not in connections:
            connections.append(connection)

        self.redis_set(key=identifier, data=connections)

        if identifier not in self.pubsubs:
            self.pubsubs[identifier] = self.make_pubsub(
                subscriptions=[self.make_global_subscription_str(identifier=identifier)]
            )

        return True

    async def remove_connection(self, identifier: str, connection: str = None) -> bool:
        """
        TODO:
            - If key, val exists in Redis, remove connection from list of connections.
            - If no more connections exist under the key, remove the identifier from Redis
            - If connection is None, remove the identifier from Redis
            - If we remove the identifier from redis, then unsub all of the identifier's pubsubs
            - Remove the identifier from the pubsub dict on the class
        """
        if not identifier:
            return False

        if identifier not in self.pubsubs:
            return False

        connections: List[str] = await self.get_identifier_connections(identifier=identifier)

        if connection and connection in connections:
            connections.remove(connection)

        if connection is not None and len(connections) > 0:
            self.redis_set(key=identifier, data=connections)

        elif len(connections) == 0 or connection is None:
            self.redis_delete(key=identifier)
            self.pubsubs[identifier].unsubscribe()
            del self.pubsubs[identifier]

        return True

    async def get_identifier_connections(self, identifier: str) -> List[str]:
        """
        TODO:
            - If key val exists in Redis, return the list of connections
        """
        connections = self.redis_get(key=identifier)
        if not connections:
            return []
        return connections

    async def add_channel_identifier(self, channel: str, identifier: str) -> bool:
        """
        TODO:
            - If identifier exists in class pubsubs dict, then sub the pubsub to:
                - 'ehelply.<service>.sockets.channel.<channel>.<identifier>'
                - 'ehelply.<service>.sockets.channel.<channel>'
        """
        if identifier in self.pubsubs:
            self.pubsubs[identifier].subscribe(
                self.make_channel_subscription_str(channel=channel),
                self.make_channel_subscription_str(channel=channel, identifier=identifier),
            )
            return True
        return False

    async def remove_channel_identifier(self, channel: str, identifier: str) -> bool:
        """
        TODO:
            - If identifier exists in class pubsubs dict, then UNsub the pubsub to:
                - 'ehelply.<service>.sockets.channel.<channel>.<identifier>'
                - 'ehelply.<service>.sockets.channel.<channel>'
        """
        if identifier in self.pubsubs:
            self.pubsubs[identifier].unsubscribe(
                self.make_channel_subscription_str(channel=channel),
                self.make_channel_subscription_str(channel=channel, identifier=identifier),
            )
            return True
        return False

    async def send(self, identifier: str, message: SocketMessage):
        """
        TODO:
            - Publish a message to 'ehelply.<service>.sockets.global.<identifier>'
        """
        self.redis.session.publish(
            channel=self.make_global_subscription_str(identifier=identifier),
            message=message.json()
        )

    async def channel_send(self, channel: str, identifier: str, message: SocketMessage):
        """
        TODO:
            - Publish a message to 'ehelply.<service>.sockets.channel.<channel>.<identifier>'
        """
        self.redis.session.publish(
            channel=self.make_channel_subscription_str(channel=channel, identifier=identifier),
            message=message.json()
        )

    async def channel_broadcast(self, channel: str, message: SocketMessage):
        """
        TODO:
            - Publish a message to 'ehelply.<service>.sockets.channel.<channel>'
        """
        self.redis.session.publish(
            channel=self.make_channel_subscription_str(channel=channel),
            message=message.json()
        )

    async def get_message(self, identifier: str, blocking: bool = True) -> Union[None, ChannelSocketMessage]:
        """
        TODO:
            - Poll identifier's Redis pubsub get_message(). Return once a message is found.
                - Examples: https://github.com/andymccurdy/redis-py
        """
        if identifier not in self.pubsubs:
            return None

        if blocking:
            while True:
                message = self.pubsubs[identifier].get_message(ignore_subscribe_messages=True)
                if message:
                    return ChannelSocketMessage(**json.loads(message['data']))
                sleep(0.1)
        else:
            message = self.pubsubs[identifier].get_message(ignore_subscribe_messages=True)
            if message:
                return ChannelSocketMessage(**json.loads(message['data']))
            else:
                return None


class SCBDynamo(SocketConnectionBackbone):
    """
    SocketConnectionBackbone powered by Dynamo

    Dynamo table will require the following keys:
        - p_key -> keydex:string
        - s_key -> None

    Great for:
     - HA models (Where more than one instance can be alive at any one time)
     - Single instance models
     - Large amounts of identifiers or connections
     - Use cases that need connection management to survive reboots

    Weak for:
     - Prototypes (Requires having a Dynamo table)
     - Low latency

     TECHNICAL NOTES BELOW:
     - This class is based on the same operations as the Dict class. However, rather than the data being stored in
        memory using dicts, the data is instead stored in DynamoDB

    """
    PKEY_NAME: str = "keydex"

    KEY_PREFIX_GLOBAL_CONNECTIONS: str = "global_connections."
    KEY_PREFIX_CHANNELS: str = "channels."
    KEY_PREFIX_CHANNEL_IDENTIFIERS: str = "channel_identifiers."
    KEY_PREFIX_MESSAGE_QUEUE: str = "message_queue."

    class DynamoRepresentation(BaseModel):
        keydex: str
        data: List[Union[str, dict]]

    def __init__(self, dynamo_table: str, connection_limit_per_identifier: int = -1) -> None:
        super().__init__(connection_limit_per_identifier)
        self.dynamo: Dynamo = Dynamo(
            table_name=dynamo_table,
            p_keys=[SCBDynamo.PKEY_NAME],
            return_model=SCBDynamo.DynamoRepresentation
        )

    async def add_connection(self, identifier: str, connection: str) -> bool:
        global_connections: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier)
        )

        if self.is_connections_limited() \
                and len(global_connections) == 1 \
                and len(global_connections[0].data) == self.connection_limit_per_identifier:
            return False

        if len(global_connections) == 1:
            global_connections[0].data.append(connection)
            self.dynamo.write_batch([
                global_connections[0]
            ])
        else:
            global_connection: SCBDynamo.DynamoRepresentation = SCBDynamo.DynamoRepresentation(
                keydex=SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier,
                data=[connection]
            )

            channel: str = self.make_global_subscription_str(identifier=identifier)

            channel: SCBDynamo.DynamoRepresentation = SCBDynamo.DynamoRepresentation(
                keydex=SCBDynamo.KEY_PREFIX_CHANNELS + identifier,
                data=[channel]
            )

            message: SCBDynamo.DynamoRepresentation = SCBDynamo.DynamoRepresentation(
                keydex=SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier,
                data=[]
            )

            self.dynamo.write_batch([
                global_connection,
                channel,
                message
            ])

        return True

    async def remove_connection(self, identifier: str, connection: str = None) -> bool:
        if not identifier:
            return False

        if connection:
            connections: List[str] = await self.get_identifier_connections(identifier)
            connections.remove(connection)
            self.dynamo.write_batch([
                SCBDynamo.DynamoRepresentation(
                    keydex=SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier,
                    data=connections
                )
            ])
        else:
            channels: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
                KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNELS + identifier)
            )

            identifiers: List[SCBDynamo.DynamoRepresentation] = []
            for channel in channels[0].data:
                channel_identifiers: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
                    KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(
                        SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel)
                )
                if len(channel_identifiers) > 0:
                    channel_identifiers[0].data.remove(identifier)
                    if len(channel_identifiers[0].data) == 0:
                        self.dynamo.delete_batch(keys=[
                            {"keydex": SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel}
                        ])
                    else:
                        identifiers.append(channel_identifiers[0])
            self.dynamo.write_batch(identifiers)

            self.dynamo.delete_batch(keys=[
                {"keydex": SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier},
                {"keydex": SCBDynamo.KEY_PREFIX_CHANNELS + identifier},
                {"keydex": SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier}
            ])

        return True

    async def get_identifier_connections(self, identifier: str) -> List[str]:
        global_connections: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier)
        )

        if len(global_connections) == 0:
            return []
        else:
            return global_connections[0].data

    async def add_channel_identifier(self, channel: str, identifier: str) -> bool:
        channel_name: str = channel
        channel = self.make_channel_subscription_str(channel=channel_name)
        channel_sends = self.make_channel_subscription_str(channel=channel_name, identifier=identifier)

        global_connections: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier)
        )

        channels: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNELS + identifier)
        )

        channel_identifiers: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel)
        )

        if len(global_connections) == 1 and channel not in channels[0].data:
            channels[0].data.append(channel)
            channels[0].data.append(channel_sends)

            self.dynamo.write_batch([
                channels[0]
            ])

            if len(channel_identifiers) == 1:
                channel_identifiers[0].data.append(identifier)
                self.dynamo.write_batch([
                    channel_identifiers[0]
                ])
            else:
                self.dynamo.write_batch([
                    SCBDynamo.DynamoRepresentation(
                        keydex=SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel,
                        data=[identifier]
                    )
                ])
            return True
        return False

    async def remove_channel_identifier(self, channel: str, identifier: str) -> bool:
        channel_name: str = channel
        channel = self.make_channel_subscription_str(channel=channel_name)
        channel_sends = self.make_channel_subscription_str(channel=channel_name, identifier=identifier)

        global_connections: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier)
        )

        channels: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNELS + identifier)
        )

        channel_identifiers: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel)
        )

        if len(global_connections) == 1 and channel in channels[0].data:
            channels[0].data.remove(channel)
            channels[0].data.remove(channel_sends)

            self.dynamo.write_batch([
                channels[0]
            ])

            channel_identifiers[0].data.remove(identifier)
            if len(channel_identifiers[0].data) == 0:
                self.dynamo.delete_batch(keys=[
                    {"keydex": SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel},
                ])
            else:
                self.dynamo.write_batch([
                    channel_identifiers[0]
                ])

            return True
        return False

    async def get_channel_identifiers(self, channel: str) -> List[str]:
        channel = self.make_channel_subscription_str(channel=channel)

        channel_identifiers: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel)
        )

        if len(channel_identifiers) == 0:
            return []

        return channel_identifiers[0].data

    async def send(self, identifier: str, message: SocketMessage):
        channel = self.make_global_subscription_str(identifier=identifier)

        global_connections: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier)
        )

        channels: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNELS + identifier)
        )

        if len(global_connections) == 1 and channel in channels[0].data:
            message_queue: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
                KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier)
            )

            message_queue[0].data.append(
                ChannelSocketMessage(
                    **message.dict(),
                    channel=channel
                ).dict()
            )

            self.dynamo.write_batch([
                message_queue[0]
            ])


    async def channel_send(self, channel: str, identifier: str, message: SocketMessage):
        channel = self.make_channel_subscription_str(channel=channel, identifier=identifier)

        global_connections: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_GLOBAL_CONNECTIONS + identifier)
        )

        channels: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNELS + identifier)
        )

        if len(global_connections) == 1 and channel in channels[0].data:
            message_queue: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
                KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier)
            )

            message_queue[0].data.append(
                ChannelSocketMessage(
                    **message.dict(),
                    channel=channel
                ).dict()
            )

            self.dynamo.write_batch([
                message_queue[0]
            ])

    async def channel_broadcast(self, channel: str, message: SocketMessage):
        channel = self.make_channel_subscription_str(channel=channel)

        channel_identifiers: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_CHANNEL_IDENTIFIERS + channel)
        )

        if channel in channel_identifiers[0].data:
            messages: List[SCBDynamo.DynamoRepresentation] = []

            for identifier in channel_identifiers[0].data:
                message_queue: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
                    KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier)
                )

                message_queue[0].data.append(
                    ChannelSocketMessage(
                        **message.dict(),
                        channel=channel
                    ).dict()
                )

                messages.append(message_queue[0])

            self.dynamo.write_batch(messages)

    async def get_message(self, identifier: str, blocking: bool = True) -> Union[None, ChannelSocketMessage]:
        message_queue: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
            KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier)
        )

        if len(message_queue) == 0:
            return None

        if blocking:
            while True:
                message_queue: List[SCBDynamo.DynamoRepresentation] = self.dynamo.query(
                    KeyConditionExpression=Key(SCBDynamo.PKEY_NAME).eq(SCBDynamo.KEY_PREFIX_MESSAGE_QUEUE + identifier)
                )

                if len(message_queue[0].data) > 0:
                    return ChannelSocketMessage(**message_queue[0].data.pop(0))

                sleep(8)
        else:
            if len(message_queue[0].data) > 0:
                return ChannelSocketMessage(**message_queue[0].data.pop(0))
            else:
                return None
