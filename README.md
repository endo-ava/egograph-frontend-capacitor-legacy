# EgoGraph Frontend Capacitor Legacy

Legacy React + Capacitor frontend extracted from `endo-ava/ego-graph` with preserved history.

## Overview

This repository contains the standalone legacy mobile/web client for EgoGraph.

- Runtime: React 19 + Vite 6 + TypeScript 5
- Mobile shell: Capacitor 8 (Android)
- State: TanStack Query + Zustand
- Styling: Tailwind CSS 4

## Repository Layout

- `src/`: application source code
- `android/`: Capacitor Android project
- `public/`: static assets and manifest
- `.github/workflows/ci.yml`: standalone CI
- `.github/workflows/deploy-capacitor-updater.yml`: OTA asset deployment workflow

## Prerequisites

- Node.js 20+
- npm 10+
- Android Studio (for Android builds)
- A running EgoGraph backend for app usage

## Environment Variables

Create `.env` from `.env.example`.

Required for normal app usage:

- `VITE_API_URL`: backend base URL, for example `http://localhost:8000`
- `VITE_API_KEY`: optional API key header value for backends that require `X-API-Key`
- `VITE_DEBUG`: `true` to enable API debug logging, otherwise `false`

Optional for Capacitor OTA setup:

- `CAPACITOR_UPDATER_URL`: URL to `latest.json` used by Capgo / Capacitor Updater during `npx cap sync` and release builds

## Local Development

Install dependencies from the repository root:

```bash
npm ci
```

Run the web development server:

```bash
npm run dev
```

Default Vite dev URL: `http://localhost:5174`

## Verification Commands

Run the same baseline locally and in CI:

```bash
npm run lint
npx tsc --noEmit
npm run build
npm run test:run
```

## Android / Capacitor Notes

Initialize Android only if the `android/` project does not exist:

```bash
npm run android:init
```

Sync web assets and regenerate Capacitor-managed Android files:

```bash
npm run build
npm run android:sync
```

Open the Android project:

```bash
npm run android:open
```

Important:

- `android/capacitor.settings.gradle` and `android/app/capacitor.build.gradle` are generated files
- after dependency or plugin changes, run `npm run android:sync` again
- OTA configuration is only injected when `CAPACITOR_UPDATER_URL` is set

## OTA / Capacitor Updater

The app still supports Capgo OTA updates.

- Runtime integration lives in `src/main.tsx` via `CapacitorUpdater.notifyAppReady()`
- build-time configuration lives in `capacitor.config.ts`
- deployment automation lives in `.github/workflows/deploy-capacitor-updater.yml`

GitHub Actions secrets expected by the OTA workflow:

- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_ENDPOINT_URL`
- `R2_PUBLIC_BUCKET_NAME`
- `R2_PUBLIC_BASE_URL`
- `CAPACITOR_UPDATER_URL`
- `VITE_API_URL`
- `VITE_API_KEY`

## Backend Contract

This client consumes these backend endpoints:

- `POST /v1/chat`
- `GET /v1/chat/models`
- `GET /v1/threads`
- `GET /v1/threads/{thread_id}`
- `GET /v1/threads/{thread_id}/messages`
- `GET /v1/system-prompts/{name}`
- `PUT /v1/system-prompts/{name}`

See [API.md](./API.md) for request/response shapes and tested error behavior.

## Troubleshooting

- `401 Invalid API key`: set `VITE_API_KEY` to a valid backend key when the backend enforces authentication
- Android Gradle/plugin path issues after dependency changes: run `npm run android:sync`
- OTA not activating: confirm `CAPACITOR_UPDATER_URL` is set for the build and that the deploy workflow secrets exist
