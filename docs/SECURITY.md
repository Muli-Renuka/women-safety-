# Security notes
- Django password hashing and session authentication are used. CSRF middleware remains enabled.
- API contact, alert, and journey querysets are owner-scoped.
- DRF throttles are enabled as a baseline; tune for deployment.
- Configure a strong `DJANGO_SECRET_KEY`, `DEBUG=false`, `ALLOWED_HOSTS`, HTTPS, secure cookies, reverse-proxy headers, restricted CORS, and monitored backups before production.
- SQLite is for local development/small single-instance use; evaluate production storage and retention requirements.
- IndexedDB is not encrypted. Shared-device users should sign out and clear local history.
- Never commit `.env`, database files containing user data, credentials, or real contact details.
- Self-service account deletion, provider-backed notifications, and full audit/retention tooling are not yet implemented.
