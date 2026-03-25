# API Contract

This document covers every backend endpoint consumed by the legacy Capacitor frontend.

## Common Behavior

- Base URL comes from `VITE_API_URL`
- All requests send `Content-Type: application/json`
- `X-API-Key` is sent only when `VITE_API_KEY` is non-empty
- The backend treats API-key auth as optional globally; when `BACKEND_API_KEY` is configured, missing or invalid keys return `401 Invalid API key`
- Client errors are surfaced as `ApiRequestError(status, detail)` using the backend JSON field `detail` when present

## POST /v1/chat

Send a chat request to the backend agent.

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

- `messages`: array of `{ role, content }`
- `stream`: optional boolean; `true` enables SSE streaming
- `thread_id`: optional existing thread UUID/string
- `model_name`: optional backend-supported model identifier

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

When `stream=true`, the same endpoint returns `text/event-stream` SSE chunks. The client parses `data: ...` payloads into:

- `delta`
- `tool_call`
- `tool_result`
- `done`
- `error`

### Tested error behavior

- `400 invalid_model_name: ...` for unsupported `model_name` (`backend/tests/integration/test_api_chat_models.py`)
- `400 At least one user message is required` when no user message exists (`backend/tests/integration/test_chat_history.py`)
- `404 Thread not found: ...` when `thread_id` does not exist (`backend/tests/integration/test_chat_history.py`)
- `401 Invalid API key` when auth is enforced and header is missing/invalid (`backend/dependencies.py` + integration tests)

## GET /v1/chat/models

Fetch the list of selectable LLM models.

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

- `401 Invalid API key` without a valid key when auth is enabled (`backend/tests/integration/test_api_chat_models.py`)

## GET /v1/threads

Fetch paginated thread summaries.

### Query parameters

- `limit`: integer, validated server-side with minimum/maximum bounds
- `offset`: integer, `>= 0`

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

- `422` when `limit` exceeds the backend maximum (`backend/tests/integration/test_threads_api.py`)

## GET /v1/threads/{thread_id}

Fetch a single thread summary.

### Response

Same thread object shape as the items returned by `GET /v1/threads`.

### Tested error behavior

- `404 Thread not found: {thread_id}` when the thread does not exist (`backend/tests/integration/test_threads_api.py`, `backend/tests/integration/test_chat_history.py`)

## GET /v1/threads/{thread_id}/messages

Fetch all saved messages for a thread in ascending creation order.

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

- `404 Thread not found: {thread_id}` when the thread does not exist (`backend/tests/integration/test_threads_api.py`, `backend/tests/integration/test_chat_history.py`)

## GET /v1/system-prompts/{name}

Fetch a named system prompt file.

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

- `400 invalid_name...` when `name` is unsupported (`backend/tests/integration/test_api_system_prompts.py`)
- `401 Invalid API key` when auth is enabled and the header is missing/invalid (`backend/tests/integration/test_api_system_prompts.py`)

## PUT /v1/system-prompts/{name}

Persist a named system prompt file.

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

- `400 invalid_name...` when `name` is unsupported (`backend/tests/integration/test_api_system_prompts.py`)
