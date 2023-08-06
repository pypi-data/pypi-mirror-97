import sys
from typing import List, Tuple, Union, Any
from pathlib import Path

import pkg_resources

from ehelply_bootstrapper.drivers.config import Config
from ehelply_bootstrapper.drivers.fast_api import Fastapi
from ehelply_bootstrapper.drivers.mongo import Mongo
from ehelply_bootstrapper.drivers.redis import Redis
from ehelply_bootstrapper.drivers.mysql import Mysql, MySQLCredentials
from ehelply_bootstrapper.drivers.sentry import Sentry
from ehelply_bootstrapper.drivers.socketio import Socketio
from ehelply_bootstrapper.drivers.aws import AWS
from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.utils.secret import SecretManager
from ehelply_bootstrapper.utils.service import ServiceMeta
from ehelply_bootstrapper.utils.environment import Environment
from ehelply_bootstrapper.integrations.integration import IntegrationManager, Integration

from ehelply_logger.Logger import Logger

LOADABLE_FASTAPI = "fastapi"
LOADABLE_MONGO = "mongo"
LOADABLE_MYSQL = "mysql"
LOADABLE_REDIS = "redis"
LOADABLE_SENTRY = "sentry"
LOADABLE_SOCKET = "socket"
LOADABLE_AWS = "aws_utils"


