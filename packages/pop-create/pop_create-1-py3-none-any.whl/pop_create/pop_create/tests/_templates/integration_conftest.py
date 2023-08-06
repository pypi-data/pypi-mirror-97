import pytest
from unittest import mock


@pytest.fixture(scope="session")
def hub(hub):
    hub.pop.sub.add(dyne_name="R__CLEAN_NAME__")

    with mock.patch("sys.argv", ["R__NAME__"]):
        hub.pop.config.load(["R__CLEAN_NAME__"], "R__CLEAN_NAME__", parse_cli=True)

    yield hub
