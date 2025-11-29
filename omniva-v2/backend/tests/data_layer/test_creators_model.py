"""Creator model smoke tests."""

from __future__ import annotations

from app.models.db.tables.creators import Creator


def test_creator_persists(session):
    creator = Creator(platform="tiktok", username="creatorlab")
    session.add(creator)
    session.commit()
    session.refresh(creator)

    stored = session.query(Creator).filter_by(username="creatorlab").one()
    assert stored.creator_id == creator.creator_id
    assert stored.platform == "tiktok"
