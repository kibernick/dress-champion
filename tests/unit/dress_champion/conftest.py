import pytest

from dress_champion.models import Dress


@pytest.fixture
def dress_id():
    return 'TW421CA0Y-A11'


@pytest.fixture
def dress(session, dress_id):
    d = Dress(id=dress_id)
    session.add(d)
    session.commit()
    return d
