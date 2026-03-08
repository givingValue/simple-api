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

## Kubernetes Deployment

The app can be deployed to Kubernetes (e.g. k3s) using the manifests in `k8s/`.

**Prerequisites:** Docker, kubectl, access to a Kubernetes cluster.

1. Build and push the image:
   ```bash
   docker build -t YOUR_DOCKERHUB_USERNAME/simple-api:latest .
   docker push YOUR_DOCKERHUB_USERNAME/simple-api:latest
   ```

2. Update `k8s/deployment.yaml` with your DockerHub username and `k8s/ingress.yaml` with your host (e.g. `api.PUBLIC_IP.sslip.io` for internet access).

3. Deploy:
   ```bash
   kubectl apply -f k8s/
   ```

**Jenkins CI/CD:** The Jenkinsfile builds the image, pushes to DockerHub, and deploys to Kubernetes.

**Jenkins credentials to configure:**

1. **dockerhub-credentials** — Kind: "Username with password". Your DockerHub username and password (or access token).

2. **kubeconfig-file** — Kind: "Secret file". Upload your kubeconfig file (e.g. `~/.kube/config` or `/etc/rancher/k3s/k3s.yaml`). ID: `kubeconfig-file`.

**Environment variables (no values in pipeline):**  
Set `DOCKERHUB_USERNAME` and `INGRESS_HOST` in one of these ways:

**Option A – Job configuration (EnvInject plugin):**
1. Install the **EnvInject** plugin (Manage Jenkins → Plugins).
2. Open your job → **Configure** → **Build Environment**.
3. Enable **Inject environment variables**.
4. In **Properties Content**, add:
   ```
   DOCKERHUB_USERNAME=your-dockerhub-username
   INGRESS_HOST=api.54.123.45.67.sslip.io
   ```

**Option B – Global properties:**  
Manage Jenkins → System → Global properties → Environment variables → add the same variables.

| Variable           | Example              |
|-------------------|----------------------|
| `DOCKERHUB_USERNAME` | `myuser`           |
| `INGRESS_HOST`    | `api.54.123.45.67.sslip.io` |

**Pipeline parameter:** `IMAGE_TAG` (default: `latest`)

**Prerequisites:** Jenkins agent with Docker and kubectl installed.

## Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
