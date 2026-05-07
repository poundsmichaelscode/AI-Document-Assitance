# AI Document Assistant — Fixed Working Full-Stack RAG Project

A corrected full-stack AI document assistant using FastAPI, React, Vite, Tailwind CSS, PostgreSQL, Redis, Celery, OpenAI, LangChain, and Pinecone.

## Important fixes included

- Tailwind fixed to stable v3 setup.
- Vite pinned to stable v5.
- React pinned to stable v18.
- Removed all Tailwind v4 packages such as `@tailwindcss/postcss`.
- Docker frontend no longer bind-mounts `node_modules`, preventing Rollup optional dependency errors.
- Backend env parsing fixed: list-like env values are plain strings and parsed safely in code.
- Docker Compose is valid YAML.
- Backend, worker, frontend, Postgres, and Redis services are wired correctly.

## Run with Docker

1. Open `backend/.env` and replace:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
JWT_SECRET_KEY=change-this-to-a-long-random-secret
```

2. From project root:

```bash
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up --build
```

Open:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## Run manually

For local/manual backend, change `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/doc_assistant
REDIS_URL=redis://localhost:6379/0
```

Start Postgres and Redis:

```bash
docker run --name doc-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=doc_assistant -p 5432:5432 -d postgres:16
docker run --name doc-redis -p 6379:6379 -d redis:7
```

Backend:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Worker:

```bash
cd backend
source venv/bin/activate
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

Frontend:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Test flow

1. Register.
2. Create a workspace.
3. Upload a PDF, DOCX, or TXT file.
4. Wait for the document status to become `ready`.
5. Ask a question about the document.
