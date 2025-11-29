# Omniva Engine — API Endpoints Reference (v1)

All endpoints are rooted at `/v1/` and return the standard wrapper shown in the API Overview (`status`, `data`, `error`, `meta`). Only the `data` object is shown below for brevity.

## 1. Projects

### GET /v1/projects
- **Description**: List all projects visible to the caller.
- **Request**: query params `limit` (default 50), `offset` (default 0), optional `status`.
- **Response**:
```json
{
  "items": [
    {
      "project_id": "proj_123",
      "name": "BusinessAI",
      "status": "RUNNING",
      "videos_scraped": 42,
      "clips_ready": 135,
      "created_at": "2024-04-01T10:00:00Z"
    }
  ],
  "pagination": { "limit": 50, "offset": 0, "total": 18 }
}
```
- **Error cases**: `400 INVALID_PAGINATION`.
- **Example request**: `GET /v1/projects?limit=20&status=RUNNING`.

### POST /v1/projects
- **Description**: Create a new project and initialize default settings.
- **Request**:
```json
{
  "name": "CreatorLab",
  "description": "Education niche automation",
  "default_platforms": ["tiktok", "youtube_shorts"],
  "scrape_window_days": 7
}
```
- **Response**:
```json
{
  "project_id": "proj_456",
  "status": "PAUSED",
  "created_at": "2024-05-01T09:12:00Z"
}
```
- **Error cases**: `400 VALIDATION_ERROR` (missing name), `409 PROJECT_EXISTS`.
- **Example**: `POST /v1/projects`.

