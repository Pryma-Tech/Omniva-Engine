# Omniva Engine — Module Interfaces

## 1. Overview
Module interfaces are the canonical contracts that keep Omniva Engine’s cognitive and operational planes in sync. They define the envelopes that transport intent, state, and telemetry between subsystems so that each component can evolve independently without breaking the pipeline. Standardized interfaces deliver four guarantees:
1. Every subsystem speaks in predictable schemas, making orchestration deterministic.
2. Shared data formats and sequencing rules eliminate ad-hoc coupling between layers.
3. Cognitive guidance and operational execution remain observable through common metadata.
4. The Zenith Integrator can arbitrate the end-to-end flow with full traceability.

## 2. Message Schema Conventions
- **Envelope format**: JSON objects (or Python dictionaries that serialize 1:1 to JSON). Binary payloads are referenced through URIs and never embedded inline.
- **Field classification**: Schemas explicitly list `required` and `optional` fields. Optional fields must be omitted rather than set to `null` unless the receiving contract states otherwise.
- **Naming**: snake_case for field names, lowercase enums, singular nouns for object identifiers. Only adopt external naming when mirroring third-party APIs.
- **Timestamps**: Always ISO 8601 with UTC suffix (`YYYY-MM-DDTHH:MM:SSZ`). Sub-second precision is allowed but must be consistent per stream.
- **Unique identifiers**: UUIDv4 strings for all long-lived objects (`job_id`, `clip_id`, `video_id`). Composite IDs are discouraged unless documented.
- **Status flags**: `PENDING`, `RUNNING`, `DONE`, `ERROR`. Optional states (`CANCELLED`, `SKIPPED`) may be added but must be enumerated in the schema that introduces them.
- **Correlation metadata**: `_meta_parents` holds the lineage of Stardust packets that produced the message. `trace_id` (UUIDv4) links related emissions within a workflow.
- **Versioning**: `schema_version` (semantic version) increments on any backward-incompatible change. Modules must reject unknown major versions.

## 3. Core Data Structures
All primary internal objects follow Draft 2020-12 JSON Schema and disallow undeclared properties to ensure forward compatibility.

### 3.1 ScraperJob
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ScraperJob",
  "type": "object",
  "required": [
    "job_id",
    "creator_id",
    "platform",
    "target_url",
    "requested_range",
    "status",
    "created_at",
    "updated_at"
  ],
  "properties": {
    "job_id": { "type": "string", "format": "uuid", "description": "Stable identifier for the scrape request." },
    "creator_id": { "type": "string", "format": "uuid", "description": "Source requesting the scrape (user, workflow, or module)." },
    "platform": { "type": "string", "enum": ["tiktok", "instagram", "youtube", "other"], "description": "Origin network for the media assets." },
    "target_url": { "type": "string", "format": "uri", "description": "URL or channel handle to scrape." },
    "requested_range": {
      "type": "object",
      "required": ["since", "until"],
      "properties": {
        "since": { "type": "string", "format": "date-time" },
        "until": { "type": "string", "format": "date-time" }
      }
    },
    "status": { "type": "string", "enum": ["PENDING", "RUNNING", "DONE", "ERROR", "CANCELLED"] },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "default": "1.0.0" }
  },
  "additionalProperties": false
}
```

### 3.2 AnalysisResult
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AnalysisResult",
  "type": "object",
  "required": ["video_id", "transcript", "keywords_detected", "virality_score", "relevance_score", "clip_candidates"],
  "properties": {
    "video_id": { "type": "string", "format": "uuid" },
    "transcript": { "type": "string", "description": "Full transcript or ASR output." },
    "keywords_detected": { "type": "array", "items": { "type": "string" } },
    "virality_score": { "type": "number", "minimum": 0, "maximum": 1 },
    "relevance_score": { "type": "number", "minimum": 0, "maximum": 1 },
    "clip_candidates": { "type": "array", "items": { "$ref": "#/$defs/clip_candidate" } },
    "_meta_parents": { "type": "array", "items": { "type": "string", "format": "uuid" } },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "$defs": {
    "clip_candidate": { "$ref": "ClipCandidate.json" }
  },
  "additionalProperties": false
}
```

