# Omniva Engine — Workers Specification

## 1. Overview
Workers form the operational backbone of Omniva Engine. Each worker owns a major phase of the clipfarm pipeline and runs asynchronously so the platform can ingest, transform, and publish content in parallel. Workers pull tasks from queues, execute deterministic steps, and emit state updates to the primary database, logs, and Stardust for lineage. Cognitive modules influence worker behavior via Zenith-issued directives that encapsulate priorities, retry rules, and configuration. The active worker set:
- Scraper Worker
- Analyzer Worker
- Editor Worker
- Uploader Worker
- Scheduler Worker

## 2. Worker Architecture Model

### 2.1 Execution Model
- Workers are stateless processes or containers; any local cache is ephemeral.
- Each worker type listens to its dedicated task queue and pulls jobs when capacity allows.
- After processing, workers persist results to the relational database, upload artifacts to file storage, and publish Stardust packets documenting lineage.
- Retry limits and exponential backoff are respected per job; accumulated failures escalate to Eclipse for intervention.

### 2.2 Task Message Contract
- Tasks are JSON-like envelopes with required fields: `job_id`, `task_type`, `payload`, `priority`, `trace_id`, `created_at`.
- Payloads embed resource identifiers (e.g., `video_id`, `clip_id`), asset paths/URIs, configuration flags, and deadlines.
- Status transitions follow a standard lifecycle: `PENDING` → `RUNNING` → (`DONE` | `ERROR` | `CANCELLED`). Intermediate states (e.g., `WAITING_RETRY`) are optional but must be documented in the module interface.
- Each task includes `_meta_parents` linking back to prior Stardust entries for provenance.

### 2.3 Failure Handling
- Workers trap exceptions, capture stderr/stdout, and publish structured error events.
- Eclipse Engine consumes error events, applies policy (retry up to N, exponential backoff, reroute to alternate pool, or quarantine), and notifies Zenith.
- When quarantine is triggered, the worker stops pulling new jobs and reports unhealthy until manual or automated remediation succeeds.
- Tasks that exceed retry limits are marked `ERROR` with root-cause metadata for HaloLux to expose.

## 3. Worker Specifications

### 3.1 Scraper Worker
- **Purpose**: Download posts and media from TikTok, Instagram Reels, and YouTube Shorts, normalize metadata, and seed downstream processing.
- **Inputs**: `creator_id`, `platform`, scraping window (`since`, `until`), user-defined settings (max videos, include captions, proxy config), credentials references.
- **Outputs**: Raw video files in object storage, new rows in `posts` and `videos`, initial Stardust lineage entries linking creator → post → video.
- **State Machine**: `INIT` → `FETCH` (call platform API) → `PARSE` (normalize metadata) → `SAVE` (write DB + storage) → `DONE` or `ERROR`.
- **Data Structures**: Consumes `ScraperJob`; emits `video_asset_created` events referencing `posts`, `videos`.
- **Cognitive Interactions**: Paradox pre-checks duplicates/hard conflicts; Lattice schedules scraping order; Eclipse handles rate-limit retries and proxy rotation; Zenith authorizes final job dispatch.
- **Example Flow**: Worker pulls job for creator X TikTok past 7 days, fetches feed, hashes media, detects two new posts, writes DB entries, uploads MP4s, emits Stardust packets.
- **Error Cases**: HTTP 429 (rate limited) → backoff, `invalid_credentials` → escalate, checksum mismatch → re-download then quarantine if persistent.

### 3.2 Analyzer Worker
- **Purpose**: Transform videos into structured insights: transcripts, keywords, semantic tags, virality/relevance scores, and clip candidates.
- **Inputs**: `video_id`, file path/URI, `raw_metadata`, optional model override parameters.
- **Outputs**: `AnalysisResult` records, `ClipCandidate[]`, embeddings stored in feature store, Stardust entries capturing model versions.
- **State Machine**: `INIT` → `TRANSCRIBE` (ASR) → `NLP_ANALYSIS` (keywords, sentiment) → `CLIP_DETECTION` (candidate extraction) → `SAVE` (persist results) → `DONE`/`ERROR`.
- **Data Structures**: `AnalysisResult`, `ClipCandidate`, `ModelRunMetadata`.
- **Cognitive Interactions**: Lattice boosts/demotes task priority; Pantheon consumes candidates and feeds votes back; Stardust logs the reasoning chain; Zenith uses completion signals to trigger EditJobs.
- **Example Flow**: Job pulls `video_id=abc`, runs Whisper large, generates transcript with confidence 0.91, computes virality=0.78, extracts six candidates, writes to DB, emits events for Pantheon.
- **Error Cases**: ASR timeout → fallback model; corrupt media → request re-scrape; NLP model offline → Eclipse reroutes to backup deployment.

### 3.3 Editor Worker
- **Purpose**: Create fully processed short-form clips using automated editing operations.
- **Operations**: Smart autocut, cropping/reframing, face tracking, audio cleanup, FFmpeg rendering, caption overlay (optional).
- **Inputs**: `clip_id`, associated `EditJob` containing operations, FFmpeg command sequence, GPU requirement flag, destination URIs.
- **Outputs**: Final rendered clip files stored in object storage, edit summaries, performance metrics, Stardust packets describing command graph.
- **State Machine**: `INIT` → `CUT` (autocut/filler trims) → `REFINE` (reframe, overlays) → `RENDER` (FFmpeg) → `STORE` (upload asset, update DB) → `DONE`/`ERROR`.
- **Data Structures**: `EditJob`, `RenderedAsset`, `EditSummary`.
- **Cognitive Interactions**: Lattice prioritizes queue order; Horizon may supply style presets; Eclipse manages FFmpeg failures and GPU pool health; Zenith approves job start/stop.
- **Example Flow**: Worker receives EditJob with operations `[autocut, reframe, captions]`, executes commands via FFmpeg+Python, uploads 1080x1920 MP4, posts success to queue, logs to Stardust.
- **Error Cases**: GPU OOM → reroute to CPU fallback with lower resolution; FFmpeg exit code non-zero → capture stderr, trigger retry; storage upload failure → attempt 3 times before escalation.

