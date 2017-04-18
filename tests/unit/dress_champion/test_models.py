from dress_champion.models import Base, Dress


def test_get_or_create(db):
    d = Dress(uid="BABAROGA")
    db.session.add(d)
    db.session.commit()
    # import pdb; pdb.set_trace()
    pass
