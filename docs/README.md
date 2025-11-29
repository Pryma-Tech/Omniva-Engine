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

