"""Video model tests."""

from __future__ import annotations

from app.models.db.tables.creators import Creator
from app.models.db.tables.posts import Post
from app.models.db.tables.videos import Video


def test_video_relations(session):
    creator = Creator(platform="youtube", username="channel")
    post = Post(
        creator=creator,
        platform="youtube",
        platform_post_id="abc123",
        url="https://youtube.com/watch?v=abc123",
    )
    video = Video(post=post, file_path="s3://bucket/video.mp4", checksum="checksum123")

    session.add(video)
    session.commit()

    fetched = session.query(Video).one()
    assert fetched.post.creator.username == "channel"
    assert fetched.checksum == "checksum123"
