# EgoGraph Frontend Capacitor Legacy

`endo-ava/ego-graph` モノレポから切り出した、legacy app 用の repository です。

## Overview

このリポジトリには、EgoGraph の旧モバイル / Web クライアントと、そのクライアント専用 backend を同居させて管理します。

EgoGraph エージェントと対話するための ChatGPT ライクなインターフェースで、旧世代のモバイルファースト実装を保存しています。

- Runtime: React 19 + Vite 6 + TypeScript 5
- Mobile shell: Capacitor 8 (Android)
- State: TanStack Query + Zustand
- Styling: Tailwind CSS 4
- Mobile First: Android / Capacitor 向け UI を優先
- Web Compatible: 標準的な SPA としても動作

## Repository Layout

- `frontend/`: Legacy React + Capacitor frontend
- `frontend/src/`: アプリケーション本体
- `frontend/android/`: Capacitor Android プロジェクト
- `frontend/public/`: 静的アセットと manifest
- `backend/`: legacy frontend 専用 backend
- `.github/workflows/ci.yml`: standalone 用 CI
- `.github/workflows/deploy-capacitor-updater.yml`: OTA 配信用 workflow

## Architecture

- Framework: React 19 + Vite 6 + TypeScript 5
- Mobile Runtime: Capacitor 8
- UI System: Tailwind CSS 4 + shadcn/ui
- State Management:
  - Server State: TanStack Query
  - Client State: Zustand

### Key Directories

- `frontend/src/components/chat/`: チャット UI コンポーネント
- `frontend/src/lib/api.ts`: backend 接続用 API client
- `frontend/src/hooks/`: UI / chat / thread 関連 hooks
- `frontend/src/main.tsx`: CapacitorUpdater 初期化を含む app entry point
- `docs/40.deploy/`: Legacy Capacitor の deploy / architecture docs
- `docs/20.technical_selections/02_frontend.md`: 旧 frontend 技術選定記録

## Prerequisites

- Node.js 20+
- npm 10+
- Android Studio（Android ビルド時）
- 利用対象の EgoGraph backend

## Environment Variables

`frontend/.env.example` をもとに `frontend/.env` を作成してください。

通常利用で必要:

- `VITE_API_URL`: backend の base URL。例: `http://localhost:8000`
- `VITE_API_KEY`: backend が `X-API-Key` を要求する場合に送る API key
- `VITE_DEBUG`: API デバッグログを有効にする場合は `true`、通常は `false`

Capacitor OTA で任意:

- `CAPACITOR_UPDATER_URL`: `latest.json` の URL。`npx cap sync` や release build 時に利用されます

## Local Development

依存関係のインストール:

```bash
cd frontend
npm ci
```

Web 開発サーバー起動:

```bash
cd frontend
npm run dev
```

既定の Vite URL は `http://localhost:5174` です。

## Verification Commands

ローカルでも CI でも、以下を基準コマンドとして使用します。

```bash
cd frontend
npm run lint
npx tsc --noEmit
npm run build
npm run test:run
```

## Android / Capacitor Notes

`frontend/android/` が存在しない場合のみ Android 初期化を実行します。

```bash
cd frontend
npm run android:init
```

Web アセット同期と Capacitor 管理ファイルの再生成:

```bash
cd frontend
npm run build
npm run android:sync
```

Android Studio を開く:

```bash
cd frontend
npm run android:open
```

補足:

- `frontend/android/capacitor.settings.gradle` と `frontend/android/app/capacitor.build.gradle` は生成ファイルです
- 依存関係や plugin 構成が変わったら `npm run android:sync` を再実行してください
- OTA 設定は `CAPACITOR_UPDATER_URL` が設定されている場合のみ注入されます

## OTA / Capacitor Updater

このアプリは引き続き Capgo OTA update をサポートします。

- runtime 側 integration: `frontend/src/main.tsx` の `CapacitorUpdater.notifyAppReady()`
- build 時設定: `frontend/capacitor.config.ts`
- 配信 automation: `.github/workflows/deploy-capacitor-updater.yml`

OTA workflow で期待する GitHub Actions secrets:

- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_ENDPOINT_URL`
- `R2_PUBLIC_BUCKET_NAME`
- `R2_PUBLIC_BASE_URL`
- `CAPACITOR_UPDATER_URL`
- `VITE_API_URL`
- `VITE_API_KEY`

## Backend Contract

この client が利用する backend endpoint は以下です。

- `POST /v1/chat`
- `GET /v1/chat/models`
- `GET /v1/threads`
- `GET /v1/threads/{thread_id}`
- `GET /v1/threads/{thread_id}/messages`
- `GET /v1/system-prompts/{name}`
- `PUT /v1/system-prompts/{name}`

request / response shape や error behavior は [API.md](./API.md) を参照してください。

## Current Status

- `frontend/` への再編は完了済み
- `backend/` は legacy chat API を同居させるために追加済み


## Legacy Deploy Docs

Capacitor 関連の旧ドキュメントは `docs/40.deploy/` に移動しています。

- `docs/40.deploy/frontend-android-capacitor.md`
- `docs/40.deploy/capacitor.md`

## Troubleshooting

- `401 Invalid API key`: backend が認証を有効化している場合は `VITE_API_KEY` を設定してください
- CORS errors: backend 側で frontend origin が許可されているか確認してください
- Android Gradle / plugin path が崩れた: `npm run android:sync` を再実行してください
- OTA が有効化されない: `CAPACITOR_UPDATER_URL` と workflow secrets を確認してください
