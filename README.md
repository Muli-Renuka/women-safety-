# ShadowMode — Safety that respects your privacy

ShadowMode is a React/Vite Progressive Web App with a Django REST Framework backend and SQLite. This project package includes account/session flows, trusted contacts, emergency event recording, journey check-ins, local offline records, a PWA shell, and a GPS location screen.

> **Safety limitation:** This is a development project, not an emergency service. GPS updates run only while the page is open; the browser may suspend them. The location screen stores coordinates on this device and does not automatically share live location with trusted contacts. SMS/push/email delivery is not configured by default. Do not rely on this app as your only emergency plan.

## Requirements
- Python 3.11 or newer
- Node.js 20 or newer (includes npm)
- Windows 10/11, macOS, or Linux

## Windows PowerShell setup

### 1. Open the correct folder
Extract the ZIP, then open the extracted **ShadowMode** folder in VS Code. The folder you open should directly contain `backend`, `frontend`, `docs`, and this `README.md`.

### 2. Backend setup
Run these commands from the project root (the folder containing `backend` and `frontend`):

```powershell
python -m venv .venv
```

To avoid PowerShell's script execution-policy issue, activation is optional. Use the virtual-environment Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
.\.venv\Scripts\python.exe .\backend\manage.py migrate
.\.venv\Scripts\python.exe .\backend\manage.py check
.\.venv\Scripts\python.exe .\backend\manage.py test
.\.venv\Scripts\python.exe .\backend\manage.py runserver
```

Keep that terminal running. Django should be available at `http://127.0.0.1:8000/`.

If `python` is not recognized but you know the installed Python path, create the environment using its full path, for example:

```powershell
& "$env:LocalAppData\Programs\Python\Python313\python.exe" -m venv .venv
```

### 3. Frontend setup
Open a second terminal at the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173/`. The Vite development server proxies `/api` requests to Django at `http://127.0.0.1:8000`.

## GPS location
1. Sign in to ShadowMode.
2. Open **GPS Location** in the app navigation.
3. Select **Get my location** and allow location permission in the browser.
4. Select **Start live updates** only when you want updates while the page is open.
5. **Stop live updates** to stop watching location. You can clear the locally saved coordinates from the same screen.

Browser GPS requires permission and a secure context (localhost or HTTPS). Location accuracy depends on the device and its available location services. The saved coordinates may be stale when viewed later. Online map tiles require internet access.

## Implementation notes and limitations
- Emergency events are stored locally in IndexedDB before network submission.
- The API supports authenticated, owner-scoped records and idempotent alert identifiers.
- API acceptance does not prove a contact received or acknowledged an alert.
- External SMS/email/push providers are not configured by default; no fake delivery is reported.
- Live GPS sharing to trusted contacts, reliable background tracking, verified help-point data, and self-service account deletion are not fully implemented in this package.
- IndexedDB is not encrypted by default. Avoid using sensitive data on a shared device.
- Production deployment requires HTTPS, secure cookie configuration, secret management, restricted CORS, rate limiting, provider setup, and security/privacy review.

## Useful checks
From the project root:

```powershell
.\.venv\Scripts\python.exe .\backend\manage.py check
.\.venv\Scripts\python.exe .\backend\manage.py test
cd frontend
npm run build
```

The backend and frontend must be tested in your own environment after installing dependencies. A successful local build does not verify physical-device GPS, background behavior, or external notification delivery.

See `docs/` for architecture, API, security, offline behavior, testing, and limitations.
