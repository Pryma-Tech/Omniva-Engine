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
