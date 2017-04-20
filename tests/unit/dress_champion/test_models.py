from unittest import mock

from sqlalchemy.exc import IntegrityError

from dress_champion.models import Dress


def test_get_or_create_obj_present(dress, dress_id):
    _dress = Dress.get_or_create('id', dress_id)

    assert _dress.id == dress_id


def test_get_or_create_obj_not_present(db, dress_id):
    _dress = Dress.get_or_create('id', dress_id)

    assert _dress.id == dress_id


def test_get_or_create_obj_not_present_race_condition(db, dress_id, dress):
    with mock.patch('dress_champion.models.db.session') as _session, \
            mock.patch('dress_champion.models.Dress.query') as _query:

        _session.commit.side_effect = IntegrityError(None, None, 'race condition')
        _query.get.side_effect = [None, dress]

        _dress = Dress.get_or_create('id', dress_id)

        assert _dress.uid == dress_id
        assert _session.rollback.called