### 3.3 ClipCandidate
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ClipCandidate",
  "type": "object",
  "required": [
    "start_time",
    "end_time",
    "confidence",
    "subject_focus",
    "faces_detected",
    "semantic_tags",
    "pantheon_votes",
    "lattice_priority"
  ],
  "properties": {
    "start_time": { "type": "number", "minimum": 0, "description": "Seconds offset from video start." },
    "end_time": { "type": "number", "exclusiveMinimum": 0, "description": "Seconds offset; must be greater than start_time." },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "subject_focus": { "type": "string", "description": "High-level subject label (creator, guest, product, etc.)." },
    "faces_detected": { "type": "integer", "minimum": 0 },
    "semantic_tags": { "type": "array", "items": { "type": "string" }, "uniqueItems": true },
    "pantheon_votes": {
      "type": "object",
      "patternProperties": {
        "^[a-z_]+$": { "type": "number", "minimum": 0, "maximum": 1 }
      },
      "description": "Vote weight per Pantheon agent persona."
    },
    "lattice_priority": { "type": "number", "minimum": 0, "maximum": 1 },
    "clip_id": { "type": "string", "format": "uuid", "description": "Filled in when Zenith promotes the candidate." }
  },
  "additionalProperties": false
}
```

### 3.4 EditJob
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EditJob",
  "type": "object",
  "required": ["clip_id", "operations", "ffmpeg_commands", "gpu_required", "estimated_duration"],
  "properties": {
    "clip_id": { "type": "string", "format": "uuid" },
    "operations": { "type": "array", "items": { "type": "string" }, "description": "Ordered list of logical editing steps." },
    "ffmpeg_commands": { "type": "array", "items": { "type": "string" }, "description": "Concrete commands generated by the Editor planner." },
    "gpu_required": { "type": "boolean" },
    "estimated_duration": { "type": "integer", "minimum": 1, "description": "Seconds of wall time predicted." },
    "expected_outputs": { "type": "array", "items": { "type": "string", "format": "uri" }, "description": "Storage URIs for resulting assets." }
  },
  "additionalProperties": false
}
```

### 3.5 UploadJob
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "UploadJob",
  "type": "object",
  "required": ["clip_id", "title", "description", "keywords", "scheduled_time", "privacy_status"],
  "properties": {
    "clip_id": { "type": "string", "format": "uuid" },
    "title": { "type": "string", "maxLength": 120 },
    "description": { "type": "string", "maxLength": 5000 },
    "keywords": { "type": "array", "items": { "type": "string" }, "maxItems": 15 },
    "scheduled_time": { "type": "string", "format": "date-time" },
    "privacy_status": { "type": "string", "enum": ["public", "unlisted", "private"] },
    "yt_video_id": { "type": "string", "pattern": "^[A-Za-z0-9_-]{11}$" },
    "distribution_targets": { "type": "array", "items": { "type": "string" }, "description": "Secondary platforms for syndication." }
  },
  "additionalProperties": false
}
```

### 3.6 ScheduleTask
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ScheduleTask",
  "type": "object",
  "required": ["clip_id", "recommended_time", "priority", "horizon_adjustment", "final_decision_source"],
  "properties": {
    "clip_id": { "type": "string", "format": "uuid" },
    "recommended_time": { "type": "string", "format": "date-time" },
    "priority": { "type": "number", "minimum": 0, "maximum": 1 },
    "horizon_adjustment": { "type": "number", "minimum": -1, "maximum": 1, "description": "Offset from Horizon Engine relative weighting." },
    "final_decision_source": { "type": "string", "enum": ["zenith", "operator_override", "automation"], "description": "Who owns the ultimate call." },
    "notes": { "type": "string", "maxLength": 512 },
    "_meta_parents": { "type": "array", "items": { "type": "string", "format": "uuid" } }
  },
  "additionalProperties": false
}
```

