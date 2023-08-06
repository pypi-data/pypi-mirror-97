from ehelply_bootstrapper.events.events import Event, EventListener
from ehelply_bootstrapper.sockets.managers import SocketConnectionManager
from ehelply_bootstrapper.sockets.schemas import SocketMessage


class EventSocketMessage(Event):
    """
    Generic SocketMessage event can be used as a base class for any Events that are to
        be used with a sockets_manager
    """
    identifier: str
    connection_manager: SocketConnectionManager

    class Config:
        arbitrary_types_allowed = True


class EventSocketEcho(EventSocketMessage):
    """
    Used to echo back the contents of message.data.text of the incoming socket message
    """
    text: str

    def __init__(self, **parameters) -> None:
        super().__init__(
            name="ehelply.bootstrapper.socket.echo",
            **parameters
        )


class EListenerSocketEcho(EventListener):
    """
    Sends a message back to the socket connection containing the same text the connection sent
    """
    def __init__(self):
        super().__init__("ehelply.bootstrapper.socket.echo", EventSocketEcho)

    async def trigger(self, event: EventSocketEcho):
        await event.connection_manager.send(
            identifier=event.identifier,
            message=SocketMessage(
                action="ehelply.bootstrapper.socket.echo",
                data={
                    "text": event.text
                }
            )
        )
