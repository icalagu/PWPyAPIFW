import pytest
from pytest_bdd import scenario, given, when, then


@scenario("features/first_feature.feature", "Verify the response to a valid GET request")
def test_verify_response_to_valid_get_request():
    pass


@scenario("features/first_feature.feature", "Verify the response to an invalid GET request")
def test_verify_response_to_invalid_get_request():
    pass