## 4. Cognitive Module Interfaces
Each cognitive interface is written as an idempotent service contract: inputs arrive over the event bus, outputs are published back with lineage metadata, and Zenith consumes the consolidated context.

### 4.1 Paradox Engine Interface
- **Inputs**: Video metadata, clip metadata, worker state digests (`ScraperJob`, `AnalysisResult`, `EditJob` descriptors), and any prior conflict reports referenced via `_meta_parents`.
- **Outputs**: `conflict_resolution` documents describing duplicate detections, conflicting timestamps, or circular dependencies. Each payload includes severity, recommended action (`block`, `quarantine`, `ignore`), and affected identifiers.
- **Trigger Conditions**: Fired on new ingestion requests, scheduled audits (hourly), or when Atlas storage detects collisions.
- **Expected Behavior**: Evaluate lineage graphs for contradictions, flag mutually exclusive tasks before execution begins, and raise `ERROR` status only when the suggested action is to halt.
- **Notes for Implementers**: Treat Paradox guidance as advisory; it must not mutate job states directly. Include pointers to Stardust records so HaloLux can narrate root causes.

### 4.2 Eclipse Engine Interface
- **Inputs**: Worker error events, timeout alerts, abnormal log signatures, health check deviations, and hooks from Paradox when conflicts escalate.
- **Outputs**: Structured retry plans (per job with backoff configuration), fallback strategies (reroute to backup workers), and quarantine instructions that Zenith can enforce.
- **Trigger Conditions**: Consecutive failures above threshold, heartbeat gaps exceeding SLA, or manual operator panic button.
- **Expected Behavior**: Contain the blast radius of failures, isolate problematic workers, propose healing steps, and emit readiness signals when a cluster is safe again.
- **Notes for Implementers**: Attach actionable remediation metadata (e.g., `restart_required`, `cache_flush`). Eclipse should never execute system changes itself; operations are executed by orchestrator workers once Zenith approves.

### 4.3 Stardust Interface
- **Inputs**: Every event produced by Omniva modules with `_meta_parents`, plus operational telemetry that needs lineage tracking.
- **Outputs**: Immutable metadata packets persisted to the Stardust ledger, accessible through hash-addressable IDs for auditing and analytics.
- **Trigger Conditions**: Mandatory on each publish; no event may bypass Stardust.
- **Expected Behavior**: Provide verifiable chain-of-custody records, enforce schema validation, and surface inconsistencies to Paradox.
- **Notes for Implementers**: Keep payloads lean (references over blobs) and maintain bidirectional links so HaloLux can reconstruct reasoning chains quickly.

### 4.4 Lattice Router Interface
- **Inputs**: Analysis scores, workload distribution metrics, Horizon Engine goal gradients, and resource utilization stats from ops workers.
- **Outputs**: Job priority deltas, routing directives (e.g., assign to GPU-optimized editor pool), and semantic clustering hints for Pantheon.
- **Trigger Conditions**: Arrival of new `ClipCandidate`s, backlog threshold crossings, or strategy recalibration windows (every 10 minutes).
- **Expected Behavior**: Balance throughput vs. creative objectives by steering jobs toward the best-suited workers while keeping queue depths within SLA.
- **Notes for Implementers**: Output a monotonic `routing_sequence` to maintain ordering guarantees. Do not mutate worker state directly; provide intents that Zenith translates into commands.

### 4.5 Horizon Engine Interface
- **Inputs**: Long-term campaign goals, historical engagement logs, seasonality data, and reflective notes from Zenith’s previous cycles.
- **Outputs**: Adjusted scheduling weights, campaign trajectory recommendations, and early warnings when current output drifts from strategic intent.
- **Trigger Conditions**: Daily cadence, major goal updates, or when Horizon detects trend inflection.
- **Expected Behavior**: Smooth short-term volatility by nudging scheduler targets and providing Pantheon with long-range desirability metrics.
- **Notes for Implementers**: Ensure outputs are tagged with the `goal_window` they apply to so Zenith can scope decisions; keep models explainable enough for HaloLux to narrate the shifts.

