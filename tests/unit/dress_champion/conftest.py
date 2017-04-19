import pytest

from dress_champion.models import Dress


@pytest.fixture
def dress_uid():
    return 'TW421CA0Y-A11'


@pytest.fixture
def dress(session, dress_uid):
    d = Dress(uid=dress_uid)
    session.add(d)
    session.commit()
    return d
