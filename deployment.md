# Deployment Guide: GitStat<sup>&trade;</sup>

This guide covers the steps required to run GitStat Next locally for development and deploy it to a production environment.

## 1. Prerequisites

- **Python**: 3.12+ (3.14 recommended)
- **uv**: Modern Python package manager
- **PostgreSQL**: 15+ (with `asyncpg` compatibility)
- **Redis**: 6.2+ for caching
- **GitHub OAuth App**: Create one at [GitHub Developer Settings](https://github.com/settings/developers)
  - **Callback URL**: `http://localhost:8000/api/v1/auth/callback` (for local)

---

## 2. Local Development Setup

### 1. Clone & Install
```bash
# Sync dependencies and create virtual environment
uv sync --all-extras
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in the required values:
```bash
cp .env.example .env
```

**Required Variables:**
- `DATABASE_URL`: `postgresql+asyncpg://user:pass@localhost:5432/gitstat_db`
- `REDIS_URL`: `redis://localhost:6379`
- `SECRET_KEY`: Long random string for session signing
- `GITHUB_CLIENT_ID`: From your GitHub OAuth App
- `GITHUB_CLIENT_SECRET`: From your GitHub OAuth App
- `GITHUB_TOKEN_ENCRYPTION_KEY`: A 32-byte URL-safe base64-encoded string.
  - *Generate one:* `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

### 3. Run Application
```bash
# Start the development server
uv run uvicorn app.main:app --reload
```
Access the app at `http://localhost:8000`.

---

## 3. Production Deployment

### 1. Infrastructure Requirements
- **Process Manager**: Gunicorn with Uvicorn workers
- **Reverse Proxy**: Nginx or Cloudflare (for SSL termination)
- **Database**: Managed PostgreSQL (AWS RDS, Supabase, etc.)
- **Cache**: Managed Redis (AWS ElastiCache, Upstash, etc.)

### 2. Security Hardening Checklist
- [ ] **Encryption Key**: Ensure `GITHUB_TOKEN_ENCRYPTION_KEY` is unique and kept secret. Rotating this key will invalidate existing tokens in the DB.
- [ ] **HTTPS**: Always run behind SSL. Set `SESSION_COOKIE_SECURE=True` in production.
- [ ] **Secret Management**: Use a secret manager (AWS Secrets Manager, Doppler, etc.) instead of plain `.env` files.

### 3. Deployment via Docker (Recommended)
```bash
# Build the production image
docker build -t gitstat-next .

# Run with environment variables
docker run -d \
  --name gitstat \
  -p 8000:8000 \
  --env-file .env.prod \
  gitstat-next
```

### 4. Direct Deployment (Standard Linux)
```bash
# Install dependencies
uv sync --no-dev

# Run with Gunicorn (4 workers recommended for 2-core CPU)
uv run gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000
```

---

## 4. Maintenance & Monitoring

### Database Migrations
If using Alembic for migrations (recommended for production):
```bash
uv run alembic upgrade head
```

### Performance Tuning
- **API Concurrency**: The `GitHubService` is configured with a semaphore (default: 5) to prevent rate limiting. Adjust this based on your GitHub App's tier.
- **Cache TTL**: GitHub stats are cached for 1 hour; AI resumes for 24 hours. Adjust in `app/services/` if needed.

### Logs
Structured logging is enabled. In production, pipe these to a log aggregator (Datadog, ELK, or CloudWatch).
