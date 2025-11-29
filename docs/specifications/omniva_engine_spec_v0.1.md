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

