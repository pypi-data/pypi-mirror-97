import os
import sys
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('../src/curia/api'))
sys.path.insert(0, os.path.abspath('../src/curia/api/swagger_client'))

import datetime
import pytest
import curia

CURIA_API_TOKEN = 'test-token'
FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


@pytest.fixture(scope="session")
def curia_session():
    return curia.session.Session(api_token=CURIA_API_TOKEN)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
