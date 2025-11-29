"""Clip model tests."""

from __future__ import annotations

from app.models.db.tables.clips import Clip, ClipStatus
from app.models.db.tables.creators import Creator
from app.models.db.tables.posts import Post
from app.models.db.tables.videos import Video


def test_clip_defaults(session):
    creator = Creator(platform="instagram", username="insta")
    post = Post(
        creator=creator,
        platform="instagram",
        platform_post_id="xyz",
        url="https://instagram.com/p/xyz",
    )
    video = Video(post=post, file_path="storage/vid.mp4", checksum="hashxyz")
    clip = Clip(video=video, start_time=0.0, end_time=15.0, confidence=0.9)

    session.add(clip)
    session.commit()

    stored = session.query(Clip).one()
    assert stored.status == ClipStatus.PENDING
    assert stored.video.post.creator.username == "insta"
