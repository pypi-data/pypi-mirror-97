import logging

from curia.session import Session


def test_session_defaults():
    session = Session()
    assert session
    assert session.debug is False
    assert session.api_token is None


def test_session_with_token():
    session = Session(api_token='test_token')
    assert session
    assert session.api_token == 'test_token'


def test_session_with_debug():
    session = Session(debug=True)
    assert session
    assert session.debug
    assert session.logger.level == logging.DEBUG
