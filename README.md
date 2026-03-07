# Simple API

A minimal FastAPI boilerplate with configuration, health checks, and environment-based settings.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example env file and adjust as needed:
   ```bash
   cp .env.example .env
   ```

## Running

**Use `python main.py`** so host, port, and other settings from `.env` are applied:

```bash
python main.py
```

If you run `uvicorn main:app` directly, uvicorn ignores our config and uses its own defaults (port 8000). To use config values with uvicorn, pass them explicitly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
# Or from .env: uvicorn main:app --host $HOST --port $PORT
```

## Endpoints

- `GET /` — Root
- `GET /health` — Health check (useful for load balancers, k8s probes)
- `GET /items/{item_id}` — Example item endpoint

## Configuration

| Variable     | Default   | Description                    |
|-------------|-----------|--------------------------------|
| HOST        | 0.0.0.0   | Bind address                   |
| PORT        | 8000      | Server port                    |
| RELOAD      | false     | Enable auto-reload (dev)       |
| DEBUG       | false     | Enable debug logging           |
| CORS_ORIGINS| *         | Comma-separated allowed origins|

## Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
