# Omniva Engine v2

Omniva Engine v2 is a modular, plugin-based AI clipfarming platform featuring a FastAPI backend, Next.js frontend, and internal EventBus/Worker architecture for orchestrating clip discovery, editing, and publishing.

## Minimal Backend (v0.1)
This repo now includes a lightweight FastAPI service under `backend/` used to exercise the Heartbeat + Orchestrator flows described in the Omniva docs.

### Setup
```
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Run the service
```
uvicorn backend.app.main:app --reload
```

### Run backend tests
```
pytest tests/test_api_orchestrator.py tests/test_cron_tasks.py tests/test_heartbeat_engine.py
```

### Project storage
- Backend v0.1 persists project metadata under `backend/storage/projects_meta/`.
- A default project with ID `1` is created automatically on first startup so API and heartbeat flows have deterministic data.
- To reset, stop the container/service and clear the JSON files in that directory.

### Docker workflows
Use the `omniva` helper to build + redeploy both backend and frontend containers with coordinated settings:
```
./omniva build redeploy
```
The script prompts for:
- Backend/Frontend image tags and container names.
- Backend host port (mapped to container port 8000).
- Frontend host port (mapped to container port 3000; default 8080).

It then:
1. Builds images from `Dockerfile.backend` and `Dockerfile.frontend`.
2. Recreates containers on the shared `omniva_network`.
3. Injects `NEXT_PUBLIC_BACKEND_URL=http://omniva-backend:8000` so the frontend talks to the backend over the docker network.
4. Prints verification steps (`curl http://localhost:<backend_port>/healthz`, visit the frontend host port) plus a reminder to follow PROMPT I for DNS/firewall exposure.

## Project Structure
```
omniva-v2/
  backend/
    app/
      core/
      subsystems/
      models/
      api/
      main.py
  frontend/
    omniva-ui/
      app/
      components/
```

## Setup Instructions
### Backend
```
cd omniva-v2/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```
cd omniva-v2/frontend/omniva-ui
npm install
npm run dev
```

## Environment Variables
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```
Ensure this value is set before starting the Next.js app so fetch calls target the backend.

## Development Rules
1. All subsystems live in `backend/app/subsystems/`.
2. All models live in `backend/app/models/`.
3. All UI pages live in `frontend/omniva-ui/app/`.
