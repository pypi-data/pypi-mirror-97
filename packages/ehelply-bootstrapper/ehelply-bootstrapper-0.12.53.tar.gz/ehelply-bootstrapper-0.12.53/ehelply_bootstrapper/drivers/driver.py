from ehelply_bootstrapper.utils.connection_details import ConnectionDetails
from ehelply_bootstrapper.utils.environment import Environment


class Driver:
    def __init__(self, connection_details: ConnectionDetails = None, verbosity: int = 0):
        self.connection_details = connection_details
        self.dev_mode = Environment.is_dev()
        self.verbosity = verbosity
        self.instance = None

    def init(self):
        if self.dev_mode:
            self.setup_dev()
            self.test()
        else:
            self.setup()

        return self

    def setup(self):
        pass

    def setup_dev(self):
        self.setup()

    def test(self):
        pass
