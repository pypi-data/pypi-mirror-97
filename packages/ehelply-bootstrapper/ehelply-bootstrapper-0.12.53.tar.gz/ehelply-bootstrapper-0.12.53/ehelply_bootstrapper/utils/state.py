from ehelply_bootstrapper.drivers.fast_api import Fastapi
from ehelply_bootstrapper.drivers.mongo import Mongo
from ehelply_bootstrapper.drivers.redis import Redis
from ehelply_bootstrapper.drivers.mysql import Mysql
from ehelply_bootstrapper.drivers.socketio import Socketio
from ehelply_bootstrapper.drivers.aws import AWS
from ehelply_logger.Logger import Logger
from ehelply_bootstrapper.integrations.integration import IntegrationManager
from ehelply_bootstrapper.utils.secret import SecretManager


class State:
    """
    A state class used to hold globally accessible values across the application
    It can be extended or modified as needed.
    """

    # Bootstrapper
    bootstrapper = None

    # Config
    config = None

    # Logger
    logger: Logger = None

    # Drivers
    app: Fastapi = None
    sockets: Socketio = None
    mongo: Mongo = None
    redis: Redis = None
    mysql: Mysql = None
    aws: AWS = None

    # Integrations
    integrations: IntegrationManager = None

    # Secrets
    secrets: SecretManager = None

    services: dict = {}

    @staticmethod
    def service(name: str):
        if name in State.services:
            return State.services[name]
        else:
            return None
