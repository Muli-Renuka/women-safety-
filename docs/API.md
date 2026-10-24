# API contract
All endpoints are under `/api/v1/`. Session auth uses cookies and CSRF for unsafe methods. JSON errors use DRF validation responses.

- `POST auth/register/`: username, optional email, password.
- `POST auth/login/`: username/password; returns user and CSRF token.
- `POST auth/logout/`: end session.
- `GET auth/me/`: current user and CSRF token.
- `/contacts/`: GET/POST; `/contacts/{id}/`: GET/PATCH/PUT/DELETE. Owner-scoped.
- `/alerts/`: GET/POST; `/alerts/{id}/`: GET; `/alerts/{id}/acknowledge/` and `/alerts/{id}/cancel/`: POST. Duplicate UUID returns existing record.
- `/journeys/`: CRUD; `/journeys/{id}/check_in/` and `/journeys/{id}/end/`: POST.
- `/api/health/`: basic health check.

Server acceptance is not notification delivery. Notification status is `NOT_CONFIGURED` until a provider integration is implemented and configured.
