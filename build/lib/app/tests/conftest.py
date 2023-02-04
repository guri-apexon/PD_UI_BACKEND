import pytest
from app.tests import utils as test_utils

@pytest.fixture(scope="module", autouse=True)
def new_token_on_headers():
    return test_utils.get_token()
