import boto3

from ehelply_bootstrapper.utils.connection_details import ConnectionDetails
from ehelply_bootstrapper.drivers.driver import Driver
from ehelply_bootstrapper.utils.cryptography import Encryption


class AWS(Driver):

    def __init__(self, service_gatekeeper_key: str, connection_details: ConnectionDetails = None, verbosity: int = 0):
        from ehelply_bootstrapper.utils.state import State
        super().__init__(connection_details, verbosity)
        enc: Encryption = Encryption([service_gatekeeper_key.encode(Encryption.STRING_ENCODING)])
        self.aws_access_key_id = enc.decrypt_str(State.config.aws.auth.access_key_id.encode(Encryption.STRING_ENCODING))
        self.aws_secret_access_key = enc.decrypt_str(State.config.aws.auth.access_key.encode(Encryption.STRING_ENCODING))

    def make_client(self, name: str, region_name: str = 'ca-central-1', **client_parameters):
        return boto3.client(name, region_name=region_name, aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key, **client_parameters)

    def make_resource(self, name: str, region_name: str = 'ca-central-1', **resource_parameters):
        return boto3.resource(name, region_name=region_name, aws_access_key_id=self.aws_access_key_id,
                              aws_secret_access_key=self.aws_secret_access_key, **resource_parameters)
