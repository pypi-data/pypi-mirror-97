from ehelply_bootstrapper.drivers.driver import Driver
import redis
from ehelply_bootstrapper.utils.connection_details import ConnectionDetails


class RedisCredentials(ConnectionDetails):
    database: int


class Redis(Driver):
    def __init__(self, credentials: RedisCredentials = None, verbosity: int = 0):
        super().__init__(verbosity=verbosity)
        self.credentials: RedisCredentials = credentials

        if not self.credentials:
            from ehelply_bootstrapper.utils.state import State
            self.credentials = RedisCredentials(
                host=State.config.redis.host,
                port=State.config.redis.port,
                database=State.config.redis.db,
                username="",
                password=""
            )

        self.session: redis.Redis = None

    def setup(self):
        self.session = redis.Redis(
            host=self.credentials.host,
            db=self.credentials.database,
            port=self.credentials.port
        )