### 4.6 Pantheon Interface
- **Inputs**: Clip candidates, scoring embeddings, Lattice context (workload + semantic buckets), and Horizon-provided goal biases.
- **Outputs**: Multi-agent vote reports capturing consensus, dissent, and rationale per persona. Includes standardized columns (`agent`, `vote`, `confidence`, `commentary`).
- **Trigger Conditions**: Each scoring batch, manual review requests, or whenever new Horizon guidance arrives.
- **Expected Behavior**: Refine clip prioritization by aggregating perspectives (risk mitigation, exploratory push, trend-chasing) and surface top candidates with justification.
- **Notes for Implementers**: Maintain reproducibility—identical inputs must yield identical votes unless models are versioned. Provide deterministic sorting for Zenith consumption.

### 4.7 Chorus Interface
- **Inputs**: Draft titles, descriptions, tags, and style preferences from Pantheon or operators; Paradox alerts for compliance concerns.
- **Outputs**: Refined stylistic metadata (tone-aligned titles/descriptions), plus style deltas indicating what changed and why.
- **Trigger Conditions**: Whenever a new UploadJob is prepared or creative guidelines shift.
- **Expected Behavior**: Normalize brand voice, enforce policy constraints, and highlight any unresolved compliance conflict.
- **Notes for Implementers**: Emit both human-readable and machine-readable forms so Uploader workers can use the same payload without further transformation.

### 4.8 HaloLux Interface
- **Inputs**: Decisions and evidence from all cognitive modules, operational worker telemetry, Stardust lineage IDs, and user queries from the dashboard.
- **Outputs**: Interpretability bundles (text narrative + JSON reasoning chain) that describe why a decision was made, what evidence was used, and what alternatives were discarded.
- **Trigger Conditions**: Operator requests, regulatory audits, anomaly escalations, or any Zenith decision flagged as high-impact.
- **Expected Behavior**: Provide transparent narratives in under 2 seconds, surface missing evidence, and score each explanation for completeness.
- **Notes for Implementers**: Keep explanations deterministic; cache by `trace_id` to avoid recomputation. HaloLux should never invent data—every statement references a Stardust packet.

### 4.9 Zenith Interface
- **Inputs**: Aggregated outputs from all cognitive modules, operational status feeds, and manual overrides from the dashboard.
- **Outputs**: Final execution directives targeted at operational workers, commitment logs for Stardust, and arbitration verdicts when modules disagree.
- **Trigger Conditions**: Every control cycle (default 30 seconds), arrival of high-priority jobs, or crisis escalations from Eclipse.
- **Expected Behavior**: Resolve conflicting advice, authorize or cancel operational work, assign ownership, and publish consistent state transitions.
- **Notes for Implementers**: Zenith’s contracts form the ultimate source of truth. Each command must reference the evidence it used and include rollback guidance so Eclipse can recover if execution fails.

## 5. Operational Module Interfaces
Operational workers consume Zenith commands, execute concrete work, and echo results back through Stardust before the orchestrator mutates global state.

### 5.1 Scraper Worker
- **Input contract**: Accepts `ScraperJob` plus optional `retry_plan` from Eclipse. Requires valid platform credentials resolved via secret store references, not inline tokens.
- **Output contract**: Emits `video_asset_created` events containing storage URIs, normalized metadata, and a seed `AnalysisResult` stub. Always references the originating `job_id`.
- **Error signaling**: Sets job status to `ERROR`, publishes failure reason codes (`network_timeout`, `rate_limited`, `auth_failed`), and alerts Eclipse when automatic retries are exhausted.
- **Stardust reference**: Every downloaded asset registers two lineage packets—one for the raw capture, one for metadata normalization.

### 5.2 Analyzer Worker
- **Input contract**: Consumes video artifacts referenced by URI, transcripts or ASR instructions, and the originating `ScraperJob`.
- **Output contract**: Publishes full `AnalysisResult` objects plus zero or more embedded `ClipCandidate`s. Generates embeddings stored separately with pointers.
- **Error signaling**: Reports parser or model failures with granular codes (`transcript_missing`, `model_offline`) and downgrades status to `ERROR` so Lattice can reprioritize.
- **Stardust reference**: Links each clip candidate to the raw asset packet and the analysis model version for reproducibility.

