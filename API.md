# API Contract

このドキュメントは、legacy Capacitor frontend が利用する backend endpoint をまとめたものです。

## Common Behavior

- Base URL は `VITE_API_URL` から取得します
- すべての request は `Content-Type: application/json` を送ります
- `VITE_API_KEY` が空でない場合のみ `X-API-Key` を送ります
- backend 側の API key 認証は optional ですが、`BACKEND_API_KEY` が設定されている環境では無効または未指定の key に対して `401 Invalid API key` を返します
- client 側では backend JSON の `detail` を使って `ApiRequestError(status, detail)` を生成します

## POST /v1/chat

LLM agent 用 chat request を送信します。

### Request body

```json
{
  "messages": [
    { "role": "user", "content": "Hello" }
  ],
  "stream": false,
  "thread_id": null,
  "model_name": "openai/gpt-5-mini"
}
```

### Fields

- `messages`: `{ role, content }` の配列
- `stream`: optional boolean。`true` の場合は SSE streaming
- `thread_id`: optional。既存 thread の ID
- `model_name`: optional。backend がサポートする model identifier

### Non-stream response

```json
{
  "id": "chatcmpl-...",
  "message": { "role": "assistant", "content": "..." },
  "tool_calls": null,
  "usage": {
    "prompt_tokens": 1,
    "completion_tokens": 2,
    "total_tokens": 3
  },
  "thread_id": "uuid",
  "model_name": "openai/gpt-5-mini"
}
```

### Stream response

`stream=true` の場合、同じ endpoint は `text/event-stream` を返します。client は `data: ...` payload を次の chunk type として解釈します。

- `delta`
- `tool_call`
- `tool_result`
- `done`
- `error`

### Tested error behavior

- `400 invalid_model_name: ...`：未対応 `model_name`（`backend/tests/integration/test_api_chat_models.py`）
- `400 At least one user message is required`：user message がない（`backend/tests/integration/test_chat_history.py`）
- `404 Thread not found: ...`：存在しない `thread_id`（`backend/tests/integration/test_chat_history.py`）
- `401 Invalid API key`：認証有効時に key 不正または未指定（`backend/dependencies.py` と integration tests）

## GET /v1/chat/models

選択可能な LLM model 一覧を取得します。

### Response

```json
{
  "models": [
    {
      "id": "openai/gpt-5-mini",
      "name": "GPT-5 mini",
      "provider": "openai",
      "input_cost_per_1m": 0,
      "output_cost_per_1m": 0,
      "is_free": false
    }
  ],
  "default_model": "openai/gpt-5-mini"
}
```

### Tested error behavior

- `401 Invalid API key`：認証有効時に有効な key がない（`backend/tests/integration/test_api_chat_models.py`）

## GET /v1/threads

thread summary の paginated list を取得します。

### Query parameters

- `limit`: integer。backend 側で最小値 / 最大値を検証
- `offset`: integer。`>= 0`

### Example

`GET /v1/threads?limit=20&offset=0`

### Response

```json
{
  "threads": [
    {
      "thread_id": "uuid",
      "user_id": "default_user",
      "title": "Hello",
      "preview": "Assistant reply",
      "message_count": 2,
      "created_at": "2026-03-25T00:00:00Z",
      "last_message_at": "2026-03-25T00:00:10Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

### Tested error behavior

- `422`：`limit` が backend 最大値を超える（`backend/tests/integration/test_threads_api.py`）

## GET /v1/threads/{thread_id}

単一 thread summary を取得します。

### Response

`GET /v1/threads` の各 item と同じ thread object shape を返します。

### Tested error behavior

- `404 Thread not found: {thread_id}`：thread が存在しない（`backend/tests/integration/test_threads_api.py`, `backend/tests/integration/test_chat_history.py`）

## GET /v1/threads/{thread_id}/messages

指定 thread の保存済み message を作成日時昇順で取得します。

### Response

```json
{
  "thread_id": "uuid",
  "messages": [
    {
      "message_id": "uuid",
      "thread_id": "uuid",
      "user_id": "default_user",
      "role": "user",
      "content": "Hello",
      "created_at": "2026-03-25T00:00:00Z",
      "model_name": null
    }
  ]
}
```

### Tested error behavior

- `404 Thread not found: {thread_id}`：thread が存在しない（`backend/tests/integration/test_threads_api.py`, `backend/tests/integration/test_chat_history.py`）

## GET /v1/system-prompts/{name}

名前付き system prompt file を取得します。

### Supported names

- `user`
- `identity`
- `soul`
- `tools`

### Response

```json
{
  "name": "user",
  "content": "..."
}
```

### Tested error behavior

- `400 invalid_name...`：未対応の `name`（`backend/tests/integration/test_api_system_prompts.py`）
- `401 Invalid API key`：認証有効時に header が不正または未指定（`backend/tests/integration/test_api_system_prompts.py`）

## PUT /v1/system-prompts/{name}

名前付き system prompt file を更新します。

### Request body

```json
{
  "content": "updated prompt text"
}
```

### Response

```json
{
  "name": "user",
  "content": "updated prompt text"
}
```

### Tested error behavior

- `400 invalid_name...`：未対応の `name`（`backend/tests/integration/test_api_system_prompts.py`）
