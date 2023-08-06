from ehelply_bootstrapper.drivers.driver import Driver
from fastapi import FastAPI, Depends, Header, HTTPException

from typing import List

from ehelply_bootstrapper.utils.connection_details import ConnectionDetails

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from sentry_asgi import SentryMiddleware

import uvicorn


class Fastapi(Driver):
    def __init__(self, service_name: str, service_version: str, connection_details: ConnectionDetails = None,
                 verbosity: int = 0):
        super().__init__(connection_details, verbosity)
        self.service_name = service_name
        self.service_version = service_version

    def setup(self):
        self.instance = FastAPI(
            title=self.service_name,
            description=self.service_name + " API",
            version=self.service_version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
        )

    def cors(self, origins: List[str] = None, allow_credentials: bool = True):
        if origins is None:
            origins = []
        self.instance.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=allow_credentials,
                                     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], allow_headers=["*"])

    def compression(self, min_size: int = 500):
        self.instance.add_middleware(GZipMiddleware, minimum_size=min_size)

    def sentry(self):
        self.instance.add_middleware(SentryMiddleware)

    def run_dev_server(self, key_file_path: str = None, cert_file_path: str = None):
        from ehelply_bootstrapper.utils.state import State

        if key_file_path and cert_file_path:
            uvicorn.run(self.instance, host=State.config.fastapi.dev_server.host, port=State.config.fastapi.dev_server.port, ssl_keyfile=key_file_path, ssl_certfile=cert_file_path)
        else:
            uvicorn.run(self.instance, host=State.config.fastapi.dev_server.host, port=State.config.fastapi.dev_server.port)

    def mount_app(self, path: str, app):
        self.instance.mount(path, app)


async def verify_secret(x_interservice_secret: str = Header(...)):
    """
    Verifies with the secret manager that a valid interservice secret exists
    :param x_ehelply_interservice_secret:
    :return:
    """
    from ehelply_bootstrapper.utils.state import State
    if not State.secrets.exists(x_interservice_secret):
        raise HTTPException(status_code=400, detail="Invalid or missing secret: `X-interservice-secret`")


def interservice_protect():
    """
    Helps generate the dependency injection dependencies
    :return:
    """
    return [Depends(verify_secret)]
