from ehelply_bootstrapper.drivers.driver import Driver
from pymongo import MongoClient


class Mongo(Driver):
    def setup(self):
        from ehelply_bootstrapper.utils.state import State
        self.instance = MongoClient(host=State.config.mongo.host,
                                    port=State.config.mongo.port,
                                    username=State.config.mongo.username,
                                    password=State.config.mongo.password,
                                    authSource=State.config.mongo.authsource)

