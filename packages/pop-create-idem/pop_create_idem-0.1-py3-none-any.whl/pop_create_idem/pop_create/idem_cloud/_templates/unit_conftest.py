from unittest import mock

import pytest


@pytest.fixture(scope="function")
def hub(hub):
    hub.pop.sub.add(dyne_name="idem")
    yield hub


@pytest.fixture(scope="function")
def mock_hub(hub):
    m_hub = hub.pop.testing.mock_hub()
    m_hub.OPT = mock.MagicMock()
    yield m_hub
