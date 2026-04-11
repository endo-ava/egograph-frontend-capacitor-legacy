# Legacy Backend Streaming

legacy chat API は、SSE ベースのストリーミング応答に対応しています。

## 目的

- LLM のテキスト生成をリアルタイムに表示する
- ツール実行中の進捗を段階的に返す
- 最終的な `thread_id` や usage 情報を完了イベントで返す

## フロー

```text
Client
  -> POST /v1/chat (stream=true)
  -> API Layer
  -> ChatUseCase.execute_stream()
  -> ToolExecutor.execute_loop_stream()
  -> LLM Provider stream
  -> SSE chunks
```

## 主なイベント

- `delta`: テキスト断片
- `tool_call`: ツール呼び出し開始
- `tool_result`: ツール実行結果
- `error`: エラー通知
- `done`: 完了通知

## 主要ファイル

- `backend/api/chat.py`
- `backend/usecases/chat/chat_usecase.py`
- `backend/usecases/chat/tool_executor.py`
- `backend/infrastructure/llm/providers/openai.py`
- `backend/infrastructure/llm/providers/anthropic.py`

## 注意点

- OpenAI / Anthropic でストリームの粒度が異なるため、provider 層で `StreamChunk` 相当に正規化して扱う
- ツール引数は断片的に届く場合があるため、executor 側で組み立ててから実行する
- ネットワーク中断時も、可能な範囲でバッファ済みの tool call をフラッシュする方針を取る

## frontend 側との関係

legacy frontend では `/v1/chat` のストリーミング結果を受け取り、逐次描画します。非ストリーミングの request/response だけでなく、SSE の挙動も backend の互換性対象です。
