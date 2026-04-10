# Legacy Backend

旧 Capacitor frontend 専用の FastAPI backend です。chat / threads / system prompts API を提供し、必要に応じて R2 上の EgoGraph データへツール経由でアクセスします。

## Setup

```bash
cp .env.example .env
uv sync
```

## Run

```bash
uv run uvicorn backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

## Verify

```bash
uv run pytest backend/tests
uv run ruff check backend
```

## Notes

- chat 履歴 SQLite は `backend/data/chat.sqlite` に保存されます
- frontend から接続する場合は `frontend/.env` の `VITE_API_URL` をこの backend に向けてください
