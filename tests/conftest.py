import pytest

from hypatia import _import_all


@pytest.fixture(scope="session", autouse=True)
def run_before(request):
    _import_all()
