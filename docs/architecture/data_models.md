# Omniva Engine — Data Models

## 1. Overview
Omniva Engine relies on a unified relational data model to keep cognitive guidance and operational execution synchronized. The database acts as the backbone that ties ingestion, analysis, editing, publishing, and scheduling together so that every worker consumes and emits consistent state. Stardust, the provenance ledger, coexists with this store by recording immutable lineage packets that reference primary keys in the relational tables, letting HaloLux narrate decisions with full evidence. Strict schemas eliminate ambiguity across workers: job lifecycles are enforced through foreign keys, JSONB columns capture structured metadata without breaking contracts, and UUIDv4 identifiers ensure global uniqueness.

## 2. ERD (Entity Relationship Diagram)
```
creators 1 ──< posts 1 ──< videos 1 ──< analysis 1 ──< clips 1 ──< edit_jobs 1 ──< upload_jobs 1 ──< schedules
   |              |           |             |             |              |                      |
   |              |           |             |             |              |                      `──< logs
   |              |           |             |             |              `──< stardust_metadata
   |              |           |             |             `──< logs
   |              |           |             `──< stardust_metadata
   |              `──< logs
   `──< stardust_metadata
```
Arrow legend: `A ──< B` means `A` (parent) has many `B` (child). Logs and Stardust entries may reference any upstream entity via polymorphic foreign keys.

```text
┌────────────┐   ┌─────────────┐   ┌────────────┐
│  creators  │ 1 │    posts    │ n │   videos   │
└─────┬──────┘   └──────┬──────┘   └──────┬─────┘
      │                │                 │
      │                ▼                 ▼
      │          ┌───────────┐     ┌────────────┐
      │          │  analysis │ 1 n │   clips    │
      │          └──────┬────┘     └──────┬─────┘
      │                 │                │ │
      │                 ▼                │ ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ stardust_meta│  │  edit_jobs   │ 1 │ upload_jobs │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                │
       ▼                 ▼                ▼
┌────────────────────────┐
│       schedules        │
└────────────────────────┘

       ┌──────────────────────────────────────────┐
       │                  logs                    │
       └──────────────────────────────────────────┘
```

## 3. Table Definitions (SQL Schema)
All tables use `UUIDv4` primary keys, `TIMESTAMP WITH TIME ZONE` (UTC) for temporal fields, and `NOT NULL` constraints unless a column is explicitly optional.

