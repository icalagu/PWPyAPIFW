from typing import Generator
import pytest
from playwright.sync_api import Playwright, APIRequestContext, sync_playwright
from steps.first_step import *
from config import API_BASE_URL

# Fixture para obtener la URL base de la API
@pytest.fixture
def api_base_url():
    return API_BASE_URL


@pytest.fixture
def step_request(request):
    return request


@pytest.fixture(scope="session")
def playwright(playwright: Playwright):
    return playwright


@pytest.fixture(scope="session")
def api_request_context(
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url=API_BASE_URL
    )
    yield request_context
    # This method discards all stored responses
    request_context.dispose()

