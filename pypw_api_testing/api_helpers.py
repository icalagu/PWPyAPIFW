import json
from typing import Any
import pytest
import requests
from playwright.sync_api import APIRequestContext
from requests.structures import CaseInsensitiveDict
from config import API_BASE_URL, REQUEST_TIMEOUT


RESPONSE_CACHE_KEY = "response"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_response(resource, request: requests.request, api_base_url=API_BASE_URL):
    response = requests.get(f"{api_base_url}/{resource}", timeout=REQUEST_TIMEOUT)
    handle_response_error(response)
    store_api_response(request, response)
    # return response

def get_response_2(resource, request: requests.request, context: APIRequestContext, api_base_url=API_BASE_URL):
    response = context.get(f"/{resource}")
    handle_response_error(response)
    store_api_response(request, response)

def post_response(resource, data, api_base_url=API_BASE_URL):
    response = requests.post(f"{api_base_url}/{resource}", json=data, timeout=REQUEST_TIMEOUT)
    handle_response_error(response)
    return response


def put_response(resource, data, api_base_url=API_BASE_URL):
    response = requests.put(f"{api_base_url}/{resource}", json=data, timeout=REQUEST_TIMEOUT)
    handle_response_error(response)
    return response


def delete_response(resource, api_base_url=API_BASE_URL):
    response = requests.delete(f"{api_base_url}/{resource}", timeout=REQUEST_TIMEOUT)
    handle_response_error(response)
    return response


def patch_response(resource, data, api_base_url=API_BASE_URL):
    response = requests.patch(f"{api_base_url}/{resource}", json=data, timeout=REQUEST_TIMEOUT)
    handle_response_error(response)
    return response


def handle_response_error(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return response  # Return the response object if an HTTP error occurs

    return None  # Return None if the response is successful without any HTTP error


def store_api_response(request, response: requests.Response):
    """
    Store the API response in the cache.

    Args:
        request: The request object that provides access to the pytest configuration cache.
        response: The API response object of type requests.Response.

    Response Data:
        - status_code (int): The status code of the API response.
        - content (Any): The parsed JSON content of the API response.
        - headers (Dict[str, str]): The headers of the API response.
        - url (str): The URL of the API response.
        - elapsed (float): The elapsed time in seconds for the API request.
        - request_data (Dict[str, Any]): The data related to the API request.
            - method (str): The HTTP method used in the request.
            - url (str): The URL of the request.
            - headers (Dict[str, str]): The headers of the request.
            - body (Any): The body of the request.

    Example:
        response_data = {
            "status_code": response.status_code,
            "content": response.json(),
            "headers": dict(response.headers),
            "url": response.url,
            "elapsed": response.elapsed.total_seconds(),
            "request_data": {
                "method": response.request.method,
                "url": response.request.url,
                "headers": dict(response.request.headers),
                "body": response.request.body,
            }
        }
        request.config.cache.set(RESPONSE_CACHE_KEY, response_data)
    """

    response_data = {
        "status_code": getattr(response, "status_code", None),
        "content": None,
        "headers": dict(getattr(response, "headers", CaseInsensitiveDict())),
        "url": getattr(response, "url", None),
        "elapsed": getattr(response.elapsed, "total_seconds", lambda: None)(),
        "request_data": {
            "method": getattr(response.request, "method", None),
            "url": getattr(response.request, "url", None),
            "headers": dict(getattr(response.request, "headers", CaseInsensitiveDict())),
            "body": getattr(response.request, "body", None),
        }
    }

    try:
        response_data["content"] = response.json()
    except json.JSONDecodeError:
        pass

    request.config.cache.set(RESPONSE_CACHE_KEY, response_data)


def get_stored_response(request) -> Any:
    response = request.config.cache.get(RESPONSE_CACHE_KEY, None)
    assert response is not None, f"Response not found in cache for key '{RESPONSE_CACHE_KEY}'"
    return response