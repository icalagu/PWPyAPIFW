from typing import Any
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import APIRequestContext
from api_helpers import get_response, RESPONSE_CACHE_KEY, get_stored_response, get_response_2


@given(parsers.parse("I send a GET request to the {endpoint} endpoint"))
@when(parsers.parse("I send a GET request to the {endpoint} endpoint"))
@then(parsers.parse("I send a GET request to the {endpoint} endpoint"))
def send_get_request_to_endpoint(endpoint: str, api_base_url: str, step_request, api_request_context: APIRequestContext):
    get_response_2(resource=endpoint, api_base_url=api_base_url, request=step_request, context=api_request_context)



@given(parsers.parse("the response should have a status code of {status_code}"))
@when(parsers.parse("the response should have a status code of {status_code}"))
@then(parsers.parse("the response should have a status code of {status_code}"))
def verify_response_status_code(status_code, request):
    response = get_stored_response(request)
    assert response is not None, f"Response not found in cache for key '{RESPONSE_CACHE_KEY}'"
    assert response["status_code"] == int(status_code), f'Response code expected: {status_code} - Current code: {response["status_code"]}'
    
    

@then("the response should contain the expected data")
def verify_response_contains_expected_data(api_base_url: str, request):
    response = get_response(resource="", request=request,  api_base_url=api_base_url)
    response_data = response.json()
    # Verificar si la clave "id" está presente en la respuesta
    test = response_data.keys()
    assert "ability" in response_data.keys(), "La respuesta no contiene la clave 'id'"
    # Perform your assertions on the response data here
