# EgoGraph Frontend Capacitor Legacy

`endo-ava/ego-graph` モノレポから履歴を保持したまま切り出した、Legacy React + Capacitor フロントエンドです。

## Overview

このリポジトリには、EgoGraph の旧モバイル / Web クライアントが standalone repo として格納されています。

- Runtime: React 19 + Vite 6 + TypeScript 5
- Mobile shell: Capacitor 8 (Android)
- State: TanStack Query + Zustand
- Styling: Tailwind CSS 4

## Repository Layout

- `src/`: アプリケーション本体
- `android/`: Capacitor Android プロジェクト
- `public/`: 静的アセットと manifest
- `.github/workflows/ci.yml`: standalone 用 CI
- `.github/workflows/deploy-capacitor-updater.yml`: OTA 配信用 workflow

## Prerequisites

- Node.js 20+
- npm 10+
- Android Studio（Android ビルド時）
- 利用対象の EgoGraph backend

## Environment Variables

`.env.example` をもとに `.env` を作成してください。

通常利用で必要:

- `VITE_API_URL`: backend の base URL。例: `http://localhost:8000`
- `VITE_API_KEY`: backend が `X-API-Key` を要求する場合に送る API key
- `VITE_DEBUG`: API デバッグログを有効にする場合は `true`、通常は `false`

Capacitor OTA で任意:

- `CAPACITOR_UPDATER_URL`: `latest.json` の URL。`npx cap sync` や release build 時に利用されます

## Local Development

依存関係のインストール:

```bash
npm ci
```

Web 開発サーバー起動:

```bash
npm run dev
```

既定の Vite URL は `http://localhost:5174` です。

## Verification Commands

ローカルでも CI でも、以下を基準コマンドとして使用します。

```bash
npm run lint
npx tsc --noEmit
npm run build
npm run test:run
```

## Android / Capacitor Notes

`android/` が存在しない場合のみ Android 初期化を実行します。

```bash
npm run android:init
```

Web アセット同期と Capacitor 管理ファイルの再生成:

```bash
npm run build
npm run android:sync
```

Android Studio を開く:

```bash
npm run android:open
```

補足:

- `android/capacitor.settings.gradle` と `android/app/capacitor.build.gradle` は生成ファイルです
- 依存関係や plugin 構成が変わったら `npm run android:sync` を再実行してください
- OTA 設定は `CAPACITOR_UPDATER_URL` が設定されている場合のみ注入されます

## OTA / Capacitor Updater

このアプリは引き続き Capgo OTA update をサポートします。

- runtime 側 integration: `src/main.tsx` の `CapacitorUpdater.notifyAppReady()`
- build 時設定: `capacitor.config.ts`
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


## Legacy Deploy Docs

Capacitor 関連の旧ドキュメントは `docs/40.deploy/` に移動しています。

- `docs/40.deploy/frontend-android-capacitor.md`
- `docs/40.deploy/capacitor.md`

## Troubleshooting

- `401 Invalid API key`: backend が認証を有効化している場合は `VITE_API_KEY` を設定してください
- Android Gradle / plugin path が崩れた: `npm run android:sync` を再実行してください
- OTA が有効化されない: `CAPACITOR_UPDATER_URL` と workflow secrets を確認してください
