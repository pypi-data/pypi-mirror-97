from pathlib import Path
import json

ENV_PROD = "prod"
ENV_QA = "qa"
ENV_TEST = "test"
ENV_DEV = "dev"


class Environment:
    """
    Singleton class used to store environment variables
    """
    env: dict = None
    path: str = None

    def __init__(self, path, exception_if_created: bool = False) -> None:
        """
        Read in the env.json file in the root of the repo and setup the env singleton var
        """
        if Environment.env is not None:
            if exception_if_created:
                raise Exception("Cannot recreate the environment after it has already been created")
            else:
                return

        Environment.env = {}
        Environment.path = path  # Path(Path(__file__).resolve().parents[2]).joinpath('env.json')

        Environment.env = {
            "stage": "dev"
        }

        with open(path, 'r') as file:
            Environment.env.update(json.load(file))

    @staticmethod
    def stage():
        """
        Return the current stage (dev, qa, prod) from the env vars
        :return:
        """
        if Environment.env is None:
            raise Exception("Environment has not been created yet")
        return Environment.env['stage']

    @staticmethod
    def is_prod():
        """
        Returns true if we are in prod
        :return:
        """
        return Environment.stage() == ENV_PROD

    @staticmethod
    def is_qa():
        """
        Returns true if we are in QA
        :return:
        """
        return Environment.stage() == ENV_QA

    @staticmethod
    def is_test():
        """
        Returns true if we are in test
        :return:
        """
        return Environment.stage() == ENV_TEST

    @staticmethod
    def is_dev():
        """
        Returns true if we are in dev
        :return:
        """
        return Environment.stage() == ENV_DEV
