# Omniva Engine — Unified Reference v0.1

## Table of Contents

- [📘 Omniva Engine — Documentation Overview](#-omniva-engine-documentation-overview)
- [📘 Omniva Engine — System Overview](#-omniva-engine-system-overview)
- [📘 Omniva Engine — System Architecture](#-omniva-engine-system-architecture)
- [📘 Omniva Engine — Cognitive Architecture](#-omniva-engine-cognitive-architecture)
- [📘 Omniva Engine — Module Interfaces](#-omniva-engine-module-interfaces)
- [📘 Omniva Engine — Data Models](#-omniva-engine-data-models)
- [📘 Omniva Engine — Technical Specification (v0.1)](#-omniva-engine-technical-specification-v01)
- [📘 Omniva Engine — Clipfarm Pipeline Specification](#-omniva-engine-clipfarm-pipeline-specification)
- [📘 Omniva Engine — Workers Specification](#-omniva-engine-workers-specification)
- [📘 Omniva Engine — Dashboard & UI Specification](#-omniva-engine-dashboard-ui-specification)
- [📘 Omniva Engine — API Overview](#-omniva-engine-api-overview)
- [📘 Omniva Engine — API Endpoints Reference (v1)](#-omniva-engine-api-endpoints-reference-v1)
- [📘 Omniva Engine — Engineering Roadmap](#-omniva-engine-engineering-roadmap)

---
# 📘 Omniva Engine — Documentation Overview
_Sourced from: docs/README.md_
---

# Omniva Engine — Documentation Overview

## 1. Introduction
Omniva Engine is a fully autonomous, AI-powered clipfarming system that ingests long-form creator content and publishes optimized shorts with no manual babysitting. It fuses a cognitive architecture—nine Omniva modules that reason about priorities, conflicts, and strategy—with an operational pipeline that executes scraper → analyzer → editor → uploader → scheduler loops. The system is engineered for fire-and-forget operation, delivering high reliability, observability, and interpretability through Stardust lineage and HaloLux insights.

## 2. Key Features
- Multi-platform scraping (TikTok, Instagram Reels, YouTube Shorts)
- AI-driven clip detection and scoring
- Automated video editing (smart autocut, reframing, audio cleanup)
- Automatic YouTube uploading and scheduling
- Full metadata and provenance tracking via Stardust
- Crisis recovery orchestration (Eclipse Engine)
- Multi-agent refinement for clip relevance (Pantheon)
- Interpretability layer (HaloLux) for reasoning traces
- Operator dashboards + comprehensive API surface

## 3. Repository Structure
```
omniva-engine/
├── api/
├── dashboard/
├── workers/
│   ├── scraper/
│   ├── analyzer/
│   ├── editor/
│   ├── uploader/
│   └── scheduler/
├── database/
├── config/
├── utils/
├── static/
├── tests/
└── docs/
    ├── architecture/
    ├── specifications/
    ├── api/
    └── README.md
```

## 4. Documentation Index

### Core Docs
- **Omniva Engine Overview** (`docs/omniva_engine_overview.md`): Executive summary of goals, components, and flow.
- **System Architecture** (`docs/architecture/system_architecture.md`): High-level diagrams, deployment topologies.
- **Cognitive Architecture** (`docs/architecture/cognitive_architecture.md`): Deep dive on the nine modules.
- **Module Interfaces** (`docs/architecture/module_interfaces.md`): Schemas and contracts for cognitive/operational communication.
- **Data Models** (`docs/architecture/data_models.md`): Relational schema definitions and lineage relationships.

### Specs
- **Omniva Engine Spec v0.1** (`docs/specifications/omniva_engine_spec_v0.1.md`)
- **Clipfarm Pipeline Spec** (`docs/specifications/clipfarm_pipeline_spec.md`)
- **Workers Spec** (`docs/specifications/workers_spec.md`)
- **Dashboard/UI Spec** (`docs/specifications/dashboard_spec.md`)

### API Docs
- **API Overview** (`docs/api/api_overview.md`)
- **Endpoints Reference** (`docs/api/endpoints_reference.md`)

## 5. Getting Started (Developer Setup)
1. **Clone the repo**
   ```bash
   git clone git@github.com:omniva/omniva-engine.git
   cd omniva-engine
   ```
2. **Install dependencies** (Python 3.11+, FastAPI, Pydantic, Celery/RQ, FFmpeg, moviepy)
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables**: copy `.env.example`, set DB credentials, Redis URL, API secrets.
4. **Setup YouTube OAuth credentials**: create OAuth client, place secrets in `config/credentials/`.
5. **Run database migrations** (e.g., Alembic):
   ```bash
   alembic upgrade head
   ```
6. **Start services**
   ```bash
   uvicorn api.main:app --reload
   python workers/scraper/worker.py
   # repeat for analyzer/editor/uploader/scheduler as needed
   ```

## 6. Running the System
- **Start scraping**: via dashboard bot controls or `POST /v1/projects/{id}/scrape`.
- **Observe job queues**: Redis UI, Celery flower, or dashboard worker panel.
- **Outputs**: rendered clips land in configured object storage; UploadJobs record platform IDs.
- **Dashboard URL**: `http://localhost:3000` (or deployment-specific host).
- **Logs**: centralized `logs` table + `logs/` directory + observability stack (Prometheus/Grafana/Loki).

## 7. Expanding Omniva
- **New workers**: scaffold under `workers/<name>/`, register with Zenith, add queue + config entries, update workers spec.
- **Extend cognitive modules**: add advisory services under `backend/app/subsystems/`, expose outputs via module interface schemas.
- **New data sources**: implement scraper adapters, extend data models, add platform credentials, update dashboard forms.
- **Future features**: integrate subtitle generators, B-roll injectors, AI voiceovers by augmenting EditJobs and Editor worker operations.

## 8. Contributing
- **Coding standards**: follow PEP 8 for Python, ESLint/Prettier for frontend, type hints everywhere.
- **Branch naming**: `feature/<ticket>`, `bugfix/<ticket>`, `docs/<topic>`.
- **PR workflow**: open against `main`, include description + screenshots/logs, request review from subsystem owners.
- **Testing**: run unit + integration suites (`pytest`, worker smoke tests, API contract tests) before submitting PRs.

## 9. License
TBD — see forthcoming `LICENSE` file or contact Omniva legal for guidance.

---
# 📘 Omniva Engine — System Overview
_Sourced from: docs/omniva_engine_overview.md_
---

# Omniva Engine — System Overview

## 1. Purpose
Omniva Engine is a hybrid cognitive + operational automation platform that manages autonomous clip-farming workflows end-to-end. It fuses advanced reasoning subsystems (Pantheon, Horizon, Paradox, etc.) with concrete pipeline workers (scraper, analyzer, editor, uploader, scheduler) to orchestrate large-scale short-form content generation without manual intervention.

## 2. System Objectives
- Fully autonomous video-to-clip pipeline
- High reliability via cognitive subsystems (Paradox, Eclipse, Infinity, Zenith)
- Intelligent prioritization through semantic routing and lattice fabrics
- Transparent metadata lineage via the Stardust graph
- Interpretable decision behavior powered by HaloLux
- Long-horizon continuity and purpose alignment through Horizon
- Multi-agent decision refinement with Pantheon archetypes

## 3. High-Level Capabilities
- Multi-platform scraping (TikTok, Instagram Reels, YouTube Shorts)
- AI-driven analysis, transcript generation, and clip scoring
- Automated video editing pipeline (rendering, branding, captioning)
- Auto-uploading plus scheduling optimization for optimal audience windows
- Branding and title/description automation aligned with Chorus/Horizon signals
- Metadata tracking with Stardust to maintain provenance for every clip and decision
- Crisis-mode recovery through Infinity (autoscaling) + Eclipse (failsafe rituals)

## 4. Architectural Overview
```
[Cognitive Layer]
  - Paradox Engine
  - Eclipse Engine
  - Stardust Layer
  - Lattice Router
  - Horizon Engine
  - Pantheon Agents
  - Chorus Harmonizer
  - HaloLux Interpretability
  - Zenith Integrator

↓ Controls / Guides / Monitors ↓

[Operational Layer]
  - Scraper Worker
  - Analyzer Worker
  - Editor Worker
  - Uploader Worker
  - Scheduler Worker
  - Dashboard UI
  - Database + Metadata Store
```

## 5. Cognitive–Operational Interaction
- Paradox continuously checks for conflicting jobs, duplicate timestamps, or drift spikes before operational execution.
- Eclipse coordinates soft rebuilds, subsystem resets, and full reboot rituals after worker or node failures.
- Stardust attaches metadata packets to every pipeline action, preserving lineage for each produced clip.
- Lattice routes priorities and semantic relationships, ensuring downstream workers receive context-aware jobs.
- Horizon tracks project-level goals and long-horizon objectives that bias scheduling and strategy selection.
- Pantheon archetypes vote on clip importance, risk appetite, and exploration preferences before scheduling.
- Chorus harmonizes the emotional tone used for titles, descriptions, and creative assets across workers.
- HaloLux exposes interpretability hooks so operators can inspect reasoning chains for any decision.
- Zenith aggregates messages from cognitive subsystems, computing coherence scores and reflection reports to keep operations aligned.

## 6. Example End-to-End Flow
1. User adds creators and project configuration via the dashboard.
2. Scraper workers download recent videos from TikTok/IG/YouTube.
3. Analyzer workers transcribe footage, run AI scoring, and pass candidate clips to strategy.
4. Pantheon agents evaluate scoring, refining priorities with archetype voting and Chorus modulation.
5. Editor workers render clips with FFmpeg, applying templates, captions, and branding.
6. Uploader workers post finalized clips to YouTube and other platforms.
7. Scheduler optimizes posting times using Oracle forecasts and Horizon goals.
8. Stardust records full provenance for every step, linking packets across the Lattice fabric.
9. HaloLux provides a reasoning chain so operators can review why each clip was produced and scheduled.

---
# 📘 Omniva Engine — System Architecture
_Sourced from: docs/architecture/system_architecture.md_
---

# Omniva Engine — System Architecture

## 1. High-Level Description
Omniva Engine operates as an autonomous short-form clip-farming platform that orchestrates the entire pipeline from creator discovery to branded clip distribution. The system is divided into two cohesive strata:
- **Cognitive Layer** (Pantheon, Horizon, Paradox, Chorus, HaloLux, etc.): provides reasoning, self-checks, interpretability, and long-horizon oversight.
- **Operational Layer** (workers, pipelines, schedulers, dashboard): executes scraping, analysis, editing, uploading, and reporting tasks.
This architecture allows Omniva to remain scalable, resilient, and interpretable while continuously running large volumes of clip-production workflows.

## 2. End-to-End Workflow
1. **User initializes a project** via the dashboard, defining brand requirements and content constraints.
2. **Creator links are added** (TikTok, Instagram Reels, YouTube Shorts) and persisted to the project store.
3. **Scraper worker fetches recent posts** for each creator, storing raw media artifacts and metadata.
4. **Analyzer processes videos**, extracts transcripts, identifies clip candidates, and computes virality + relevance scores.
5. **Pantheon agents refine selection** by applying multi-agent weighting over the analyzer’s scores.
6. **Editor worker** pulls the prioritized clips and performs automated editing (FFmpeg, templates, captions, branding).
7. **Uploader publishes to YouTube** (or other targets) using platform APIs.
8. **Scheduler determines optimal posting times** leveraging Oracle/Horizon signals and queues future jobs.
9. **Stardust logs full metadata and lineage** so every clip has end-to-end provenance and semantic links.
10. **Dashboard displays progress** (foreground + background metrics, incidents, throughput) in near real time.

## 3. Architecture Diagram (Text-Based)
```
[Cognitive Layer]
   Paradox — Eclipse — Stardust — Lattice — Horizon — Pantheon — Chorus — HaloLux — Zenith

↓ Orchestration / Strategy / Metadata ↓

[Operational Layer]
   Scraper → Analyzer → Editor → Uploader → Scheduler → Dashboard
                    ↓
           Database / Metadata Store
```

```arduino
         ┌─────────────────────────────────────────┐
         │              COGNITIVE LAYER             │
         │─────────────────────────────────────────│
         │ Paradox  |  Eclipse  |  Stardust        │
         │ Lattice  |  Horizon  |  Pantheon        │
         │ Chorus   |  HaloLux  |  Zenith          │
         └──────────────────────────┬──────────────┘
                                    │ Controls / Guidance
                                    ▼
     ┌───────────────────────────────────────────────────────────┐
     │                  OPERATIONAL LAYER                        │
     │───────────────────────────────────────────────────────────│
     │ Scraper → Analyzer → Editor → Uploader → Scheduler       │
     └──────────────────────────┬────────────────────────────────┘
                                │
                                ▼
                   ┌────────────────────────┐
                   │   Database / Metadata   │
                   │   Logs / Stardust       │
                   └────────────────────────┘
```

## 4. Worker Queue Model
- **Worker Types**: scraper, analyzer, editor, uploader, scheduler, discovery, governance maintenance.
- **Queue Architecture**: Redis-backed priority queues (Celery/RQ style) with per-worker namespaces and sharded channels for horizontal scale.
- **Message Format**: JSON payload including job_id, project_id, artifact references, priority, retries, metadata parents (for Stardust).
- **Retry Logic**: exponential backoff with capped retries (e.g., 3 attempts). Paradox/Eclipse mark failed jobs for manual inspection.
- **Timeout Logic**: job-level timeouts enforced by worker runtime; long-running tasks (rendering, upload) have extended windows with heartbeat checks.
- **Distributed Processing**: workers are stateless; they pull jobs from shared queues and persist results to the database and object storage. Scaling simply adds more worker containers or nodes.

## 5. State Machines
- **Scraper**: `INIT → FETCH → PARSE → SAVE → DONE / ERROR`
- **Analyzer**: `INIT → TRANSCRIBE → SCORE → CLIP-FIND → DONE / ERROR`
- **Editor**: `INIT → CUT → REFINE → RENDER → DONE / ERROR`
- **Uploader**: `INIT → AUTH → UPLOAD → VERIFY → DONE / ERROR`
- **Scheduler**: `INIT → CALC → ENQUEUE → DONE`
Each state machine emits structured events (start, transition, completion, failure) which flow into Stardust & HaloLux for provenance and interpretability.

## 6. Database Layer Overview
- **Core Tables**: `projects`, `creators`, `posts`, `videos`, `clips`, `jobs`, `job_logs`, `artifacts`, `metadata_packets`.
- **Query Flows**: read-heavy queries for dashboards use indexed views; writers use batched inserts to minimize contention.
- **Indexing Strategy**: composite indexes on `(project_id, creator_id)`, timestamps (`posted_at`, `scheduled_at`), and job states. Clips table indexes `status`, `priority`, and `lineage_id` to accelerate scheduling and provenance queries.
- **Relationships**: each clip references a source video, derived job entries, and Stardust packets; jobs reference worker type and project; metadata packets store parent-child relationships linking to Lattice.

## 7. Logging & Observability
- **Structured Logs**: JSON logs emitted by every worker & subsystem, tagged with job_id/project_id.
- **Log Levels**: DEBUG for development, INFO for runtime operations, WARN for recoverable anomalies, ERROR/FATAL for escalations triggered via Eclipse.
- **Error Propagation**: failures bubble to Paradox (consistency), Eclipse (recovery orchestration), and Infinity (scaling signals). Alerts propagate to the dashboard.
- **Telemetry + Metrics**: Prometheus-compatible counters/gauges (queue depth, throughput, failures, render time); Grafana dashboard consumption.
- **Interpretability Hooks**: HaloLux attaches reasoning chains, and Stardust captures metadata packets for all events.
- **Dashboard Integration**: UI consumes aggregated metrics/logs to visualize health, throughput, and issues.

## 8. Scalability Model
- **Horizontal Scaling**: add worker containers/nodes; all subsystems are stateless or rely on shared databases/object stores.
- **Stateless Workers**: no local session required; state persisted to DB + storage ensures resilience.
- **GPU Nodes**: editor/render workers can target GPU-enabled nodes for heavy workloads.
- **Throughput Control**: scheduler and Infinity loop adjust job injection rates based on load score; limiter prevents overload.
- **Graceful Degradation**: Paradox + Eclipse throttle high-risk operations, Infinity scales down gracefully, and Horizon adjusts goals when resources tighten, ensuring the system remains stable under stress.

---
# 📘 Omniva Engine — Cognitive Architecture
_Sourced from: docs/architecture/cognitive_architecture.md_
---

# Omniva Engine — Cognitive Architecture

## 1. Overview
The Omniva cognitive layer is a meta-reasoning system that supervises, guides, optimizes, and stabilizes the entire clip-farming engine. It sits above the operational workers, constantly evaluating coherence, enforcing recovery, refining prioritization, surfacing interpretability signals, and projecting long-horizon strategy. This layer orchestrates dozens of subsystems to maintain performance, reliability, and transparency at scale.

```
[Cognitive Layer]
  Paradox | Eclipse | Stardust | Lattice | Horizon | Pantheon | Chorus | HaloLux | Zenith
        ↓ Controls / Guides / Monitors ↓
[Operational Layer]
  Scraper → Analyzer → Editor → Uploader → Scheduler
```

## 2. The Nine Cognitive Modules (Omniva Subsystems)
Each module exposes advisory signals, listens to shared events, and influences operational decisions through Zenith.

### 2.1 Paradox Engine
- **Responsibility**: Detect temporal inconsistencies, duplicate media, conflicting worker states, drift spikes.
- **Input Signals**: Worker telemetry, job state transitions, Oracle drift/stress, Stardust metadata.
- **Output Signals**: Anomaly flags, blocking advisories, recovery tickets.
- **When It Activates**: On job creation/completion, conflict detection, periodic scans.
- **Integration Points**: Scheduler (prevent enqueue), workers (halt job), Zenith (escalate to Eclipse).
- **Example Behavior**: Paradox detects two identical clip jobs scheduled simultaneously and issues a block + Stardust log.

### 2.2 Eclipse Engine
- **Responsibility**: Crisis handling, retries, subsystem reset rituals, node quarantine.
- **Input Signals**: Paradox crisis flags, Infinity scaling telemetry, worker failure events.
- **Output Signals**: Soft rebuild triggers, subsystem reset commands, full reboot rituals, quarantine list.
- **When It Activates**: After critical worker errors, when Paradox raises severe anomalies, scheduled resilience checks.
- **Integration Points**: Scheduler queues, worker orchestrator, event bus, Zenith resolution flow.
- **Example Behavior**: Analyzer worker crash triggers Eclipse to pause that queue, reroute jobs, and publish recovery status.

### 2.3 Stardust Metadata Layer
- **Responsibility**: End-to-end provenance graph from source post → clip candidates → decisions → edits → uploads → engagement.
- **Input Signals**: Event bus events (job start/end, scoring, rendering, upload). Each payload provides metadata parents.
- **Output Signals**: Metadata packets, Lattice link references, audit queries for dashboard + HaloLux.
- **When It Activates**: On every event bus publish.
- **Integration Points**: All workers, Lattice fabric, HaloLux explanations, dashboard provenance view.
- **Example Behavior**: Editor completion event generates Stardust packet linking raw video, analyzer decision, and final render artifact.

### 2.4 Lattice Mesh Router
- **Responsibility**: Maintain semantic priorities, align worker tasks, route clip scoring & scheduling weights.
- **Input Signals**: Oracle forecasts, Astral futures, Infinity load states, Stardust metadata links, Pantheon recommendations.
- **Output Signals**: Routing updates, priority adjustments, semantic graph edges, job hints for scheduler.
- **When It Activates**: On project forecast refresh, new clip candidates, queue rebalancing, manual overrides.
- **Integration Points**: Scheduler, analyzer/editor weighting, HaloLux interpretability, Zenith integration.
- **Example Behavior**: New high-engagement trend detected, Lattice boosts connected clips and pushes them to the front of the editor queue.

### 2.5 Horizon Engine
- **Responsibility**: Long-horizon strategy (cadence, niche direction, growth targets, content diversity goals) and goal alignment metrics.
- **Input Signals**: Oracle trends, project performance metrics, Pantheon voting history, scheduler outcomes.
- **Output Signals**: Epoch goals, alignment scores, strategic biases communicated to Zenith and Lattice.
- **When It Activates**: On epoch transitions, weekly planning windows, goal adjustments requested by operators.
- **Integration Points**: Scheduler (posting windows), discovery engine (creator expansion), Pantheon weighting, Zenith reflection.
- **Example Behavior**: Horizon detects under-served educational content; updates bias so Pantheon and Lattice prioritize such clips.

### 2.6 Pantheon Multi-Agent Layer
- **Responsibility**: Council of archetypal agents voting on clip priority, topic suitability, and strategic fit.
- **Input Signals**: Analyzer scores, Horizon goals, Chorus tone guidance, Lattice semantics, project context.
- **Output Signals**: Consensus vectors (risk, explore, stability, creativity), per-clip recommendations, weight adjustments.
- **When It Activates**: For each batch of candidate clips, during strategy recalibration, before scheduler finalization.
- **Integration Points**: Strategy engine, scheduler, Zenith integrator, HaloLux explanations.
- **Example Behavior**: Pantheon votes down a clip misaligned with brand tone, rerouting resources to a better candidate.

### 2.7 Chorus Engine
- **Responsibility**: Maintain tonal consistency for generated text (titles, descriptions, keywords, branding suggestions).
- **Input Signals**: Pantheon consensus, Oracle stress/drift, Horizon goals, Paradox anomaly counts.
- **Output Signals**: Emotional field + modulation (risk, exploration, focus adjustments) fed to text generators and strategy.
- **When It Activates**: During metadata generation, when emotional state changes, nightly harmonization cycles.
- **Integration Points**: Text generators, uploader metadata pipeline, dashboard copy previews, HaloLux emotional context.
- **Example Behavior**: Elevated stress triggers Chorus to recommend calmer titles and toned-down descriptions.

### 2.8 HaloLux Interpretability Layer
- **Responsibility**: Provide structured explanations for clip scoring, worker decisions, failures, and long-term strategy.
- **Input Signals**: Lightfield snapshots (Pantheon, Chorus, Horizon, Oracle, Astral, Strategy, Infinity, Paradox, Lattice, Stardust).
- **Output Signals**: Explainable reasoning chains, cross-layer influence maps, API responses consumed by dashboard.
- **When It Activates**: On user request, audit events, anomaly investigations, scheduled transparency reports.
- **Integration Points**: Dashboard UI, logging pipeline, operator tooling, compliance reporting.
- **Example Behavior**: HaloLux surfaces why clip ABC was prioritized (Pantheon risk vote + Chorus excitement + Oracle trend spike).

### 2.9 Zenith Integrator
- **Responsibility**: Master orchestrator consolidating outputs from all cognitive subsystems, resolving conflicts, and issuing final directives.
- **Input Signals**: Coherence scores, recommendations, anomaly notices, modulation vectors, strategic goals.
- **Output Signals**: Final decisions for scheduler/strategy, coherence metrics, reflection reports.
- **When It Activates**: Every control cycle, on decision requests, after major subsystem updates.
- **Integration Points**: Scheduler, workers, dashboard, HaloLux interpretability, Infinity scaling.
- **Example Behavior**: Zenith merges Pantheon consensus with Horizon pacing, overrides conflicting analyzer advice, and dispatches final job orders.

## 3. Interaction Model
Cognitive modules communicate through:
- **Event Bus**: async dispatch of JSON-like payloads (job events, anomalies, decisions, recovery notices).
- **Shared Registry Access**: modules fetch snapshots from other subsystems as needed.
- **Triggers**: job completion, worker error, scheduler tick, manual UI command, or periodic cron tasks.
- **Payload Schema**: includes job_id/project_id, type, context, priority, `_meta_parents` for Stardust linking.

## 4. Cognitive Loop Cycle
1. **Monitor worker states** (Infinity telemetry, heartbeat events).
2. **Gather metadata** (Stardust packets, Lattice updates).
3. **Evaluate potential issues** (Paradox anomaly checks).
4. **Route decisions** (Lattice fabric assigns priorities).
5. **Apply agent consensus** (Pantheon voting/weights).
6. **Update long-term trajectory** (Horizon goals + alignment).
7. **Ensure stylistic harmony** (Chorus modulation for text/branding).
8. **Emit interpretability insights** (HaloLux explanations, dashboard hooks).
9. **Integrate and finalize** (Zenith coherence, directives to operational layer).

```markdown
               ┌────────────────────────────────┐
               │        Cognitive Loop          │
               └────────────────────────────────┘


┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────┐
│ Stardust │ → │ Paradox │ → │ Lattice │ → │ Pantheon │
└──────────┘ └───────────┘ └──────────┘ └──────────┘
▲ │ │ │
│ ▼ ▼ ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
│ Logs     │ │ Eclipse  │ │ Horizon  │ │ Chorus      │
└──────────┘ └──────────┘ └──────────┘ └────────────┘
│
▼
┌────────────┐
│ HaloLux     │
└────────────┘
▼
┌────────────┐
│ Zenith      │
└────────────┘
▼
Final Cognitive Output
```

## 5. Example Walkthroughs
### Example A — Duplicate Clip Detected
Paradox detects duplicate job → logs via Stardust → Lattice reroutes tasks to new clips → Zenith issues a directive canceling the duplicate and scheduling a replacement.

### Example B — Analyzer Worker Failure
Analyzer crashes → Eclipse triggers retries/fallback → Paradox marks job anomaly → HaloLux documents the failure chain → Zenith pauses the analyzer queue and alerts operations.

### Example C — Selecting Best Clip
Analyzer proposes scores → Pantheon votes on importance → Horizon checks goal alignment → Chorus refines tone for metadata → Zenith finalizes the schedule entry → Stardust records lineage.

## 6. Implementation Notes
- Cognitive modules are implemented as Python classes registered with the subsystem registry.
- Modules emit advisory signals only; they do not directly execute operational commands.
- Operational workers consume finalized directives exclusively from Zenith (or scheduler orchestrator), ensuring a single source of truth.

---
# 📘 Omniva Engine — Module Interfaces
_Sourced from: docs/architecture/module_interfaces.md_
---

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

---
# 📘 Omniva Engine — Data Models
_Sourced from: docs/architecture/data_models.md_
---

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

---
# 📘 Omniva Engine — Technical Specification (v0.1)
_Sourced from: docs/specifications/omniva_engine_spec_v0.1.md_
---

# Omniva Engine — Technical Specification (v0.1)

## 1. Introduction
Omniva Engine is a hybrid orchestration platform that combines a cognitive control plane with an operational clipfarm pipeline. The cognitive architecture provides reasoning, prioritization, and interpretability; the operational layer executes scraping, analysis, editing, uploading, and scheduling at scale. Omniva exists to autonomously source long-form content, extract the best short-form clips, and publish them reliably with minimal human intervention.

Design goals:
- **Autonomy**: Cognitive subsystems collaborate to make end-to-end decisions without manual babysitting.
- **Resilience**: Built-in fault detection, isolation, and retry loops keep the pipeline healthy in hostile environments.
- **Interpretability**: Every action is traceable through Stardust so operators can understand and audit decisions.
- **Modularity**: Cognitive modules and workers evolve independently behind stable interfaces, enabling rapid iteration.

## 2. System Overview
Omniva Engine is organized as two tightly coupled layers:
- **Cognitive Layer**: Nine specialized subsystems (Paradox, Eclipse, Stardust, Lattice, Horizon, Pantheon, Chorus, HaloLux, Zenith) exchange signals on an event bus. They evaluate data quality, set priorities, reason about risk, and produce commands.
- **Operational Layer**: Workers (Scraper, Analyzer, Editor, Uploader, Scheduler), shared infrastructure (Database, File Storage), and the Dashboard act on Zenith’s directives to modify real-world state.

### End-to-End Flow
1. **Ingestion**: Scraper pulls creator posts into storage and records them in the database.
2. **Analysis**: Analyzer transcribes and scores videos, emitting clip candidates.
3. **Decision Making**: Cognitive modules coordinate on which clips to pursue, how to edit them, and when to post.
4. **Production**: Editor renders final clips according to EditJob specs.
5. **Distribution**: Uploader publishes to YouTube (and future platforms) with Chorus-refined metadata.
6. **Scheduling**: Scheduler aligns posting times with Horizon and Zenith guidance.
7. **Telemetry**: Stardust and logs capture every step so HaloLux can narrate the reasoning chain.

## 3. Components

### 3.1 Cognitive Components
| Module | Purpose | Inputs | Outputs | Activation Triggers | Interactions | Operational Impact |
|--------|---------|--------|---------|---------------------|--------------|--------------------|
| **Paradox** | Detect duplicates, conflicts, or circular dependencies before work is executed. | Video metadata, clip metadata, worker states, Stardust lineage. | Conflict reports with severity + recommended actions. | New ingestion events, scheduled audits, anomaly alerts. | Feeds Eclipse and Zenith when conflicts block progress; references Stardust for evidence. | Prevents wasted compute and conflicting jobs, protecting Scraper and Scheduler. |
| **Eclipse** | Crisis manager for worker failures and infrastructure faults. | Worker errors, heartbeats, Paradox escalations, telemetry. | Retry plans, fallback strategies, quarantine directives. | Consecutive failures, heartbeat gaps, manual panic signals. | Coordinates with Zenith to pause queues; notifies Scheduler to hold tasks; logs data for HaloLux. | Ensures Editors/Uploaders recover safely without cascading outages. |
| **Stardust** | Provenance ledger that records every event and decision. | All module outputs, worker telemetry, `_meta_parents`. | Immutable metadata packets, lineage graphs. | Each publish event. | Supplies HaloLux with evidence; referenced by Paradox, Zenith, Dashboard. | Guarantees interpretability and auditability end-to-end. |
| **Lattice** | Semantic router optimizing workload distribution and priorities. | Analysis scores, workload metrics, Horizon goals, worker capacity. | Priority adjustments, routing hints, clustering metadata. | New clip candidates, backlog threshold breaches. | Informs Pantheon on context; provides Zenith with ordering hints. | Keeps Analyzer/Editor queues balanced and aligned with strategy. |
| **Horizon** | Strategic planner maintaining long-term campaign goals. | Historical engagement, campaign objectives, Zenith retrospectives. | Adjusted scheduling weights, trend warnings, goal alignment scores. | Daily cadence, major goal updates, trend shifts. | Influences Pantheon, Scheduler, and Lattice; referenced by Zenith for final arbitration. | Prevents short-term optimizations from derailing long-term targets. |
| **Pantheon** | Multi-agent voting ensemble ranking clip candidates. | Clip metadata, Lattice context, Horizon biases, analysis embeddings. | Vote reports with per-agent scores, consensus level, rationale. | Each scoring batch or manual evaluation request. | Shares results with Zenith and Chorus; provides data to HaloLux. | Determines which clips advance to editing and uploading. |
| **Chorus** | Stylistic and compliance refinement for metadata. | Draft titles/descriptions, Pantheon context, Paradox alerts. | Brand-aligned titles, descriptions, keyword suggestions, diff reports. | When UploadJob is prepared or creative guidelines change. | Feeds Uploader; references Pantheon and Paradox guidance. | Ensures published clips match tone and policy requirements. |
| **HaloLux** | Interpretability surface for operators. | Stardust lineage, cognitive decisions, worker telemetry, user queries. | Human-readable narratives, machine-readable reasoning chains. | On-demand queries, audits, anomalies. | Pulls data from all modules; pushes summaries to Dashboard. | Provides transparency so operators can trust automation. |
| **Zenith** | High-order orchestrator making final decisions and issuing commands. | Outputs from all cognitive modules and operational status. | Authoritative commands to workers, arbitration logs, rollback guidance. | Continuous control cycles, urgent events, manual overrides. | Consumes Paradox/Eclipse alerts, Lattice priorities, Pantheon votes, Horizon goals, Chorus copy, HaloLux context. | Ensures the operational layer executes coherent, conflict-free plans. |

### 3.2 Operational Components
| Component | Responsibilities | Inputs | Outputs | Error Conditions | Links to Cognitive Modules |
|-----------|------------------|--------|---------|------------------|-----------------------------|
| **Scraper Worker** | Fetch creator posts, download media, normalize metadata. | `ScraperJob` directives from Zenith, platform credentials, retry plans from Eclipse. | Stored media files, populated `posts`/`videos`, logs/Stardust packets. | Rate limits, auth failures, media corruption. | Paradox prevents duplicate work; Eclipse provides retries; Stardust logs each capture. |
| **Analyzer Worker** | Generate transcripts, keywords, clip candidates. | Video URIs, `AnalysisResult` templates, guidance from Lattice/Pantheon. | `analysis` rows, candidate clips, model metadata. | Missing assets, model downtime, timeout. | Lattice sets priority; Pantheon consumes outputs; Stardust records inference lineage. |
| **Editor Worker** | Produce final clips via FFmpeg/automation. | `EditJob` specs, clip metadata, Pantheon scores. | Rendered clip files, edit summaries, telemetry. | GPU starvation, invalid commands, storage errors. | Eclipse triggers retries; Zenith issues jobs; Stardust logs FFmpeg graph. |
| **Uploader Worker** | Publish clips to YouTube (and future platforms). | `UploadJob` payloads, Chorus-refined metadata, tokens. | Platform responses, schedule confirmations, logs. | API quotas, policy violations, metadata conflicts. | Horizon influences scheduling; Paradox flags compliance issues; HaloLux references logs for interpretability. |
| **Scheduler Worker** | Determine and apply final posting slots. | `ScheduleTask` directives, Horizon weights, queue state. | Scheduled commitments, reschedules, notifications. | Double booking, horizon conflicts, queue overflow. | Receives strategy from Horizon; commands originate in Zenith; HaloLux narrates adjustments. |
| **Dashboard** | Operator console for monitoring and overrides. | Aggregated status, HaloLux explanations, Stardust lineage. | Manual overrides, approvals, annotations. | UI latency, stale data. | HaloLux supplies insights; Zenith receives overrides; Stardust ties actions to history. |
| **Database** | Authoritative store for relational entities (creators, posts, clips, jobs). | Worker writes, cognitive annotations. | Queryable state for all modules, transactional guarantees. | Deadlocks, replication lag. | All modules depend on consistent schemas; Stardust references PKs. |
| **File Storage** | Durable storage for raw and processed media. | Uploads from Scraper/Editor, references from DB. | Signed URLs, lifecycle policies, integrity checks. | Bucket unavailability, checksum mismatch. | Scraper, Editor, Uploader rely on it; Paradox uses checksums to detect duplicates. |

## 4. Internal Flows

### 4.1 Cognitive Flow
1. **Stardust** records new ingestion or analysis events.
2. **Paradox** inspects lineage for duplicates/conflicts.
3. **Lattice** adjusts routing weights so high-value work progresses.
4. **Pantheon** votes on clip quality and relevance.
5. **Horizon** evaluates strategy alignment and nudges priorities.
6. **Chorus** prepares compliant metadata once clips near upload stage.
7. **Eclipse** stands by to react if any worker or module faults.
8. **HaloLux** captures the reasoning chain for interpretability.
9. **Zenith** consolidates all signals, resolves disagreements, and sends commands to workers.

### 4.2 Operational Flow
1. **Scraper** ingests creator posts and stores media + metadata.
2. **Analyzer** produces transcripts, keywords, and clip candidates.
3. **Editor** renders final clips based on EditJobs.
4. **Uploader** stages metadata, uploads clips, and confirms publish status.
5. **Scheduler** commits posting times aligning with Horizon guidance.
6. **Dashboard** presents live status, allowing operators to intervene.

### 4.3 Error Flow (Crisis Mode)
- When a worker fails, **Eclipse** consumes error telemetry, classifies severity, and drafts a retry plan (exponential backoff, alternate worker, or quarantine).
- Eclipse notifies **Zenith**, which pauses conflicting queues and authorizes retries.
- If repeated faults occur, the worker is isolated; workloads are rerouted to healthy nodes.
- **Paradox** double-checks for upstream conflicts, while **HaloLux** generates a narrative that links the failure, retries, and final outcome for operator review.
- Stardust records each failure, retry, and resolution for audit purposes.

### 4.4 Metadata & Lineage Flow
- Every ingestion, analysis, edit, upload, and schedule mutation emits a **Stardust** packet referencing the relevant entity (video, clip, job).
- Lineage captures source video → clip → edit job → upload job → schedule, enabling full traceability.
- Decision-chain metadata records why a clip was selected, what votes supported it, what edits were executed, and how it was scheduled.
- Logs reference the corresponding `stardust_id` so operators can pivot from runtime events to immutable provenance.

## 5. Module Interfaces
Omniva modules communicate through structured JSON contracts. Cognitive modules emit advisory outputs (e.g., Pantheon vote reports, Lattice priority deltas, Chorus metadata packages) that Zenith consumes. Zenith translates the aggregated advice into operational commands (`ScraperJob`, `EditJob`, `UploadJob`, `ScheduleTask`). Operational workers respond with status updates, metrics, and error signals that feed back into Stardust and are available to cognitive modules. See `docs/architecture/module_interfaces.md` for the canonical schemas and API expectations.

## 6. Data Models (Summary)
The relational schema centers on:
- `creators` → `posts` → `videos` → `analysis` → `clips`
- Downstream job tables: `edit_jobs`, `upload_jobs`, `schedules`
- Supporting observability: `stardust_metadata`, `logs`

ASCII relationship summary:
```
creators ──< posts ──< videos ──< analysis ──< clips ──< edit_jobs ──< upload_jobs ──< schedules
             \──< logs                 \──< stardust_metadata
```
Full schemas live in `docs/architecture/data_models.md`.

## 7. Use Cases

### Use Case 1 — Detecting the Best Clip
1. Analyzer emits clip candidates for a new video.
2. Lattice elevates candidates from underrepresented topics.
3. Pantheon’s agents vote; consensus highlights a clip with high virality and relevance.
4. Horizon confirms the clip fits the long-term campaign mix.
5. Zenith approves an `EditJob` and `UploadJob` for that clip, referencing Pantheon’s rationale in Stardust.

### Use Case 2 — Worker Failure Recovery
1. Editor encounters an FFmpeg crash while rendering.
2. Eclipse receives error telemetry, generates a retry plan with new hardware constraints, and quarantines the failing node.
3. Zenith pauses additional EditJobs on that worker and reassigns the job according to Eclipse’s instructions.
4. Stardust logs the failure, retry, and resolution; HaloLux publishes an interpretability narrative for operators.

### Use Case 3 — Scheduling Optimization
1. Scheduler proposes a posting time based on queue availability.
2. Horizon evaluates engagement history and recommends shifting to a better window.
3. Zenith reconciles Scheduler’s proposal with Horizon’s advice and commits the final time; Stardust records the decision chain.

## 8. Example Executions
1. **Viral Clip Pipeline**  
   - Input: New podcast episode URL.  
   - Cognitive chain: Stardust records ingestion → Paradox clears conflicts → Lattice boosts clips featuring guest X → Pantheon votes highlight a 45-second segment → Horizon confirms alignment → Chorus polishes metadata → Zenith issues Edit/Upload commands.  
   - Operational action: Scraper downloads, Analyzer scores, Editor renders, Uploader posts, Scheduler schedules.  
   - Result: Clip published with full lineage logged.
2. **Failure Recovery**  
   - Input: EditJob fails due to GPU outage.  
   - Cognitive chain: Eclipse detects repeated timeout → Paradox verifies no duplicate job → HaloLux captures narrative.  
   - Operational action: Zenith reroutes job to backup Editor, Scheduler delays dependent uploads.  
   - Result: Clip produced after single retry; operators receive explanation.
3. **Strategy Adjustment**  
   - Input: Horizon detects over-indexing on one niche.  
   - Cognitive chain: Horizon lowers priority weight → Lattice redistributes routing → Pantheon votes shift to diverse clips → Zenith updates scheduling plan.  
   - Operational action: Scheduler reprioritizes queue; Uploader staggers releases accordingly.  
   - Result: Content mix rebalanced while maintaining throughput.

## 9. Operational Guidelines
- **Retry strategies**: Workers must support idempotent retries with exponential backoff provided by Eclipse; all commands include `trace_id` for deduplication.
- **Extensibility**: New cognitive modules should emit advisory outputs conforming to the module interface contract; new workers must integrate with Zenith commands and Stardust logging.
- **Deployment**: Prefer containerized workers with rolling updates and health checks; cognitive services should be stateless with persistent state externalized to the database and Stardust.
- **Logging/Monitoring**: Workers log structured JSON referencing `stardust_id`; metrics flow to centralized observability (Prometheus/Grafana). Alerts integrate with Eclipse for automated remediation.
- **Safety**: Zenith is the only component allowed to mutate operational state; manual overrides route through Dashboard with full audit logging. Sensitive credentials live in secret managers.
- **Versioning**: Schemas and interfaces use semantic versioning. Backward-incompatible changes require coordination across cognitive and operational teams plus migration plans.

## 10. Future Extensions
- **Pantheon v2 Multi-Agent Expansion**: Introduce additional personas and reinforcement signals to improve clip selection diversity.
- **Real-time Analytics**: Stream engagement telemetry back into Lattice/Horizon for faster feedback loops.
- **Automatic Niche Drift Correction**: Detect when content deviates from target audience and auto-adjust priorities.
- **Cross-Platform Scheduling**: Extend Scheduler/Uploader to TikTok, Instagram, and upcoming platforms with platform-aware policies.
- **Advanced Editing Workflows**: Integrate automatic subtitle generation, B-roll insertion, and AI voiceovers into EditJobs for richer output.
- **Adaptive Orchestration**: Allow Zenith to renegotiate resource allocation based on cost/performance factors in real time.

---
# 📘 Omniva Engine — Clipfarm Pipeline Specification
_Sourced from: docs/specifications/clipfarm_pipeline_spec.md_
---

# Omniva Engine — Clipfarm Pipeline Specification

## 1. Overview
The clipfarm pipeline is the operational backbone of Omniva. It autonomously converts long-form creator videos into optimized short-form clips by linking workers, shared infrastructure, and the Omniva cognitive layer. The cognitive subsystems prioritize sources, validate quality, and enforce strategy, while the pipeline executes scrape → analyze → edit → upload → schedule without manual touch points.

## 2. Pipeline Stages

### 2.1 Scraping & Ingestion
- **Supported platforms**: TikTok, Instagram Reels, YouTube Shorts (extensible via platform adapters).
- **Behavior**:
  - TikTok: Pulls creator feed via private API wrapper, respecting rate limits.
  - Instagram Reels: Uses authenticated session with paging markers.
  - YouTube Shorts: Fetches channel feed or playlist, downloading shorts under 90 seconds.
- **Download rules**: Default window is past 7 days per creator; configurable overrides let Zenith widen or narrow the window based on Horizon strategy.
- **Duplicate detection**: Each media file is hashed (SHA-256). Existing checksums in `videos.checksum` prevent re-downloading; Paradox uses these hashes to flag duplicates across creators.
- **Metadata extraction**: Captions, posted_at timestamps, platform IDs, engagement counters, and hashtags stored in `posts.raw_metadata`.

### 2.2 Analysis Pipeline

#### 2.2.1 Transcript Extraction
- Whisper or cloud ASR options selected per worker pool.
- Supports multi-language detection; language tags stored next to transcripts.
- Confidence scores provided per segment; low-confidence regions trigger reprocessing or manual review flags.

#### 2.2.2 Keyword Detection
- Combines user-defined keyword lists with auto-extracted semantic tags (spaCy/BERT).
- Topic clustering groups clips by theme for Horizon-level diversity metrics.

#### 2.2.3 Virality Scoring
- **Inputs**: Engagement signals (likes/comments/views), velocity metrics (growth rate since posting), NLP sentiment, audience resonance indicators (match to target personas).
- **Outputs**: `virality_score` (0–1) and `relevance_score` (0–1). Stored in `analysis` and fed to Lattice for prioritization.

#### 2.2.4 Clip Candidate Extraction
- Sliding-window scan (5–120 seconds configurable) with stride tuned per platform.
- Silence removal ensures clips start/end on speech or action.
- Speaker change detection (diarization) prevents mid-sentence cuts.
- Action/facial prominence detection verifies subject is centered and expressive.
- Stored fields: `start_time`, `end_time`, `confidence`, `semantic_tags`, plus `pantheon_votes` after scoring.

### 2.3 Cognitive Layer Integration
- **Paradox**: Cross-checks clip/post metadata for duplicates or circular references before jobs progress.
- **Pantheon**: Votes on candidate quality, assigning consensus/confidence that drive which clips move to editing.
- **Lattice**: Assigns processing priority across creators and stages, ensuring GPU/CPU capacity targets the highest strategic value.
- **Horizon**: Adjusts quotas and scheduling weights so the pipeline maintains long-horizon campaign mix (e.g., themes per week).
- **Zenith**: Consumes all signals and issues binding commands (ScraperJob → EditJob → UploadJob → ScheduleTask) to workers.
- **HaloLux/Stardust**: Capture reasoning and provenance at each stage, enabling dashboard traceability.

### 2.4 Editing Pipeline
Automated V1 editing produces publish-ready clips with minimal human touch.

#### 2.4.1 Smart Autocut
- Removes silence using RMS thresholds.
- Trims filler words (“uh”, “like”) via transcript alignment.
- Tightens pacing with beat detection heuristics; minimum jump cut spacing enforced.

#### 2.4.2 Reframing / Cropping
- Enforces 9:16 output; fallback to 1:1 if subject framing fails.
- Face detection + subject tracking keep presenter centered; uses optical flow for continuity.
- Optional Ken Burns-style motion adds energy to static shots.

#### 2.4.3 Audio Processing
- LUFS normalization (-14 target).
- Broadband noise reduction + de-ess filters.
- Light compression (2:1) to smooth dynamics; limiter prevents clipping.

#### 2.4.4 Rendering
- FFmpeg pipelines defined in `EditJob.ffmpeg_commands`.
- GPU acceleration (NVENC) triggered when `gpu_required=true`.
- Output consistency: 1080x1920, 30/60fps as per platform, H.264 video + AAC audio, max 60 MB file size. Checksums stored for dedupe.

### 2.5 Upload Pipeline

#### 2.5.1 Metadata Generation
- AI proposes titles/descriptions using Chorus signals + Pantheon rationale.
- Keywords derived from analysis tags plus platform trend seeds.
- Thumbnail v1 = best-frame screenshot (subject in focus, high brightness). Metadata embedded in `UploadJob`.

#### 2.5.2 YouTube Integration
- OAuth2 per brand account; tokens rotated via secret manager.
- Upload via YouTube Data API videos.insert endpoint; resumable uploads for >50 MB.
- Privacy settings: `public|unlisted|private` set from UploadJob.
- Error handling: quota exhaustion triggers delayed retry; policy violations escalate to Paradox/Eclipse for manual review.

### 2.6 Scheduling Pipeline
- Posting time optimization blends historical engagement, Horizon adjustments, and current queue saturation.
- Daily clip quota ensures creators do not flood feeds (default 5/day configurable).
- Conflict avoidance ensures no double-booking per channel/time slot; Scheduler coordinates with Zenith.
- Horizon-provided long-horizon weights enforce content mix (e.g., 40% educational, 60% entertainment) across the calendar.

## 3. Data Structures Used in the Pipeline
Representative payloads (see full schemas in module interface document):

```jsonc
// ScraperJob
{
  "job_id": "uuid",
  "creator_id": "uuid",
  "platform": "tiktok",
  "target_url": "https://tiktok.com/@creator",
  "requested_range": { "since": "2024-05-01T00:00:00Z", "until": "2024-05-07T00:00:00Z" }
}

// AnalysisResult
{
  "video_id": "uuid",
  "transcript": "...",
  "keywords_detected": ["motivation", "fitness"],
  "virality_score": 0.83,
  "relevance_score": 0.77,
  "clip_candidates": ["clip-uuid-1", "clip-uuid-2"]
}

// ClipCandidate
{
  "clip_id": "uuid",
  "video_id": "uuid",
  "start_time": 45.2,
  "end_time": 72.1,
  "confidence": 0.92,
  "semantic_tags": ["guest_quote", "call_to_action"]
}

// EditJob
{
  "edit_job_id": "uuid",
  "clip_id": "uuid",
  "operations": ["autocut", "reframe", "captions"],
  "ffmpeg_commands": ["ffmpeg -i ..."],
  "gpu_required": true
}

// UploadJob
{
  "upload_job_id": "uuid",
  "clip_id": "uuid",
  "title": "5-Second Productivity Reset",
  "description": "...",
  "keywords": ["productivity", "routine"],
  "scheduled_time": "2024-05-10T16:00:00Z"
}

// ScheduleTask
{
  "schedule_id": "uuid",
  "clip_id": "uuid",
  "recommended_time": "2024-05-12T18:00:00Z",
  "final_decision_source": "zenith"
}
```

## 4. Error Handling
- **Scraper failures**: network retries with exponential backoff; rate-limit responses cause cooldown before reattempt. Invalid URLs routed to Paradox for validation, logged via Stardust.
- **Analysis failures**: ASR timeout triggers secondary ASR provider; malformed video escalates to Scraper for re-download. Analyzer marks job `ERROR` and notifies Eclipse.
- **Editor failures**: FFmpeg crash records command and stderr; Eclipse either retries on same host (max 3) or moves job to GPU-safe pool. Persistent failures quarantine the clip.
- **Upload failures**: Quota exceeded results in automatic defer to next quota window; policy errors require operator review flagged through Dashboard and HaloLux.
- **Scheduler deadlocks**: When overlapping constraints cannot be satisfied, Scheduler emits `scheduler_fault`, prompting Horizon to adjust targets and Zenith to break ties.
- **Eclipse handling**: Central crisis loop classifies failure severity, issues retry/rollback plans, isolates failing workers, and keeps HaloLux updated for operator visibility.

## 5. Performance Considerations
- Parallel scraping via worker pools per platform; concurrency tuned to API limits.
- Batch processing: Analyzer groups videos to reuse model warm starts; Editor batches renders when GPU memory allows.
- Worker scaling: Horizontal auto-scaling on CPU/GPU pools based on queue length and Lattice priority backlog.
- Disk I/O: Local NVMe cache for hot assets, periodic flush to cloud storage; checksums verify integrity post-transfer.
- GPU usage: Reserved for editing and high-throughput ASR; scheduler ensures GPU queues don’t starve CPU-only tasks.
- Queue backpressure: Zenith enforces max in-flight jobs per stage; when thresholds exceeded, upstream stages slow or pause until downstream drains.

## 6. Example End-to-End Execution
1. **Scraper** downloads 12 videos across three creators (past 7 days), storing media + metadata, logging every action to Stardust.
2. **Analyzer** produces transcripts and extracts 38 clip candidates with virality scores; low-confidence transcripts are reprocessed automatically.
3. **Pantheon** ranks candidates, elevating the top 5 with multi-agent consensus >0.8; Lattice adjusts queue priorities accordingly.
4. **Editor** renders the 5 clips using smart autocut + reframing; two require GPU acceleration with NVENC.
5. **Uploader** posts 2 clips immediately (based on Zenith instruction) and schedules the remaining 3 using Scheduler recommendations.
6. **Stardust** links every step, so HaloLux can show source video → clip → edit → upload → schedule lineage on the Dashboard.

## 7. Future Extensions (Pipeline v2+)
- Auto-subtitles with stylized captions and animated karaoke effects.
- Background music recommendation + loudness-aware mixing.
- B-roll injection leveraging stock/video libraries and semantic matching.
- AI voiceovers for narration or dubbing into additional languages.
- Style templates (brand kits) controlling fonts, overlays, motion graphics.
- Multi-clip compound editing to stitch thematic narratives.
- Trend analysis that adapts scraping focus based on real-time social signals.
- Thumbnail generator v2 using Stable Diffusion or similar generative models.

---
# 📘 Omniva Engine — Workers Specification
_Sourced from: docs/specifications/workers_spec.md_
---

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

---
# 📘 Omniva Engine — Dashboard & UI Specification
_Sourced from: docs/specifications/dashboard_spec.md_
---

# Omniva Engine — Dashboard & UI Specification

## 1. Overview
The Omniva dashboard is the primary user interface for managing projects and monitoring the clipfarm pipeline. Operators use it to interact with workers, review logs, track clip statuses, manage credentials, and examine cognitive reasoning generated by HaloLux. The UI is minimal and optimized for operational clarity, exposing core functions:
- Project management
- Creator management
- Bot control (start/stop/restart)
- Monitoring & alerts
- Settings and pipeline configuration
- Credential management
- Cognitive insights display (HaloLux narratives)

## 2. Dashboard Architecture
- **Frontend**: Lightweight SPA (React, Vue, or Svelte) with modular components.
- **Backend**: FastAPI service providing REST + WebSocket endpoints that proxy orchestrator data, worker statuses, and cognitive outputs.
- **Real-time updates**: Combination of periodic polling (5–15s) for heavy lists and WebSocket channels for critical signals (worker heartbeats, HaloLux updates).
- **Integrations**:
  - Stardust metadata for provenance traces.
  - Logs table for structured events.
  - Worker status service for queue depth, heartbeats.
  - Upload scheduling service for calendar data.
  - HaloLux cognitive API for interpretability payloads.

Text diagram:
```
[Frontend UI] → [FastAPI Backend] → [Database + Stardust + Logs + Workers + Cognitive Layer]
```

## 3. Pages & Views

### 3.1 Projects Overview Page
- **Display**: List of projects with status (RUNNING/PAUSED/ERROR), total videos scraped, clips processed, upload queue size, last activity timestamp.
- **User controls**: Create project, open project, pause/resume automation per project.
- **Indicators**: Color-coded badges for status, small sparkline showing throughput per project.

### 3.2 Project Detail Page
- **Content**: Project metadata (description, owner, targets), creator roster, worker progress summaries, clip pipeline visualization, latest cognitive insights (e.g., Pantheon votes, Horizon adjustments).
- **Tabs**:
  - Overview (pipeline KPIs, clip funnel).
  - Creators (CRUD, scraping windows, platform tokens).
  - Clips (table of clip states, filters by status).
  - Schedule (calendar view of upcoming posts).
  - Logs (project-scoped log viewer).
  - Settings (project-specific configuration).

### 3.3 Bot Control Page
- **Controls**: Start/stop/restart bot processes, reset failed tasks, trigger manual scrape/upload, flush or rebuild queues.
- **Metrics**: Worker heartbeats, error counts, CPU/GPU load, queue depth per worker.
- **Actions** require confirmation modals and display recent command history.

### 3.4 Logs Viewer
- **Features**: Stream logs from the centralized `logs` table with filters by source, level, date range, worker type.
- **Live tail mode**: WebSocket push for real-time monitoring.
- **UX**: JSON viewer toggle, link to Stardust/HaloLux references for each log entry.

### 3.5 Settings Page
- **Configuration**:
  - Scraping window (default 7 days) per project.
  - Keyword lists, clip length preferences.
  - Posting quotas (1–10 clips/day) and daily schedules.
  - Parallel worker counts and GPU allocation.
  - Storage paths/buckets and lifecycle rules.
  - Notification preferences (email, Slack, PagerDuty).
- Changes persist via FastAPI endpoints and require audit logging.

### 3.6 YouTube Credentials & Channel Branding
- **Display/manage**:
  - OAuth tokens (status, expiration, re-auth flow).
  - Channel selection dropdown (per project).
  - Logo/Banner uploads (v1 manual file upload; v2 note for SDXL generation).
  - Title/description template editor with handlebars-style variables.

### 3.7 HaloLux Interpretability View
- **Purpose**: Present cognitive reasoning chain per clip/job.
- **Data**:
  - Paradox conflict resolutions.
  - Eclipse recovery actions.
  - Pantheon vote summaries.
  - Lattice routing decisions.
  - Horizon long-term adjustments.
  - Zenith final decision notes.
- **UI**: Tree/accordion combined with JSON inspector. Provide copy-to-clipboard for raw payloads.

## 4. UI Components
- `ProjectCard`: status badge, KPI summary, action buttons.
- `CreatorList`: table with platform icons, scraping windows, action menu.
- `WorkerStatusBadge`: heartbeat indicator, load percent, error tooltip.
- `LogTable`: virtualized table with filters, JSON viewer.
- `ClipTimeline`: horizontal pipeline view illustrating clip state transitions.
- `ScheduleCalendar`: week/month calendar with drag-to-reschedule (future).
- `AIExplanationPanel`: renders HaloLux reasoning with highlight states and raw JSON toggle.
- `Modal` components for sensitive actions (stop bot, re-auth credentials, delete project).

## 5. Data Fetching & API Integration
- **Endpoints** (examples):  
  - `GET /api/projects`, `POST /api/projects`  
  - `GET /api/projects/{id}/overview`  
  - `GET /api/logs?project_id=...`  
  - `POST /api/bots/{id}/command` (start/stop/reset)  
  - `GET /api/halolux/explanations?clip_id=...`  
  - `GET /api/schedules/upcoming`  
  - `GET /api/workers/status`
- **Polling/websockets**:
  - Projects overview: poll every 15s.
  - Worker status + heartbeats: WebSocket (fallback to 5s poll).
  - Logs viewer live tail: WebSocket stream.
  - HaloLux insights: on-demand fetch + WebSocket for updates flagged as critical.
- **Error handling**: show toast notifications, fallback to last known state, allow manual refresh. For 401s, prompt re-auth. For 5xx, display contextual message and retry/backoff.
- **State updates**: UI uses optimistic updates for stop/start commands, reconciling with backend responses; long-running tasks display spinner + event log.

## 6. UX Guidelines
- Operational-first: prioritize clarity of state over aesthetic flourish.
- Status colors: green = healthy, yellow = attention, red = error, gray = paused.
- Minimal clutter: collapse advanced settings behind accordions; highlight pipeline progress metrics.
- Provide inline links from UI elements to Stardust/HaloLux artifacts for interpretability.
- Tooltips explain cognitive insights and decision reasons.
- Do not block user interactions during background tasks; show non-blocking progress indicators.

## 7. Wireframe Diagrams

### Projects Overview
```
-----------------------------------------
| Project Name | Status | Videos | Clips |
-----------------------------------------
| BusinessAI   | RUNNING|   42   |  135  |
| FitnessGuru  | PAUSED |   18   |   67  |
| CreatorLab   | ERROR  |    9   |   21  |
-----------------------------------------
[Create Project] [Pause All]
```

### Cognitive Insight Drawer
```
-----------------------------------------
| HaloLux Insight — Clip #12            |
| Decision Trace:                       |
|  Paradox: No conflicts                |
|  Lattice: Priority 0.82 (under-index) |
|  Pantheon Votes:                      |
|    - Strategist: High novelty (0.91)  |
|    - Guardian: Medium virality (0.65) |
|  Horizon: Aligns with Week 6 goals    |
|  Zenith: Approved Edit+Upload         |
-----------------------------------------
| Raw JSON { ... } [Copy]               |
-----------------------------------------
```

## 8. Implementation Notes
- UI can be delivered incrementally—start with projects overview and logs, then add HaloLux panels.
- Handle missing/partial data gracefully: empty states with guidance, skeleton loading indicators.
- HaloLux payloads can be large/structured; JSON viewer must support nested objects and search.
- Support multiple concurrent operator sessions with shared state; consider role-based access (future).
- Ensure accessibility (ARIA labels, keyboard navigation) for operational tasks.
- Document versioning between frontend and backend APIs to avoid drift as modules evolve.

---
# 📘 Omniva Engine — API Overview
_Sourced from: docs/api/api_overview.md_
---

# Omniva Engine — API Overview

## 1. Purpose of the API
The Omniva Engine API exposes programmatic control over every stage of the content pipeline. Dashboard clients, automation scripts, CLI utilities, and external systems call the API to create projects, manage creators, launch scraping jobs, inspect analysis outputs, trigger editing/uploading, adjust schedules, and retrieve interpretability data. By mirroring the clipfarm lifecycle, the API enables full automation from ingestion through publishing while preserving auditing and governance.

## 2. Architecture
- **Backend**: FastAPI application deployed behind authenticated gateways.
- **Protocol**: REST-style endpoints exchanging JSON payloads over HTTPS.
- **Execution**: API requests mutate state in PostgreSQL (system of record) and enqueue tasks for workers (Scraper, Analyzer, Editor, Uploader, Scheduler).
- **Cognitive Layer**: Worker events and API-triggered operations notify cognitive subsystems (Paradox, Lattice, Pantheon, etc.) through internal buses; results surface back through API responses.

Diagram:
```
(Client / Dashboard / Automation)
        ↓ HTTPS / JSON
        [FastAPI Gateway]
        ↓           ↓
   [Workers & Queues]   [Database + Stardust + Cognitive Subsystems]
```

## 3. API Principles
- **Predictable**: Consistent nouns/verbs, idempotent GET/DELETE, side-effecting POST.
- **Versioned**: All endpoints live under `/v1/`; future major versions use `/v2/`.
- **Typed**: JSON schemas define request/response bodies; enums documented per field.
- **Transparent Errors**: Machine-readable error objects with stable codes.
- **Paginated**: Collection endpoints support `limit`, `offset`, or cursor pagination for large result sets.

## 4. Authentication
- Current deployments run behind the Omniva Dashboard and rely on trusted network access; no external authentication is required.
- Future: API key or OAuth2 client credentials per tenant to enable third-party integrations. Spec should treat `Authorization: Bearer <token>` as forthcoming requirement.

## 5. Response Format
Every endpoint returns a wrapper object:
```json
{
  "status": "success",
  "data": { /* endpoint-specific payload */ },
  "error": null,
  "meta": { "request_id": "uuid", "generated_at": "2024-05-07T15:00:00Z" }
}
```
On error:
```json
{
  "status": "error",
  "data": null,
  "error": { "message": "clip not found", "code": "CLIP_NOT_FOUND" },
  "meta": { "request_id": "uuid" }
}
```

## 6. Error Handling
- HTTP status codes align with behavior: `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `409 Conflict`, `422 Validation Error`, `500 Internal Server Error`.
- Errors generated by workers propagate back via Eclipse Engine. For example, a failed upload surfaces as `409` with `UPLOAD_FAILED`, while Eclipse schedules a retry.
- All API interactions are logged to Stardust, including request metadata, response code, and associated entity IDs, ensuring interpretability through HaloLux.

## 7. Rate Limits (Future)
- Planned per-project/requester rate limiting with leaky-bucket semantics.
- Queue saturation indicators will be exposed via `Retry-After` headers when downstream workers near capacity.
- Until rate limits ship, monitoring dashboards track usage and operations teams can throttle via infrastructure policies.

---
# 📘 Omniva Engine — API Endpoints Reference (v1)
_Sourced from: docs/api/endpoints_reference.md_
---

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

---
# 📘 Omniva Engine — Engineering Roadmap
_Sourced from: docs/ROADMAP.md_
---

# Omniva Engine — Engineering Roadmap

## Overview
This roadmap defines the phased evolution of Omniva Engine from the v0.1 foundation through a fully autonomous v1.0 release. Each phase introduces major functionality while preserving stability, extensibility, and observability. The overarching goal is to deliver an intelligent, resilient clipfarming machine that can operate end-to-end with minimal human intervention.

---

## Phase v0.1 — Foundations (Documentation + Architecture)
**Deliverables**
- Complete documentation set (architecture, specs, interfaces).
- Initial repository scaffold for API, workers, dashboard, and cognitive subsystems.
- Worker definitions with TODO stubs and queue contracts.
- Cognitive subsystem definitions (interfaces only).
- Basic FastAPI scaffolding with placeholder endpoints.
- Dashboard/UI skeleton with routing and layout seeds.
- Database schemas defined for creators, posts, videos, clips, jobs, logging.
- Logging and Stardust specifications finalized.

**Success Criteria**
- Documentation is comprehensive and current.
- Repository structure is stable, lint-clean, and ready for implementation work.

---

## Phase v0.2 — Cognitive Integration (Minimal Viable Intelligence)
**Deliverables**
- First-pass implementations of Paradox (duplicate detection), Eclipse (failure/retry logic), and Stardust (metadata store + ingestion hooks).
- Lattice influences worker queue ordering.
- Pantheon agent framework with heuristic scoring.
- Chorus provides basic title/description cleanup.
- Zenith integrator skeleton wiring cognitive outputs to worker commands.

**Success Criteria**
- Cognitive modules actively influence pipeline decisions and emit advisory signals consumed by Zenith.

---

## Phase v0.3 — Operational Expansion (Pipeline Maturity)
**Deliverables**
- Scraper v2 with resilient platform adapters and retry logic.
- Analyzer v2 with improved ASR accuracy and clip scoring.
- Editor v2 with hardened FFmpeg workflows and asset management.
- Scheduler v2 with smarter posting windows and quota controls.
- Real-time worker monitoring dashboards + alerting.
- Error dashboards surfacing Eclipse events.
- HaloLux basic interpretability panel wired to Stardust.

**Success Criteria**
- System reliably ingests content, produces clips, and schedules uploads without manual babysitting.

---

## Phase v0.4 — Multi-Agent Intelligence (Pantheon v2)
**Deliverables**
- Full Pantheon multi-agent council featuring virality, relevance, novelty, quality, and consistency agents.
- Lattice semantic routing improvements ingesting additional context signals.
- Horizon begins learning long-term posting patterns and feedback loops.
- Adaptive prioritization adjusting workloads based on historical performance.

**Success Criteria**
- Clip selection quality measurably improves through agent consensus and adaptive routing.

---

## Phase v0.5 — Creative Automation (Advanced Editing)
**Deliverables**
- Subtitle generation with styling.
- B-roll injection pipeline.
- Music alignment and mixdown automation.
- AI voiceover synthesis for narration/dubbing.
- Style templates + brand kits for consistent overlays.
- Thumbnail generator v2 powered by Stable Diffusion or equivalent.

**Success Criteria**
- Produced clips reach near-production quality with minimal manual editing.

---

## Phase v0.6 — Autonomy Boost (Hands-Off Operation)
**Deliverables**
- Automatic creator discovery and onboarding suggestions.
- Automatic niche/topic expansion recommendations.
- Posting strategy optimization driven by engagement analytics.
- Horizon long-range planning upgrade with proactive goal management.
- Reduced operator input for daily operations.

**Success Criteria**
- Omniva maintains and grows channels autonomously, requiring only high-level oversight.

---

## Phase v0.7 — Distributed Omniva (Scalability)
**Deliverables**
- Horizontal scaling strategy for API and workers.
- Multi-GPU editing clusters with resource-aware scheduling.
- Distributed worker deployment across multiple nodes/regions.
- Shared global Stardust metadata layer with replication.

**Success Criteria**
- System handles many concurrent projects with consistent latency and reliability.

---

## Phase v0.8 — Language & Platform Expansion
**Deliverables**
- Multilingual ASR/NLP support (major languages first).
- Scraping adapters for additional platforms (e.g., long-form podcasts, LinkedIn, X).
- Upload workflows for multiple platforms (TikTok, Instagram, YouTube, more).

**Success Criteria**
- Omniva operates across global markets and social networks with localized accuracy.

---

## Phase v0.9 — Full Interpretability (HaloLux v2)
**Deliverables**
- Rich visualization of Pantheon votes, Lattice routing, Horizon strategy logic, Eclipse recovery sequences, Stardust lineage graphs.
- Deep integration with the dashboard (insight drawer, drill-down charts).
- Exportable audit packs for compliance reviews.

**Success Criteria**
- Operators gain complete transparency into Omniva’s decisions, enabling trust and auditability.

---

## Phase v1.0 — Complete Autonomous Omniva
**Deliverables**
- Fully autonomous end-to-end engine: self-correcting, self-scheduling, self-optimizing.
- Resilient, scalable deployment with multi-project support.
- Comprehensive interpretability and logging.
- Minimal mandatory user intervention; optional human-in-the-loop controls.

**Success Criteria**
- Omniva can run indefinitely with human oversight optional, meeting SLAs for quality, throughput, and transparency.

---

## Notes on Versioning
- Follow semantic versioning: MAJOR (breaking changes), MINOR (new features), PATCH (bug fixes).
- Maintain backward-compatible APIs where possible; announce deprecations.
- Provide database migration scripts for any schema change, tested across environments.
- Publish structured changelogs detailing features, fixes, and migration notes each release cycle.

---
_Compiled automatically by Codex — Omniva Engine v0.1 Unified Reference_
---
