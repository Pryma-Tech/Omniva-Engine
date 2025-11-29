"""Initial Omniva data backbone.

Revision ID: 0001_initial_schema
Revises: None
Create Date: 2025-11-29
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.models.db.types import GUID, JSONType

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "creators",
        sa.Column("creator_id", GUID(), primary_key=True),
        sa.Column("platform", sa.String(length=32), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("profile_url", sa.Text(), nullable=True),
        sa.Column("metadata", JSONType(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("platform", "username", name="uq_creators_platform_username"),
    )

    op.create_table(
        "posts",
        sa.Column("post_id", GUID(), primary_key=True),
        sa.Column("creator_id", GUID(), sa.ForeignKey("creators.creator_id", ondelete="CASCADE")),
        sa.Column("platform", sa.String(length=32), nullable=False),
        sa.Column("platform_post_id", sa.String(length=255), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("posted_at", sa.DateTime(timezone=True)),
        sa.Column("downloaded_at", sa.DateTime(timezone=True)),
        sa.Column("raw_metadata", JSONType()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("platform", "platform_post_id", name="uq_posts_platform_source"),
    )
    op.create_index("ix_posts_creator_posted_at", "posts", ["creator_id", "posted_at"])

    op.create_table(
        "videos",
        sa.Column("video_id", GUID(), primary_key=True),
        sa.Column("post_id", GUID(), sa.ForeignKey("posts.post_id", ondelete="CASCADE")),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("duration_seconds", sa.Float()),
        sa.Column("resolution", sa.String(length=32)),
        sa.Column("checksum", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("checksum", name="uq_videos_checksum"),
    )
    op.create_index("ix_videos_post_id", "videos", ["post_id"])

    op.create_table(
        "analysis",
        sa.Column("analysis_id", GUID(), primary_key=True),
        sa.Column("video_id", GUID(), sa.ForeignKey("videos.video_id", ondelete="CASCADE")),
        sa.Column("transcript", sa.Text()),
        sa.Column("keywords", JSONType()),
        sa.Column("virality_score", sa.Float()),
        sa.Column("relevance_score", sa.Float()),
        sa.Column("language", sa.String(length=16)),
        sa.Column("raw_ai_output", JSONType()),
        sa.Column("model_version", sa.String(length=64)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_analysis_video_id", "analysis", ["video_id"])
    op.create_index("ix_analysis_virality_score", "analysis", ["virality_score"])

    clip_status_enum = sa.Enum("pending", "promoted", "rejected", "archived", name="clipstatus")
    clip_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "clips",
        sa.Column("clip_id", GUID(), primary_key=True),
        sa.Column("video_id", GUID(), sa.ForeignKey("videos.video_id", ondelete="CASCADE")),
        sa.Column("start_time", sa.Float(), nullable=False),
        sa.Column("end_time", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float()),
        sa.Column("subject_focus", sa.String(length=128)),
        sa.Column("faces_detected", sa.Integer()),
        sa.Column("semantic_tags", JSONType()),
        sa.Column("pantheon_votes", JSONType()),
        sa.Column("lattice_priority", sa.Float()),
        sa.Column("metadata", JSONType()),
        sa.Column("status", clip_status_enum, nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_clips_video_id", "clips", ["video_id"])
    op.create_index("ix_clips_confidence_desc", "clips", ["confidence"])

    edit_job_status_enum = sa.Enum("pending", "running", "done", "error", "cancelled", name="editjobstatus")
    edit_job_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "edit_jobs",
        sa.Column("edit_job_id", GUID(), primary_key=True),
        sa.Column("clip_id", GUID(), sa.ForeignKey("clips.clip_id", ondelete="RESTRICT")),
        sa.Column("operations", JSONType(), nullable=False),
        sa.Column("ffmpeg_commands", JSONType()),
        sa.Column("gpu_required", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("estimated_duration_seconds", sa.Float()),
        sa.Column("status", edit_job_status_enum, nullable=False, server_default="pending"),
        sa.Column("error_detail", sa.Text()),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_edit_jobs_status", "edit_jobs", ["status"])
    op.create_index("ix_edit_jobs_clip_id", "edit_jobs", ["clip_id"])

    upload_status_enum = sa.Enum("pending", "uploading", "scheduled", "live", "error", name="uploadstatus")
    upload_status_enum.create(op.get_bind(), checkfirst=True)
    privacy_enum = sa.Enum("public", "unlisted", "private", name="privacystatus")
    privacy_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "upload_jobs",
        sa.Column("upload_job_id", GUID(), primary_key=True),
        sa.Column("clip_id", GUID(), sa.ForeignKey("clips.clip_id", ondelete="RESTRICT")),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("keywords", JSONType()),
        sa.Column("scheduled_time", sa.DateTime(timezone=True)),
        sa.Column("final_scheduled_time", sa.DateTime(timezone=True)),
        sa.Column("privacy_status", privacy_enum, nullable=False, server_default="unlisted"),
        sa.Column("platform", sa.String(length=32)),
        sa.Column("platform_response_id", sa.String(length=64)),
        sa.Column("status", upload_status_enum, nullable=False, server_default="pending"),
        sa.Column("error_detail", sa.Text()),
        sa.Column("metadata", JSONType()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_upload_jobs_status", "upload_jobs", ["status"])
    op.create_index("ix_upload_jobs_clip_id", "upload_jobs", ["clip_id"])

    schedule_status_enum = sa.Enum("pending", "confirmed", "cancelled", name="schedulestatus")
    schedule_status_enum.create(op.get_bind(), checkfirst=True)
    decision_enum = sa.Enum("zenith", "operator_override", "automation", name="decisionsource")
    decision_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "schedules",
        sa.Column("schedule_id", GUID(), primary_key=True),
        sa.Column("clip_id", GUID(), sa.ForeignKey("clips.clip_id", ondelete="RESTRICT")),
        sa.Column("upload_job_id", GUID(), sa.ForeignKey("upload_jobs.upload_job_id", ondelete="SET NULL")),
        sa.Column("recommended_time", sa.DateTime(timezone=True)),
        sa.Column("final_scheduled_time", sa.DateTime(timezone=True)),
        sa.Column("horizon_adjustments", JSONType()),
        sa.Column("decision_source", decision_enum),
        sa.Column("status", schedule_status_enum, nullable=False, server_default="pending"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_schedules_clip_id", "schedules", ["clip_id"])
    op.create_index("ix_schedules_final_time", "schedules", ["final_scheduled_time"])

    op.create_table(
        "stardust_metadata",
        sa.Column("stardust_id", GUID(), primary_key=True),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", GUID(), nullable=False),
        sa.Column("lineage", JSONType(), nullable=False),
        sa.Column("decision_chain", JSONType()),
        sa.Column("trace_id", GUID()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_stardust_entity_lookup", "stardust_metadata", ["entity_type", "entity_id"])

    log_level_enum = sa.Enum("DEBUG", "INFO", "WARN", "ERROR", "FATAL", name="loglevel")
    log_level_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "logs",
        sa.Column("log_id", GUID(), primary_key=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("level", log_level_enum, nullable=False, server_default="INFO"),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("metadata", JSONType()),
        sa.Column("trace_id", GUID()),
        sa.Column("stardust_id", GUID()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_logs_source", "logs", ["source"])
    op.create_index("ix_logs_level", "logs", ["level"])
    op.create_index("ix_logs_created_at_desc", "logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_logs_created_at_desc", table_name="logs")
    op.drop_index("ix_logs_level", table_name="logs")
    op.drop_index("ix_logs_source", table_name="logs")
    op.drop_table("logs")

    op.drop_index("ix_stardust_entity_lookup", table_name="stardust_metadata")
    op.drop_table("stardust_metadata")

    op.drop_index("ix_schedules_final_time", table_name="schedules")
    op.drop_index("ix_schedules_clip_id", table_name="schedules")
    op.drop_table("schedules")

    op.drop_index("ix_upload_jobs_clip_id", table_name="upload_jobs")
    op.drop_index("ix_upload_jobs_status", table_name="upload_jobs")
    op.drop_table("upload_jobs")

    op.drop_index("ix_edit_jobs_clip_id", table_name="edit_jobs")
    op.drop_index("ix_edit_jobs_status", table_name="edit_jobs")
    op.drop_table("edit_jobs")

    op.drop_index("ix_clips_confidence_desc", table_name="clips")
    op.drop_index("ix_clips_video_id", table_name="clips")
    op.drop_table("clips")

    op.drop_index("ix_analysis_virality_score", table_name="analysis")
    op.drop_index("ix_analysis_video_id", table_name="analysis")
    op.drop_table("analysis")

    op.drop_index("ix_videos_post_id", table_name="videos")
    op.drop_table("videos")

    op.drop_index("ix_posts_creator_posted_at", table_name="posts")
    op.drop_table("posts")

    op.drop_table("creators")

    for enum_name in [
        "clipstatus",
        "editjobstatus",
        "uploadstatus",
        "privacystatus",
        "schedulestatus",
        "decisionsource",
        "loglevel",
    ]:
        sa.Enum(name=enum_name).drop(op.get_bind(), checkfirst=True)
