# EgoGraph Chat Backend

Legacy Capacitor frontend 専用の FastAPI backend です。
EgoGraph エージェントとのチャット、スレッド管理、システムプロンプト管理を提供し、
R2 上の EgoGraph データ（Spotify / GitHub / Browser History）へ LLM ツール経由でアクセスします。

## Architecture

Clean Architecture ベースのレイヤード構成です。

```text
API → UseCase → Domain
           ↑
    Infrastructure
```

| Layer            | 役割                                              |
|------------------|---------------------------------------------------|
| `api/`           | HTTP 入出力、リクエストバリデーション、エラー変換       |
| `usecases/`      | チャット処理全体のオーケストレーション                  |
| `domain/`        | 会話・ツール・LLM のドメインモデル                      |
| `infrastructure/`| SQLite / DuckDB / R2 / LLM Provider との接続         |

## Directory Structure

```text
backend/
├── __init__.py
├── main.py              # FastAPI エントリーポイント
├── config.py            # 設定管理 (pydantic-settings)
├── dependencies.py      # FastAPI 依存注入
├── constants.py         # 定数定義
├── validators.py        # バリデーションユーティリティ
├── paths.py             # ランタイムパス定義
├── api/                 # API Layer
│   ├── chat.py          # POST /v1/chat (ストリーミング対応)
│   ├── threads.py       # スレッド CRUD
│   ├── system_prompts.py# システムプロンプト管理
│   ├── health.py        # ヘルスチェック
│   └── schemas/         # Pydantic スキーマ
├── usecases/            # UseCase Layer
│   ├── chat/            # チャットロジック、ツール実行
│   ├── llm_model/       # LLM モデル管理
│   └── tools/           # ツールレジストリ・ファクトリ
├── domain/              # Domain Layer
│   ├── models/          # LLM・スレッド・ツールのドメインモデル
│   └── tools/           # ツール定義 (Spotify/GitHub/BrowserHistory)
├── infrastructure/      # Infrastructure Layer
│   ├── database/        # SQLite・DuckDB 接続・クエリ
│   ├── llm/             # LLM プロバイダー (OpenAI/Anthropic/OpenRouter)
│   └── repositories/    # データアクセスリポジトリ
├── dev_tools/           # 開発用 CLI ツール
├── scripts/             # マイグレーション等のスクリプト
├── tests/               # テストスイート
│   ├── unit/
│   ├── integration/
│   ├── performance/
│   ├── domain/
│   └── fixtures/
├── data/                # ランタイムデータ (gitignore)
│   └── chat.sqlite
├── pyproject.toml
└── uv.lock
```

## Setup

```bash
# 環境変数の設定
cp .env.example .env
# .env に R2 設定、LLM API キー等を記載

# 依存関係のインストール
uv sync
```

### Required Environment Variables

| Variable                | Description                     |
|-------------------------|---------------------------------|
| `R2_ENDPOINT_URL`       | Cloudflare R2 エンドポイント     |
| `R2_ACCESS_KEY_ID`      | R2 アクセスキー                  |
| `R2_SECRET_ACCESS_KEY`  | R2 シークレットキー              |
| `R2_BUCKET_NAME`        | R2 バケット名 (default: egograph)|

### Optional Environment Variables

| Variable               | Description                              |
|------------------------|------------------------------------------|
| `OPENAI_API_KEY`       | OpenAI API キー                           |
| `ANTHROPIC_API_KEY`    | Anthropic API キー                        |
| `OPENROUTER_API_KEY`   | OpenRouter API キー                       |
| `DEFAULT_LLM_MODEL`    | デフォルトモデル (default: deepseek/deepseek-v3.2) |
| `BACKEND_HOST`         | ホスト (default: 127.0.0.1)               |
| `BACKEND_PORT`         | ポート (default: 8000)                    |
| `CORS_ORIGINS`         | CORS 許可オリジン (default: *)            |

## Run

```bash
# 開発サーバー (ホットリロード)
uv run uvicorn backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000

# API ドキュメント
# http://127.0.0.1:8000/docs (Swagger UI)
# http://127.0.0.1:8000/redoc (ReDoc)
```

## API Endpoints

### Chat

| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| POST   | `/v1/chat`                        | チャット送信 (SSE ストリーミング対応) |
| GET    | `/v1/chat/models`                 | 利用可能な LLM モデル一覧        |

### Threads

| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| GET    | `/v1/threads`                     | スレッド一覧取得                 |
| GET    | `/v1/threads/{thread_id}`         | スレッド詳細取得                 |
| GET    | `/v1/threads/{thread_id}/messages`| スレッド内メッセージ一覧取得      |

### System Prompts

| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| GET    | `/v1/system-prompts/{name}`       | システムプロンプト取得            |
| PUT    | `/v1/system-prompts/{name}`       | システムプロンプト更新            |

### Health

| Method | Endpoint     | Description      |
|--------|-------------|------------------|
| GET    | `/health`   | ヘルスチェック     |

## Verify

```bash
# テスト実行
uv run pytest tests/

# Lint
uv run ruff check .

# Import 確認
uv run python -c "from backend.main import create_app; print('OK')"
```

## Tool System

LLM はユーザーの質問に応じて自動的にツールを呼び出し、EgoGraph データにアクセスします。

| Tool                  | Description                              | Data Source         |
|-----------------------|------------------------------------------|---------------------|
| Spotify Stats         | リスニング統計の分析                       | R2 Parquet via DuckDB |
| GitHub Worklog        | GitHub アクティビティの分析                | R2 Parquet via DuckDB |
| Browser History       | ブラウザ閲覧履歴の分析                     | R2 Parquet via DuckDB |

R2 設定がない場合はツールなしでチャットのみ動作します。

## Notes

- チャット履歴 SQLite は `backend/data/chat.sqlite` に保存されます
- frontend から接続する場合は `frontend/.env` の `VITE_API_URL` をこの backend に向けてください

## Docs

詳細なドキュメントは [`docs/30.backend/`](../docs/30.backend/) を参照してください。

- [Architecture](../docs/30.backend/01_architecture.md) — レイヤー構成と依存関係ルール
- [Streaming](../docs/30.backend/02_streaming.md) — SSE ストリーミングの仕組み
- [Tool System](../docs/30.backend/03_tool-system.md) — ツール実行の仕組み
- [Performance](../docs/30.backend/04_performance/future_optimizations.md) — 将来の最適化案
