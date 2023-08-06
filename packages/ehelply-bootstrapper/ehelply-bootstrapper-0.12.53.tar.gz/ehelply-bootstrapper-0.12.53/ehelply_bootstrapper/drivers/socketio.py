from ehelply_bootstrapper.drivers.driver import Driver
from socketio import AsyncServer, ASGIApp

from ehelply_bootstrapper.utils.connection_details import ConnectionDetails


class Socketio(Driver):
    def __init__(self, connection_details: ConnectionDetails = None, verbosity: int = 0):
        super().__init__(connection_details, verbosity)
        self.socket_app = None

    def setup(self):
        self.instance = AsyncServer(async_mode='asgi', logger=True)
        self.socket_app = ASGIApp(self.instance, socketio_path='server')