### 3.1 creators
- **Description**: Canonical registry of creators or channels under management.
- **Fields**:
  - `creator_id UUID PRIMARY KEY`
  - `platform TEXT NOT NULL`
  - `username TEXT NOT NULL`
  - `profile_url TEXT`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
  - `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: Unique index on `(platform, username)` to enforce one record per handle.
- **Relationships**: `creators.creator_id` referenced by `posts.creator_id`. Logs/Stardust entries may point to creators through polymorphic keys.
- **Notes for Implementers**: Keep `updated_at` synchronized via triggers; prefer storing platform-normalized usernames to avoid duplicate casing.

### 3.2 posts
- **Description**: Individual social posts or feed entries fetched from a creator.
- **Fields**:
  - `post_id UUID PRIMARY KEY`
  - `creator_id UUID NOT NULL REFERENCES creators(creator_id)`
  - `platform_post_id TEXT NOT NULL`
  - `url TEXT NOT NULL`
  - `posted_at TIMESTAMPTZ`
  - `downloaded_at TIMESTAMPTZ`
  - `raw_metadata JSONB`
- **Indexing Strategy**: B-tree index on `(creator_id, posted_at)` for chronological queries; optional unique `(platform_post_id, platform)` if needed.
- **Relationships**: One-to-many with `videos`; logs and Stardust metadata reference `posts`.
- **Notes for Implementers**: Store raw API payloads in `raw_metadata` for reproducibility; keep `posted_at` null if unknown rather than defaulting to epoch.

### 3.3 videos
- **Description**: Media assets derived from posts, normalized for downstream processing.
- **Fields**:
  - `video_id UUID PRIMARY KEY`
  - `post_id UUID NOT NULL REFERENCES posts(post_id)`
  - `file_path TEXT NOT NULL`
  - `duration_seconds INT`
  - `resolution TEXT`
  - `checksum TEXT NOT NULL`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: B-tree on `(post_id)` for joins; unique index on `checksum` to detect duplicates across creators.
- **Relationships**: Parent of `analysis`, `clips`, `edit_jobs` (via clips), logs, and Stardust records.
- **Notes for Implementers**: `file_path` stores URI (local or cloud). Keep checksums consistent (e.g., SHA-256 hex).

### 3.4 analysis
- **Description**: Output of the Analyzer worker capturing NLP/NLU insights.
- **Fields**:
  - `analysis_id UUID PRIMARY KEY`
  - `video_id UUID NOT NULL REFERENCES videos(video_id)`
  - `transcript TEXT`
  - `keywords TEXT[]`
  - `virality_score FLOAT`
  - `relevance_score FLOAT`
  - `raw_ai_output JSONB`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: B-tree on `(video_id)`; partial index on `virality_score DESC` for trending queries.
- **Relationships**: One video may have multiple analyses (versioned); `clips` reference `video_id` directly but also infer insights from latest analysis.
- **Notes for Implementers**: Persist raw model output to enable audit/retrofits. Enforce that only one “active” analysis per video is marked via view or status flag.

### 3.5 clips
- **Description**: Candidate segments extracted from videos for editing/promotions.
- **Fields**:
  - `clip_id UUID PRIMARY KEY`
  - `video_id UUID NOT NULL REFERENCES videos(video_id)`
  - `start_time FLOAT NOT NULL`
  - `end_time FLOAT NOT NULL`
  - `confidence FLOAT`
  - `semantic_tags TEXT[]`
  - `pantheon_votes JSONB`
  - `lattice_priority FLOAT`
  - `metadata JSONB`
- **Indexing Strategy**: B-tree on `(video_id)` plus descending index on `confidence` to quickly surface top clips.
- **Relationships**: Parent for `edit_jobs`, `upload_jobs`, `schedules`. Logs/Stardust metadata often reference clips when reasoning about selection.
- **Notes for Implementers**: Validate `end_time > start_time`. Store Pantheon per-agent votes as key/value objects.

### 3.6 edit_jobs
- **Description**: Concrete editing tasks generated for a clip.
- **Fields**:
  - `edit_job_id UUID PRIMARY KEY`
  - `clip_id UUID NOT NULL REFERENCES clips(clip_id)`
  - `operations JSONB NOT NULL`
  - `ffmpeg_commands TEXT[]`
  - `gpu_required BOOL DEFAULT false`
  - `estimated_duration_seconds INT`
  - `status TEXT NOT NULL DEFAULT 'PENDING'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: B-tree on `(clip_id)`; optional partial index where `status = 'PENDING'` for quick dispatch.
- **Relationships**: Child of clips, parent of upload jobs through clip chain. Logs track execution traces keyed by `edit_job_id`.
- **Notes for Implementers**: Store declarative operations (trim, caption) in structured JSON; keep `ffmpeg_commands` derived for reproducibility.