### GET /v1/projects/{project_id}
- **Description**: Fetch project metadata, settings, and aggregate metrics.
- **Response**:
```json
{
  "project_id": "proj_123",
  "name": "BusinessAI",
  "status": "RUNNING",
  "settings": {
    "scrape_window_days": 7,
    "daily_quota": 5,
    "keywords": ["ai", "automation"]
  },
  "stats": {
    "creators": 6,
    "videos_scraped": 42,
    "clips_in_pipeline": 18,
    "uploads_pending": 4
  }
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

### POST /v1/projects/{project_id}/start
- **Description**: Start all workers assigned to the project (Zenith issues commands).
- **Request**:
```json
{ "reason": "scheduled_start" }
```
- **Response**:
```json
{ "message": "Project proj_123 scheduled to start.", "requested_at": "2024-05-07T12:00:00Z" }
```
- **Error cases**: `409 ALREADY_RUNNING`, `404 PROJECT_NOT_FOUND`.

### POST /v1/projects/{project_id}/stop
- **Description**: Gracefully stop workers and pause automation.
- **Request**:
```json
{ "reason": "manual_pause" }
```
- **Response**:
```json
{ "message": "Project proj_123 stopping.", "requested_at": "2024-05-07T12:05:00Z" }
```
- **Error cases**: `409 ALREADY_STOPPED`, `404 PROJECT_NOT_FOUND`.

---

## 2. Creators

### POST /v1/projects/{project_id}/creators
- **Description**: Attach a creator/channel to a project.
- **Request**:
```json
{
  "platform": "tiktok",
  "handle": "@creatorlab",
  "profile_url": "https://tiktok.com/@creatorlab",
  "scrape_window_days": 7
}
```
- **Response**:
```json
{
  "creator_id": "cr_789",
  "platform": "tiktok",
  "status": "ACTIVE"
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`, `409 CREATOR_EXISTS`, `422 INVALID_HANDLE`.

### GET /v1/projects/{project_id}/creators
- **Description**: List creators for the project.
- **Response**:
```json
{
  "items": [
    {
      "creator_id": "cr_789",
      "platform": "tiktok",
      "handle": "@creatorlab",
      "status": "ACTIVE",
      "last_scraped_at": "2024-05-06T20:00:00Z"
    }
  ]
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

---

## 3. Scraping

### POST /v1/projects/{project_id}/scrape
- **Description**: Trigger immediate scraping for all or a subset of creators.
- **Request**:
```json
{
  "creator_ids": ["cr_789", "cr_101"],
  "since": "2024-05-01T00:00:00Z",
  "until": "2024-05-07T00:00:00Z",
  "force": false
}
```
- **Response**:
```json
{
  "job_id": "scrape_job_001",
  "queued_creators": 2,
  "status": "QUEUED"
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`, `400 INVALID_DATE_RANGE`.

### GET /v1/projects/{project_id}/scrape/status
- **Description**: Return most recent scraping job statuses/logs.
- **Response**:
```json
{
  "jobs": [
    {
      "job_id": "scrape_job_001",
      "creator_id": "cr_789",
      "status": "DONE",
      "videos_downloaded": 4,
      "started_at": "2024-05-07T12:05:00Z",
      "completed_at": "2024-05-07T12:07:10Z"
    }
  ]
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

---

## 4. Analysis

### GET /v1/projects/{project_id}/analysis
- **Description**: Paginated analysis results for the project.
- **Query params**: `clip_status`, `min_score`, `limit`, `offset`.
- **Response**:
```json
{
  "items": [
    {
      "analysis_id": "an_123",
      "video_id": "vid_456",
      "virality_score": 0.83,
      "relevance_score": 0.77,
      "keywords": ["ai", "workflow"],
      "clip_candidates": [
        { "clip_id": "clip_1", "start_time": 45.2, "end_time": 72.1, "confidence": 0.92 }
      ]
    }
  ],
  "pagination": { "limit": 25, "offset": 0, "total": 210 }
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

---

## 5. Clips

### GET /v1/projects/{project_id}/clips
- **Description**: List clips and their current pipeline status.
- **Response**:
```json
{
  "items": [
    {
      "clip_id": "clip_1",
      "video_id": "vid_456",
      "status": "READY_FOR_EDIT",
      "confidence": 0.92,
      "semantic_tags": ["guest_quote"],
      "pantheon_votes": { "strategist": 0.91, "guardian": 0.65 }
    }
  ]
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

### GET /v1/clips/{clip_id}
- **Description**: Detailed metadata plus linked jobs.
- **Response**:
```json
{
  "clip_id": "clip_1",
  "project_id": "proj_123",
  "video_id": "vid_456",
  "status": "EDITING",
  "metadata": {
    "start_time": 45.2,
    "end_time": 72.1,
    "confidence": 0.92,
    "semantic_tags": ["guest_quote", "call_to_action"]
  },
  "edit_job": { "edit_job_id": "edit_22", "status": "RUNNING" },
  "upload_job": null
}
```
- **Error cases**: `404 CLIP_NOT_FOUND`.

---

## 6. Editing

### POST /v1/clips/{clip_id}/edit
- **Description**: Force creation of an EditJob for the clip (overrides automatic scheduling).
- **Request**:
```json
{
  "operations": ["autocut", "reframe", "captions"],
  "priority": "high",
  "gpu_required": true
}
```
- **Response**:
```json
{
  "edit_job_id": "edit_22",
  "status": "QUEUED",
  "clip_id": "clip_1"
}
```
- **Error cases**: `404 CLIP_NOT_FOUND`, `409 EDIT_ALREADY_IN_PROGRESS`.

---

## 7. Uploading

### POST /v1/clips/{clip_id}/upload
- **Description**: Create an UploadJob with optional metadata overrides.
- **Request**:
```json
{
  "title": "5-Second Productivity Reset",
  "description": "Top tip from episode 42.",
  "keywords": ["productivity", "routine"],
  "scheduled_time": "2024-05-10T16:00:00Z",
  "privacy_status": "unlisted"
}
```
- **Response**:
```json
{
  "upload_job_id": "up_45",
  "status": "QUEUED",
  "clip_id": "clip_1"
}
```
- **Error cases**: `404 CLIP_NOT_FOUND`, `409 UPLOAD_EXISTS`, `400 INVALID_SCHEDULE`.

### GET /v1/projects/{project_id}/uploads
- **Description**: List upload jobs along with platform responses.
- **Response**:
```json
{
  "items": [
    {
      "upload_job_id": "up_45",
      "clip_id": "clip_1",
      "status": "SCHEDULED",
      "yt_video_id": "abc123xyz45",
      "scheduled_time": "2024-05-10T16:00:00Z"
    }
  ]
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

---

## 8. Scheduling

### POST /v1/projects/{project_id}/schedule
- **Description**: Force recalculation of schedule based on current queue/Horizon inputs.
- **Request**:
```json
{ "reason": "manual_rebalance", "target_day": "2024-05-12" }
```
- **Response**:
```json
{
  "jobs_considered": 8,
  "updated": 4,
  "status": "QUEUED"
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`, `409 SCHEDULER_BUSY`.

### GET /v1/projects/{project_id}/schedule
- **Description**: List scheduled uploads with calendar data.
- **Response**:
```json
{
  "items": [
    {
      "clip_id": "clip_1",
      "upload_job_id": "up_45",
      "recommended_time": "2024-05-10T16:00:00Z",
      "final_time": "2024-05-10T16:05:00Z",
      "status": "CONFIRMED"
    }
  ]
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

---

## 9. Logs

### GET /v1/projects/{project_id}/logs
- **Description**: Filtered log view.
- **Query params**: `source`, `level`, `from`, `to`, `worker_type`, `limit`.
- **Response**:
```json
{
  "items": [
    {
      "log_id": "log_556",
      "timestamp": "2024-05-07T12:06:00Z",
      "source": "scraper_worker",
      "level": "INFO",
      "message": "Downloaded 4 videos",
      "metadata": { "creator_id": "cr_789" }
    }
  ]
}
```
- **Error cases**: `404 PROJECT_NOT_FOUND`.

---

## 10. Cognitive Insights (HaloLux)

### GET /v1/clips/{clip_id}/insights
- **Description**: Retrieve interpretability data for a clip.
- **Response**:
```json
{
  "clip_id": "clip_1",
  "trace_id": "trace_001",
  "insights": {
    "paradox": { "conflicts": [] },
    "lattice": { "priority": 0.82, "reason": "under-indexed topic" },
    "pantheon": [
      { "agent": "strategist", "vote": 0.91, "comment": "high novelty" },
      { "agent": "guardian", "vote": 0.65, "comment": "moderate virality" }
    ],
    "horizon": { "goal_alignment": "WEEK6_DIVERSITY" },
    "zenith": { "decision": "EDIT_UPLOAD_APPROVED" }
  },
  "raw_payload": { "...": "..." }
}
```
- **Error cases**: `404 CLIP_NOT_FOUND`, `409 HALOLUX_PENDING`.

---

## 11. System

### GET /v1/system/status
- **Description**: Report health of workers, queues, DB, and cognitive layer.
- **Response**:
```json
{
  "workers": {
    "scraper": { "status": "HEALTHY", "queue_depth": 2 },
    "editor": { "status": "DEGRADED", "queue_depth": 7 }
  },
  "queues": { "redis": "connected" },
  "database": { "status": "HEALTHY", "replication_lag_ms": 20 },
  "cognitive_layer": { "status": "HEALTHY", "last_heartbeat": "2024-05-07T12:10:00Z" }
}
```
- **Error cases**: `500 STATUS_UNAVAILABLE`.

---

## 12. Example Payloads

### Project Creation
**Request**
```http
POST /v1/projects
Content-Type: application/json

{
  "name": "FitnessGuru",
  "description": "Shorts automation for coaches",
  "default_platforms": ["youtube_shorts"]
}
```
**Response**
```json
{
  "status": "success",
  "data": { "project_id": "proj_987", "status": "PAUSED" },
  "error": null,
  "meta": { "request_id": "req_001" }
}
```

### Add Creator
```http
POST /v1/projects/proj_987/creators
{
  "platform": "youtube_shorts",
  "handle": "@coachamy"
}
```
**Response**
```json
{
  "status": "success",
  "data": { "creator_id": "cr_202", "status": "ACTIVE" }
}
```

### Trigger Scrape
```http
POST /v1/projects/proj_987/scrape
{
  "creator_ids": ["cr_202"],
  "force": true
}
```
**Response**
```json
{
  "status": "success",
  "data": { "job_id": "scrape_job_010", "status": "QUEUED" }
}
```

### Fetch Logs
```http
GET /v1/projects/proj_987/logs?source=editor_worker&level=ERROR&limit=20
```
**Response**
```json
{
  "status": "success",
  "data": {
    "items": [
      { "log_id": "log_880", "timestamp": "2024-05-07T10:00:00Z", "message": "FFmpeg crash", "metadata": { "clip_id": "clip_99" } }
    ]
  }
}
```

### HaloLux Reasoning
```http
GET /v1/clips/clip_99/insights
```
**Response**
```json
{
  "status": "success",
  "data": {
    "clip_id": "clip_99",
    "trace_id": "trace_900",
    "insights": {
      "pantheon": [
        { "agent": "strategist", "vote": 0.88, "comment": "aligns with campaign" }
      ],
      "zenith": { "decision": "SCHEDULE_APPROVED" }
    }
  }
}
```

All responses include `error` and `meta` fields even when omitted from samples.
