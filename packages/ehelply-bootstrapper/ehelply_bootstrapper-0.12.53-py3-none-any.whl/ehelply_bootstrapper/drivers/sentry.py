from ehelply_bootstrapper.drivers.driver import Driver
from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.utils.service import ServiceMeta
from ehelply_bootstrapper.utils.environment import Environment
from ehelply_logger.Logger import VERBOSITY_DEBUG
import sentry_sdk


class Sentry(Driver):
    def __init__(self, service_meta: ServiceMeta, service_process: str, verbosity: int = 0, sql_alchemy: bool = False):
        self.service_meta: ServiceMeta = service_meta
        self.service_process: str = service_process
        self.sql_alchemy = sql_alchemy
        super().__init__(verbosity=verbosity)

    def setup(self):
        integrations: list = []

        sentry_sdk.init(
            State.config.sentry.dsn,
            environment=Environment.stage(),
            release=self.service_meta.key + '@' + self.service_meta.version,
            server_name=self.service_process,
            debug=Environment.is_dev() and self.verbosity >= VERBOSITY_DEBUG,
            integrations=integrations
        )

        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("service-name", self.service_meta.name)
            scope.set_tag("service-key", self.service_meta.key)
