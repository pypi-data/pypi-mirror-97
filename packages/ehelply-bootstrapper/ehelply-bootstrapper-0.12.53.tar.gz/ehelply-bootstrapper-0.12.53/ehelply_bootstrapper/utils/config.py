from typing import List


def load_config(config_path, configs: List[str] = None):
    from ehelply_bootstrapper.utils.state import State
    from pymlconf import Root

    if State.config is None:
        State.config = Root()

    State.config.loadfile(config_path + '/bootstrap.yaml')
    State.config.loadfile(config_path + '/aws.yaml')
    State.config.loadfile(config_path + '/fastapi.yaml')
    State.config.loadfile(config_path + '/mongo.yaml')
    State.config.loadfile(config_path + '/rabbitmq.yaml')
    State.config.loadfile(config_path + '/redis.yaml')
    State.config.loadfile(config_path + '/sentry.yaml')
    State.config.loadfile(config_path + '/sql.yaml')
    State.config.loadfile(config_path + '/app.yaml')

    if configs:
        for config in configs:
            State.config.loadfile(config_path + '/' + config)
