"""
This file will contain common responses we use all the dang time. 
"""

from typing import Union, Type

from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from starlette.responses import JSONResponse

from pydantic import BaseModel


def http_404_not_found(resource: str = None):
    """ 
    Returns not found when a resource does not exist.
    In the case of this Bootstrapper, this can imply that a resource was never created, is now deleted,
      or the request is incorrect
    :param resource
    :return: response 
    """
    if resource:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND,
                            content={'message': '{resource} not found.'.format(resource=resource)})
    else:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={'message': 'Resource not found.'})


def http_403_forbidden(resource: str = None):
    """ 
    Returns forbidden when user is not authorized to access or touch that resource.
    :return: response 
    """
    if resource:
        return JSONResponse(status_code=HTTP_403_FORBIDDEN,
                            content={'message': 'Access forbidden for {resource}.'.format(resource=resource)})
    else:
        return JSONResponse(status_code=HTTP_403_FORBIDDEN, content={'message': 'Access forbidden.'})


def http_200_ok(ok_object):
    """ 
    Returns ok when a GET, PUT, PATCH, or DELETE request is successful
    The ok_object can include a message, the retrieved data, or anything relevant to the request
    :return: response 
    """
    return JSONResponse(status_code=HTTP_200_OK, content=ok_object)


def http_201_created(resource: str = None):
    """ 
    Returns created when a resource is created
    :return: response 
    """
    if resource:
        return JSONResponse(status_code=HTTP_201_CREATED,
                            content={'message': '{resource} created.'.format(resource=resource)})
    else:
        return JSONResponse(status_code=HTTP_201_CREATED, content={'message': 'Created.'})


def http_500_error(error_message: str = None):
    """ 
    Returns internal server error when the microservice errors while trying to process an endpoint
    :return: response 
    """
    if error_message:
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={'message': error_message})
    else:
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={'message': 'Internal error.'})


def http_409_conflict(error_message: str = None):
    """
    Returns conflict when trying to create a resource which already exists
    :return: response
    """
    if error_message:
        return JSONResponse(status_code=HTTP_409_CONFLICT, content={'message': error_message})
    else:
        return JSONResponse(status_code=HTTP_409_CONFLICT,
                            content={'message': 'Conflicting or duplicate resource found.'})


def http_400_bad_request(error_message: str = None, error_object: dict = None):
    """
    Returns bad request when validation fails or the incoming request is malformed
    :return: response
    """
    if error_object is None:
        error_object = {}

    if error_message:
        return JSONResponse(status_code=HTTP_409_CONFLICT, content={'message': error_message, 'error': error_object})
    else:
        return JSONResponse(status_code=HTTP_409_CONFLICT, content={'message': 'Bad request.', 'error': error_object})


def make_openapi_response_model(http_200: Union[bool, int, float, tuple, list, dict, str, Type[BaseModel]] = None, is_http_200_model: bool = False, http_409: str = None, http_400: str = None, http_404: str = None,
                                http_403: str = "Unauthorized - Denied by eHelply", other: dict = None):
    """
    Makes OpenAPI responses for adding data to the OpenAPI spec and auto generated FastAPI docs

    More details: https://fastapi.tiangolo.com/advanced/additional-responses/
    """

    responses: dict = {}

    if other:
        responses = other

    if http_200:
        if isinstance(http_200, (bool, int, float, tuple, list, dict, str)) and not is_http_200_model:
            responses[200] = {
                "description": "Successful Response",
                "content": {
                    "application/json": {
                        "example": http_200
                    }
                }
            }
        else:
            if isinstance(http_200, BaseModel):
                http_200: dict = http_200.dict()
                if 'status_code' in http_200:
                    del http_200['status_code']

                responses[200] = {
                    "description": "Successful Response",
                    "content": {
                    "application/json": {
                        "example": http_200
                    }
                }
                }

    if http_409:
        responses[409] = {
            "description": "{item} already exists".format(item=http_409),
            "content": {
                "application/json": {
                    "example": {"message": "Error message"}
                }
            }
        }

    if http_400:
        responses[400] = {
            "description": http_400,
            "content": {
                "application/json": {
                    "example": {"message": "Error message"}
                }
            }
        }

    if http_404:
        responses[404] = {
            "description": "{item} does not exist".format(item=http_404),
            "content": {
                "application/json": {
                    "example": {"message": "Error message"}
                }
            }
        }

    if http_403:
        responses[403] = {
            "description": http_403,
            "content": {
                "application/json": {
                    "example": {"message": "Error message"}
                }
            }
        }

    return responses
