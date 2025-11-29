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