### 3.4 Uploader Worker
- **Purpose**: Publish finished clips to YouTube (and eventually other platforms) with compliant metadata.
- **Inputs**: `UploadJob` referencing `clip_id`, metadata (title, description, keywords), thumbnail info, scheduled time, privacy settings.
- **Outputs**: YouTube video ID, status updates (`SCHEDULED`, `LIVE`), confirmation of playlist assignments, Stardust entries capturing API responses.
- **State Machine**: `INIT` → `AUTH` (refresh OAuth) → `UPLOAD` (videos.insert) → `VERIFY` (confirm processing & schedule) → `DONE`/`ERROR`.
- **Data Structures**: `UploadJob`, `PlatformResponse`.
- **Cognitive Interactions**: Chorus provides refined copy; Horizon influences scheduling parameters; HaloLux documents reasoning for dashboard; Zenith coordinates release order; Eclipse handles quota errors.
- **Example Flow**: Worker pulls UploadJob, refreshes OAuth token, uploads file via resumable endpoint, sets metadata/thumbnail, schedules publish time, updates DB with `yt_video_id`.
- **Error Cases**: Quota exceeded → reschedule per Eclipse instructions; metadata violation → Paradox/HaloLux alert; network failure mid-upload → resume session within TTL.

### 3.5 Scheduler Worker
- **Purpose**: Assign optimal posting times to pending clips while honoring quotas and Horizon strategy.
- **Logic**: Evaluates per-creator quotas (e.g., 1–10 clips/day), global platform limits, and engagement windows; applies Horizon adjustments for long-term pacing; avoids collisions/oversaturation.
- **Inputs**: Pending `UploadJob`s/`ScheduleTask`s, historical engagement data (future), Horizon directives, queue states from Zenith.
- **Outputs**: `ScheduleTask` entries, updates to `upload_jobs.scheduled_time`, notifications to Zenith and Dashboard.
- **State Machine**: `INIT` → `CALCULATE` (score candidate slots) → `COMMIT` (write schedule, emit events) → `DONE` (or `ERROR` if conflicts unsolved).
- **Data Structures**: `ScheduleTask`, `QueueSnapshot`.
- **Cognitive Interactions**: Horizon provides long-term pacing targets; Zenith commits decisions; Lattice may request priority bumps for urgent clips; HaloLux exposes scheduling rationale.
- **Example Flow**: Worker pulls queue snapshot, finds open slot tomorrow 16:00, writes ScheduleTask with Horizon weight adjustments, updates UploadJob, emits Stardust packet referencing reasoning.
- **Error Cases**: No feasible slot due to conflicting constraints → emit `scheduler_fault`, request Horizon guidance; DB contention → retry with exponential backoff; stale data → refresh snapshot.

## 4. Queueing Model Details
- Recommended implementation: Redis-backed queues (RQ/Celery) or cloud-native equivalents (Pub/Sub, SQS) per deployment; each worker type has its own queue key for isolation.
- Task messages include priority scores from Lattice; workers pop highest-priority jobs first when the queue backend supports it.
- Backpressure: When queue depth exceeds configured thresholds, Zenith slows upstream job creation, and Lattice reduces new dispatches until downstream catches up.
- TTL: Stale jobs older than configurable window (default 24h) are auto-expired and logged; Zenith or operators may reissue if still relevant.

## 5. Logging, Monitoring, and Stardust Interaction
- Every worker action produces structured logs (JSON) with `trace_id`, `job_id`, `worker_type`, `status`, and relevant metrics; logs funnel into the centralized `logs` table and external observability stack.
- Stardust integrates at key checkpoints: job start, major state transitions, completion/failure. Each packet references entity IDs so HaloLux can reconstruct reasoning.
- Metrics: latency per stage, success/error counts, retry counts, system resource utilization reported to Prometheus/Grafana dashboards.

## 6. Worker Scaling Strategy
- Horizontal scaling: add more worker instances per type based on queue depth, CPU/GPU usage, and SLA targets.
- Editor workers run in dedicated GPU pools with resource-aware scheduling; Analyzer ASR jobs may also leverage GPUs depending on model choice.
- Auto-scaling rules: trigger scale-out when queue latency exceeds threshold (e.g., 5 minutes) or utilization >70%; scale-in when idle for sustained intervals.
- Failure isolation: Eclipse monitors health signals and can remove individual workers from rotation, rerouting tasks and notifying operators.

## 7. Example End-to-End Worker Chain
1. **Scraper Worker** ingests new videos for a creator and records them in the database with Stardust lineage.
2. **Analyzer Worker** processes the videos, generating transcripts and 12 clip candidates.
3. **Pantheon + Lattice** (cognitive layer) evaluate candidates, promoting the top 4; Zenith issues corresponding EditJobs.
4. **Editor Worker** renders the promoted clips, uploading finalized assets and updating statuses.
5. **Uploader Worker** publishes two clips immediately and prepares UploadJobs for the remaining two with scheduled times.
6. **Scheduler Worker** assigns optimal posting windows for pending clips, aligning with Horizon’s pacing.
7. Throughout the chain, **Stardust** captures each transition, enabling HaloLux and the Dashboard to display complete provenance and status.

