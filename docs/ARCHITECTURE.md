# Architecture
React/Vite serves the PWA shell. Django REST Framework provides session-authenticated APIs and SQLite persistence. IndexedDB stores device-local event records and retry state. SOS events are saved locally before network submission; client UUIDs provide per-user idempotency. The service worker caches shell assets only and deliberately bypasses `/api/`.

Core flow: user activates countdown → optional consented geolocation → IndexedDB write → API submission if online → status reconciled from API response. Notification provider is not configured by default.
