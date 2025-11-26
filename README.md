# Omniva Engine v2

Omniva Engine v2 is a modular, plugin-based AI clipfarming platform featuring a FastAPI backend, Next.js frontend, and internal EventBus/Worker architecture for orchestrating clip discovery, editing, and publishing.

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
