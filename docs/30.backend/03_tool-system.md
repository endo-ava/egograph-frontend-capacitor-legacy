# Legacy Backend Tool System

legacy backend は、LLM がツールを呼び出して EgoGraph データにアクセスできる Tool Use を維持しています。

## 概要

チャット API は、単純なテキスト応答だけでなく、必要に応じて以下のツールを LLM から呼び出します。

- Spotify 統計
- GitHub Worklog
- Browser History

R2 設定が無い場合はツールレジストリを空で初期化し、チャットだけで動作します。

## 構成

```text
Client
  -> /v1/chat
  -> ChatUseCase
  -> ToolExecutor
  -> LLMClient
  -> ToolRegistry
  -> Repository
  -> DuckDB / R2
```

## 主要コンポーネント

### `ChatUseCase`

- スレッドの新規作成 / 継続
- 会話履歴のロードと保存
- ToolExecutor 呼び出し

### `ToolExecutor`

- LLM 応答から tool call を抽出
- 複数ツールの並列実行
- 実行結果を会話履歴へ戻して再問い合わせ
- 最大反復回数の管理

### `ToolRegistry`

- 利用可能ツールの登録
- LLM 向け schema の公開
- 名前ベースのツール解決

### `Repository`

- ビジネスロジックから DuckDB / R2 アクセスを分離
- ツールは repository を通じてデータ取得のみを委譲

## 現在のツール系ファイル

- `backend/usecases/tools/factory.py`
- `backend/usecases/tools/registry.py`
- `backend/domain/tools/spotify/stats.py`
- `backend/domain/tools/github/worklog.py`
- `backend/domain/tools/browser_history/page_views.py`

## ガードレール

- 最大イテレーション数で無限ループを防止
- リクエスト全体のタイムアウトを設定
- ツール例外は構造化して LLM に返却

## 運用メモ

- `backend/api/chat.py` は API 境界のみ担当し、実処理は UseCase 側で行う
- 新しいツールを追加する場合は `domain/tools` と `infrastructure/repositories` をセットで追加し、`usecases/tools/factory.py` で登録する
