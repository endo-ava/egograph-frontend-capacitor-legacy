# Legacy Backend Architecture

legacy frontend 専用 backend は、Clean Architecture ベースのレイヤード構成で実装しています。

## 依存関係ルール

```text
API -> UseCase -> Domain
            ^
            |
    Infrastructure
```

- `api/`: HTTP 入出力とエラー変換
- `usecases/`: チャット処理全体のオーケストレーション
- `domain/`: 会話、ツール、LLM まわりのドメインモデル
- `infrastructure/`: SQLite、R2/DuckDB、LLM Provider との接続

## 主な責務

### API Layer

- `backend/api/chat.py`
- `backend/api/threads.py`
- `backend/api/system_prompts.py`
- `backend/api/health.py`

薄いルーターとして、リクエスト受付、バリデーション、UseCase 呼び出し、レスポンス変換を担当します。

### UseCase Layer

- `backend/usecases/chat/chat_usecase.py`
- `backend/usecases/chat/tool_executor.py`
- `backend/usecases/chat/system_prompt_builder.py`
- `backend/usecases/llm_model/service.py`

チャット履歴管理、LLM とのループ、ツール実行、システムプロンプト組み立てを担当します。

### Domain Layer

- `backend/domain/models/llm.py`
- `backend/domain/models/llm_model.py`
- `backend/domain/models/thread.py`
- `backend/domain/models/tool.py`
- `backend/domain/tools/*`

LLM メッセージ、モデル情報、スレッド、ツールスキーマといった純粋なドメイン概念を保持します。

### Infrastructure Layer

- `backend/infrastructure/database/chat_connection.py`
- `backend/infrastructure/database/queries.py`
- `backend/infrastructure/database/github_queries.py`
- `backend/infrastructure/database/browser_history_queries.py`
- `backend/infrastructure/llm/*`
- `backend/infrastructure/repositories/*`

外部システムとの接続を担当します。チャット履歴は SQLite、分析データは R2 上の Parquet を DuckDB 経由で参照します。

## 現在の公開 API

- `POST /v1/chat`
- `GET /v1/chat/models`
- `GET /v1/threads`
- `GET /v1/threads/{thread_id}`
- `GET /v1/threads/{thread_id}/messages`
- `GET /v1/system-prompts/{name}`
- `PUT /v1/system-prompts/{name}`
- `GET /health`

## ディレクトリ構造

```text
backend/
├── main.py
├── config.py
├── dependencies.py
├── api/
├── usecases/
├── domain/
├── infrastructure/
├── tests/
└── docs/
```

## 補足

- SQLite の保存先は `backend/data/chat.sqlite`
- `backend/paths.py` で backend ローカルの実行パスを管理
- R2 設定がある場合のみ、Spotify / GitHub / Browser History 系ツールを有効化