class Bootstrap:
    """
    Bootstrap class gets a service ready to be loaded

    This class SHOULD be overridden to ensure maximum control
    """

    def __init__(
            self,
            service_meta: ServiceMeta,
            service_gatekeeper_key: str,
            service_environment_path: str,
            service_loadables: List[str],
            service_config_path: str = None,
            service_configs: List[str] = None,
            service_verbosity: int = 0,
    ):
        State.bootstrapper = self

        self.service_meta: ServiceMeta = service_meta

        self.service_gatekeeper_key: str = service_gatekeeper_key

        self.service_environment_path: str = service_environment_path
        self.service_loadables: List[str] = service_loadables
        self.service_config_path: str = service_config_path
        self.service_configs: List[str] = service_configs
        self.service_verbosity = service_verbosity

        # Whether to launch a dev server
        self.dev_server: bool = False

        # Applications and clients
        self.fastapi_driver: Fastapi = None
        self.socket_driver: Socketio = None
        self.redis_driver: Redis = None
        self.mysql_driver: Mysql = None
        self.mongo_driver: Mongo = None
        self.aws_driver: AWS = None

        if self.service_config_path is None:
            raise Exception("A configuration path must be specified")

        self.logger: Logger = Logger(verbosity=self.service_verbosity)
        State.logger = self.logger

        self.service_process: str = State.logger.prefix

        self.before_boot()

        self.logger.info("Booting microservice")

        self.logger.info("Creating environment...")
        try:
            Environment(path=self.service_environment_path)
        except:
            self.logger.info("Environment has already been created. Presumably this was done by a child class.")

        if self.if_dev_launch_dev_server() and (Environment.is_dev() or (len(sys.argv) > 1 and "--dev" in sys.argv)):
            self.dev_server = True

        installed_packages = pkg_resources.working_set
        installed_packages_list: list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

        self.logger.info("Loading microservice...")
        self.logger.info(" * Process: " + str(self.service_process))
        self.logger.info(" * Dev server: " + str(self.dev_server))
        self.logger.info(" * Verbosity: " + str(self.service_verbosity))
        self.logger.info(" * Environment path: " + str(self.service_environment_path))
        self.logger.info(" * Stage: " + str(Environment.stage()))
        self.logger.info(" * Configuration path: " + str(self.service_config_path))
        self.logger.info(" * Loading configs: " + str(self.service_configs))
        self.logger.info(" * Loading drivers: " + str(self.service_loadables))
        self.logger.info(" * Meta: " + str(self.service_meta.dict()))
        self.logger.info(" * Packages: " + str(installed_packages_list))

        self.check_loadables_conflicts()
        self.logger.debug("Conflict test passed")

        self.check_loadables_improvements()

        self.logger.info("Pre loading...")
        self.pre_load()

        self.before_config()

        self.logger.info("Loading configuration...")
        Config(config_path=self.service_config_path, configs=service_configs).init()

        self.before_secret_manager()

        self.logger.info("Loading secret manager...")
        State.secrets = SecretManager()

        if LOADABLE_AWS in self.service_loadables:
            self.logger.info("Loading AWS...")
            self.aws_init()
            State.aws = self.aws_driver

        if LOADABLE_FASTAPI in self.service_loadables:
            self.logger.info("Loading fast api...")
            self.fastapi_init()
            State.app = self.fastapi_driver

        self.before_integrations()

        # Loading integrations here so that we can use them when loading driver configs
        self.logger.info("Loading integrations...")
        State.integrations = IntegrationManager(self.fastapi_driver.instance)
        self.register_integrations()
        State.integrations.load()

        self.before_drivers()

        self.logger.info("Loading drivers...")

        if LOADABLE_SENTRY in self.service_loadables:
            self.logger.info("  -> Loading sentry...")
            self.sentry_init()

        if LOADABLE_MYSQL in self.service_loadables:
            self.logger.info("  -> Loading mysql...")
            self.mysql_init()
            State.mysql = self.mysql_driver

        if LOADABLE_SOCKET in self.service_loadables:
            self.logger.info("  -> Loading socket io...")
            self.socket_init()
            State.sockets = self.socket_driver

        if LOADABLE_REDIS in self.service_loadables:
            self.logger.info("  -> Loading redis...")
            self.redis_init()
            State.redis = self.redis_driver

        if LOADABLE_MONGO in self.service_loadables:
            self.logger.info("  -> Loading mongo...")
            self.mongo_init()
            State.mongo = self.mongo_driver

        if LOADABLE_FASTAPI in self.service_loadables:
            self.logger.debug("Registering middleware to fast api...")
            self.fastapi_middleware()
            self.logger.debug("Registering routers to fast api...")
            self.fastapi_routers()
            self.logger.debug("Registering additional endpoints to fast api...")
            self.fastapi_register_endpoints()

        if LOADABLE_SOCKET in self.service_loadables:
            self.logger.debug("Registering additional events to socket io...")
            self.socket_register_events()

        self.logger.info("Setting up integrations...")
        State.integrations.post_load()

        self.logger.info("Ready")

        self.logger.debug("Running post load...")
        self.post_load()

        if (LOADABLE_FASTAPI in self.service_loadables) and self.dev_server:
            self.logger.info("Starting fastapi dev server with uvicorn")
            self.fastapi_driver.run_dev_server(key_file_path=self.get_https_certificate_paths()[0],
                                               cert_file_path=self.get_https_certificate_paths()[1])

    def check_loadables_conflicts(self):
        if LOADABLE_SOCKET in self.service_loadables and LOADABLE_FASTAPI not in self.service_loadables:
            raise Exception("Cannot use sockets without fastapi.")

    def check_loadables_improvements(self):
        if LOADABLE_SENTRY not in self.service_loadables:
            self.logger.warning(
                "You're not using sentry. Consider using sentry to improve error catching and debugging.")

    def if_dev_launch_dev_server(self) -> bool:
        """
        If the environment is dev, should we launch a local gunicorn server on run
        :return:
        """
        return True

    def pre_load(self):
        pass

    def post_load(self):
        pass

    def before_boot(self):
        """
        EVENT HOOK

        Runs prior to the microservice booting
        :return:
        """
        pass

    def before_config(self):
        """
        EVENT HOOK

        Runs prior to configuration being loaded
        :return:
        """
        pass

    def before_secret_manager(self):
        """
        EVENT HOOK

        Runs prior to loading the secret manager
        :return:
        """
        pass

    def before_integrations(self):
        """
        EVENT HOOK

        Runs prior to loading integrations
        :return:
        """
        pass

    def before_drivers(self):
        """
        EVENT HOOK

        Runs prior to loading drivers
        :return:
        """
        pass

    def fastapi_init(self):
        """
        Create the fast api app object
        :return:
        """
        self.fastapi_driver = Fastapi(service_name=self.service_meta.name,
                                      service_version=self.service_meta.version).init()

    def fastapi_middleware(self):
        """
        Inject middleware into fast api
        :return:
        """
        # Cors
        self.fastapi_driver.cors(origins=['*'], allow_credentials=True)

        # Zipping Responses
        self.fastapi_driver.compression(min_size=500)

        if LOADABLE_SENTRY in self.service_loadables:
            self.fastapi_driver.sentry()

        # if LOADABLE_MYSQL in self.service_loadables:
        #     self.mysql_driver.inject_fastapi_middleware(self.fastapi_driver.instance)

    def fastapi_routers(self):
        """
        Register routers to fastapi

        Example
        -------
        self.fastapi_app.include_router(
            admin.router,
            prefix="/admin",
            tags=["admin"],
            responses={404: {"description": "Not found"}},
        )

        :return:
        """
        pass

    def fastapi_register_endpoints(self):
        """
        This allows you to import other files with extra fastapi endpoints which were not inside of routers
        :return:
        """
        pass

    def get_https_certificate_paths(self) -> Tuple[Union[None, str], Union[None, str]]:
        """
        Return file paths to the certificate files

        Tuple is in the form -> (key_file_path, certificate_file_path)
        :return:
        """
        return None, None

    def sentry_init(self):
        """
        Register sentry
        :return:
        """
        Sentry(service_meta=self.service_meta, service_process=self.service_process,
               verbosity=self.service_verbosity).init()

    def get_mysql_credentials(self) -> MySQLCredentials:
        """
        Override to return MySQL credentials
        :return:
        """
        raise Exception("get_mysql_credentials must be overridden in your service file.")

    def mysql_init(self):
        """
        Register sentry
        :return:
        """
        self.mysql_driver = Mysql(self.get_mysql_credentials()).init()

    def socket_init(self):
        """
        This sets up the sockets app

        :return:
        """
        self.socket_driver = Socketio().init()
        self.fastapi_driver.mount_app("/sockets", self.socket_driver.socket_app)

    def socket_register_events(self):
        """
        This allows you to import other files and/or define events for socket io
        :return:
        """
        pass

    def register_integration(self, integration: Integration):
        """
        Registers an integration
        :param integration:
        :return:
        """
        State.integrations.register(integration)

    def register_integrations(self):
        """
        Register all the integrations the micro-service requires
        :return:
        """
        pass

    def redis_init(self):
        self.redis_driver = Redis().init()

    def mongo_init(self):
        """
        Sets up mongodb connection
        :return:
        """
        self.mongo_driver = Mongo().init()

    def aws_init(self):
        """
        Sets up a connection to AWS
        :return:
        """
        self.aws_driver = AWS(self.service_gatekeeper_key).init()

    def install(self, integrations=None, data=None) -> Union[bool, Any]:
        pass

    def seed(self, integrations=None, data=None) -> Union[bool, Any]:
        pass
