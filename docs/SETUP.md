# Setup and Docker Guide

## Prerequisites

- Git
- Docker Desktop/Engine with Docker Compose, or Python compatible with the pinned dependencies
- Model artifact and processed background data expected by the API
- Credentials for enabled external services such as OpenAI and Qdrant Cloud
- Supabase PostgreSQL connection details for database-backed agent workflows

## Clone

```bash
git clone https://github.com/Armanix-01/Olist-Logistics-Intelligence.git
cd Olist-Logistics-Intelligence
```

## Environment configuration

The repository documentation includes a root-level [`.env.example`](../.env.example) template so a reviewer can see which external services may need credentials. It lists `OPENAI_API_KEY` for LLM features and `QDRANT_URL` / `QDRANT_API_KEY` for Qdrant Cloud. Supabase PostgreSQL settings are shown as examples because the exact variable names depend on the project's database configuration.

Before running the app, compare the template with `api/config.py`, `agent/llms.py`, `docker-compose.yml`, and the database/RAG configuration, and retain only variable names that the code actually reads. Copy the file to `.env` and fill in your own credentials locally. Never commit `.env`, real API keys, database passwords, or other secrets. The `.env.example` file must contain placeholders only.

```bash
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env`.

## Docker Compose (recommended)

### 1. Review files

Review `docker-compose.yml`, `Dockerfile.api`, `Dockerfile.streamlit`, and `.dockerignore`. Confirm that model artifacts and required data are copied into images or mounted, and that secrets are passed at runtime rather than baked into an image.

### 2. Validate and build

```bash
docker compose config
docker compose build
```

### 3. Start services

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

### 4. Inspect status and logs

```bash
docker compose ps
docker compose logs -f
```

For one service, substitute its exact name from the `services:` section:

```bash
docker compose logs -f <service-name>
```

### 5. Stop

```bash
docker compose down
```

To also remove Compose-managed volumes:

```bash
docker compose down --volumes
```

**Warning:** Removing volumes can erase persisted local database data. Use this only when intentionally resetting the environment. This does not delete data stored in your remote Supabase PostgreSQL database.

### Docker command meanings

- `docker compose build`: build images.
- `docker compose up`: create/start containers.
- `docker compose up --build`: rebuild images and start containers.
- `docker compose up -d`: run in background.
- `docker compose down`: stop/remove containers and Compose network.
- `docker image ls`: list local images.
- `docker compose ps`: inspect project containers.

Images remain in the local Docker image store unless explicitly pushed to a registry.

## Run locally with Python

Python 3.12 was used in development; verify compatibility with the pinned dependencies.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies for the service you need:

```bash
pip install -r requirements-api.txt
pip install -r requirements-streamlit.txt
```

If the root `requirements.txt` is intended as the full development environment, use it instead of installing overlapping requirements files blindly. Ensure `shap` is included in the API dependencies.

Check that `MODEL_PATH` points to the fitted pipeline and that the configured background-data path exists. The background dataset must contain the original model input columns and exclude the target column.

Start FastAPI from the repository root:

```bash
uvicorn api.main:app --reload
```

Start Streamlit in a second terminal using the entry point that exists in your checkout. For example:

```bash
streamlit run streamlit_app/app.py
```

If `app.py` is at the repository root, use `streamlit run app.py` instead.

When running in containers, `127.0.0.1` refers to the current container. To call another Compose service, configure the API URL using the appropriate service hostname and port.

## Troubleshooting

- **Model not found:** verify `MODEL_PATH`, image contents, mounted volumes, and dependency compatibility.
- **SHAP startup error:** check the expected pipeline step names, background columns, SHAP/XGBoost versions, and SHAP output shapes.
- **Streamlit connection error:** check API status, `API_URL`, published ports, and Compose service hostname.
- **LLM failure:** check credentials, model configuration, provider limits, network, and timeouts. Do not log secrets.
- **Supabase PostgreSQL/Qdrant failure:** verify credentials, network access, database connection settings, collection/schema initialization, and connection hostname configuration.
