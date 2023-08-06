import pytest
from unittest import mock


@pytest.fixture(scope="session")
def hub(hub):
    for dyne in [R__DYNES__]:
        hub.pop.sub.add(dyne_name=dyne)

    with mock.patch("sys.argv", ["R__NAME__"]):
        hub.pop.config.load([R__DYNES__], "R__CLEAN_NAME__", parse_cli=True)

    yield hub