### 3.7 upload_jobs
- **Description**: Publishing instructions for a rendered clip.
- **Fields**:
  - `upload_job_id UUID PRIMARY KEY`
  - `clip_id UUID NOT NULL REFERENCES clips(clip_id)`
  - `title TEXT`
  - `description TEXT`
  - `keywords TEXT[]`
  - `scheduled_time TIMESTAMPTZ`
  - `privacy_status TEXT`
  - `yt_video_id TEXT`
  - `status TEXT NOT NULL DEFAULT 'PENDING'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: B-tree on `(scheduled_time)` for calendar views; partial index on `(status)` for pending/failed filters.
- **Relationships**: Feeds `schedules` and references `clips`. Logs capture worker activity per upload job.
- **Notes for Implementers**: Keep `yt_video_id` nullable until publish succeeds; store multi-platform metadata in JSON if necessary.

### 3.8 schedules
- **Description**: Actual scheduling commitments derived from Horizon/Zenith decisions.
- **Fields**:
  - `schedule_id UUID PRIMARY KEY`
  - `clip_id UUID NOT NULL REFERENCES clips(clip_id)`
  - `recommended_time TIMESTAMPTZ`
  - `final_scheduled_time TIMESTAMPTZ`
  - `horizon_adjustments JSONB`
  - `status TEXT NOT NULL DEFAULT 'PENDING'`
- **Indexing Strategy**: B-tree on `(final_scheduled_time)` for calendar queries and SLA enforcement.
- **Relationships**: One-to-one or one-to-many with upload jobs depending on workflow; referenced by logs and Stardust to track scheduling provenance.
- **Notes for Implementers**: `horizon_adjustments` stores weight deltas from Horizon Engine; ensure `final_scheduled_time` is null until Zenith commits.

### 3.9 stardust_metadata
- **Description**: Immutable lineage packets linking events, evidence, and decisions.
- **Fields**:
  - `stardust_id UUID PRIMARY KEY`
  - `entity_type TEXT NOT NULL`
  - `entity_id UUID NOT NULL`
  - `lineage JSONB NOT NULL`
  - `decision_chain JSONB`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: Composite index on `(entity_type, entity_id)` for fast lookups; optional GIN index on `lineage` for containment queries.
- **Relationships**: Polymorphic links to any table (creators, posts, videos, clips, jobs). Does not enforce FK to keep ledger append-only.
- **Notes for Implementers**: Store `entity_type` using canonical table names; include `trace_id` and parent references in `lineage`.

### 3.10 logs
- **Description**: Structured operational and cognitive logs for observability.
- **Fields**:
  - `log_id UUID PRIMARY KEY`
  - `source TEXT NOT NULL` (e.g., `scraper_worker`, `zenith`)
  - `level TEXT NOT NULL` (INFO/WARN/ERROR)
  - `message TEXT NOT NULL`
  - `metadata JSONB`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Indexing Strategy**: B-tree indexes on `(source)` and `(level)`; optional `(created_at DESC)` for time-series queries.
- **Relationships**: Log metadata stores `entity_type`/`entity_id` references to other tables; also cross-links to Stardust IDs.
- **Notes for Implementers**: Keep messages concise; push heavy payloads into `metadata`. Enforce JSON schema validation to ensure consistent log structure.

## 4. Derived Views (Optional)
1. **latest_analysis_per_video**  
   ```sql
   CREATE MATERIALIZED VIEW latest_analysis_per_video AS
   SELECT DISTINCT ON (video_id)
          video_id, analysis_id, virality_score, relevance_score, created_at
   FROM analysis
   ORDER BY video_id, created_at DESC;
   ```
2. **best_clip_per_video**  
   ```sql
   CREATE MATERIALIZED VIEW best_clip_per_video AS
   SELECT DISTINCT ON (video_id)
          video_id, clip_id, confidence, lattice_priority
   FROM clips
   ORDER BY video_id, confidence DESC, lattice_priority DESC;
   ```
3. **pending_edit_jobs**  
   ```sql
   CREATE VIEW pending_edit_jobs AS
   SELECT *
   FROM edit_jobs
   WHERE status = 'PENDING'
   ORDER BY created_at ASC;
   ```
4. **upcoming_upload_schedule**  
   ```sql
   CREATE VIEW upcoming_upload_schedule AS
   SELECT uj.upload_job_id,
          uj.clip_id,
          uj.title,
          uj.scheduled_time,
          s.final_scheduled_time,
          s.status AS schedule_status
   FROM upload_jobs uj
   LEFT JOIN schedules s ON s.clip_id = uj.clip_id
   WHERE uj.status IN ('PENDING', 'SCHEDULED')
     AND (uj.scheduled_time >= now() OR s.final_scheduled_time >= now())
   ORDER BY COALESCE(s.final_scheduled_time, uj.scheduled_time);
   ```

## 5. Stardust & Metadata Integration
- Every worker emits a Stardust packet with `entity_type`/`entity_id` pointing to the affected row. This packet captures `_meta_parents`, evidence hashes, and decision context.
- `stardust_metadata` is the authoritative ledger; `lineage` stores upstream references, while `decision_chain` mirrors HaloLux reasoning nodes.
- `logs.metadata` mirrors critical Stardust identifiers so operators can pivot from logs to lineage quickly.
- Table-level metadata fields (e.g., `clips.metadata`, `edit_jobs.operations`) should embed the associated `stardust_id` when the record is created, ensuring contextual lookup without extra joins.

## 6. Storage Considerations
- **Asset storage**: Raw and rendered media files live in cloud object storage (e.g., GCS/S3) with VM local caches for hot files. `videos.file_path` and related URIs point to these buckets.
- **Retention policy**: Raw downloads retained for 90 days unless a clip is promoted; derived assets retained for 365 days or until an operator approves deletion. Stardust metadata and logs are never deleted, only archived.
- **Backups**: Perform nightly logical dumps plus streaming WAL archiving to cold storage. Materialized views should be refreshed post-restore.
- **Cleanup pipeline**: Scheduled job scans orphaned files (no DB references) and expired assets, deletes them from storage, and writes corresponding logs/Stardust entries documenting the cleanup decision.

## 7. Implementation Notes
- Prefer `JSONB` for flexible metadata while keeping core relational fields typed; enforce JSON schema validation at the application layer.
- Maintain strict foreign key constraints to prevent orphaned jobs; cascading deletes are avoided in favor of explicit archival workflows.
- Use UUIDv4 identifiers everywhere to avoid cross-region collisions and to simplify sharding.
- Store all timestamps in UTC (`TIMESTAMPTZ`) and convert at presentation time only.
- Apply role-based access controls so that cognitive services have read-only access except where mutation rights are explicitly required.