### 5.3 Editor Worker
- **Input contract**: Receives `EditJob` definitions with resolved `ClipCandidate` IDs and storage references. Requires idempotent `editing_context_id` to safeguard retries.
- **Output contract**: Produces rendered assets (URI list), `edit_summary` metadata, and duration metrics for Horizon.
- **Error signaling**: Distinguishes between deterministic (`bad_command`) and transient (`gpu_starvation`) failures; escalates the latter to Eclipse for reroute.
- **Stardust reference**: Stores operation graphs that list executed FFmpeg commands and hardware characteristics to support future forensic review.

### 5.4 Uploader Worker
- **Input contract**: Takes `UploadJob` plus Chorus-refined metadata. Expects signed tokens resolved from secret manager at run time.
- **Output contract**: Confirms publishing status (`SCHEDULED`, `LIVE`), platform response IDs (`yt_video_id`), and final scheduled slot.
- **Error signaling**: Emits structured errors (`quota_exceeded`, `content_violation`), attaches supporting evidence to HaloLux, and requests Zenith direction on whether to retry.
- **Stardust reference**: Writes one packet per platform submission, referencing both the asset URI and Chorus payload for post-mortem traceability.

### 5.5 Scheduler Worker
- **Input contract**: Consumes `ScheduleTask` objects alongside current queue snapshots from Zenith.
- **Output contract**: Issues queue mutation events (`scheduled`, `rescheduled`, `skipped`) and wall-clock commitments per clip.
- **Error signaling**: Publishes `scheduler_fault` when constraints conflict (e.g., double booking) and invites Paradox to validate duplicates.
- **Stardust reference**: Captures every schedule change and links it to the Horizon goal window that motivated it.

### 5.6 Dashboard
- **Input contract**: Aggregates metrics from operational workers, HaloLux explanations, and Stardust lineage digests. Supports streaming updates for near real-time monitoring.
- **Output contract**: Sends operator approvals, overrides, or guidance messages (e.g., manual priority change) routed through Zenith for enforcement.
- **Error signaling**: Displays UI-level alerts, pushes `operator_alert` events when manual review is required, and records them for HaloLux narratives.
- **Stardust reference**: Operator actions are first-class packets so future audits can replay decision paths exactly.

## 6. Inter-Layer Message Flow Table
| Cognitive Module | Operational Target | Purpose |
|------------------|--------------------|---------|
| Lattice Router | Analyzer Worker | Prioritize which videos enter deep analysis based on semantic load and worker availability. |
| Pantheon | Editor Worker | Highlight high-value clip candidates for editing with rationale from multi-agent votes. |
| Horizon Engine | Scheduler Worker | Adjust posting cadence and slot selection according to long-term goals. |
| Eclipse Engine | Any Worker Pool | Deliver recovery guidance, retries, or quarantines when failures occur. |
| Paradox Engine | Scraper Worker | Prevent duplicate ingestion and enforce mutually exclusive scrape policies. |
| Chorus | Uploader Worker | Provide finalized metadata packages for publishing. |
| HaloLux | Dashboard | Surface reasoning chains and traceability to operators. |
| Zenith | All Operational Workers | Issue binding commands that change system state. |

## 7. Implementation Notes
- Interfaces are backward-compatible contracts; schema changes require explicit version bumps and migration plans.
- Cognitive modules emit advisory signals—only Zenith can commit or cancel operational work, ensuring a single authority for state transitions.
- Every operational output must traverse Stardust before the orchestrator updates persistent state, preserving lineage and enabling HaloLux explainability.
- Traceability is mandatory: include `_meta_parents`, `trace_id`, and `schema_version` on all messages so downstream modules can validate provenance.
- Modules should remain idempotent; retries triggered by Eclipse must not lead to duplicate side effects if the same message is processed twice.
