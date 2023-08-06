import pytest
from unittest import mock


@pytest.fixture(scope="function")
def hub(hub):
    for dyne in [R__DYNES__]:
        hub.pop.sub.add(dyne_name=dyne)
    yield hub


@pytest.fixture(scope="function")
def mock_hub(hub):
    m_hub = hub.pop.testing.mock_hub()
    m_hub.OPT = mock.MagicMock()
    yield m_hub
