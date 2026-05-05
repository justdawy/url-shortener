# URL Shortener

A fast and simple URL shortener API built with FastAPI, SQLModel, and Redis caching.

## Stack

- **FastAPI** — web framework
- **SQLModel** — ORM and schema validation
- **SQLite** — database
- **Alembic** — migrations
- **Redis** — caching for fast redirects
- **Docker** — containerization

## Project Structure

```
app/
  core/
    config.py       # app settings
    redis.py        # redis client
  db/
    schema.py       # engine, session, create_db_and_tables
  models/
    url.py          # URL, URLCreate, URLUpdate models
  routers/
    urls.py         # all URL endpoints
  utils/
    shortcode.py    # short code generator
  main.py
migrations/         # Alembic migrations
tests/
```

## Getting Started

### With Docker (recommended)

```bash
docker compose up --build
```

### Without Docker

**1. Install dependencies**
```bash
pip install uv
uv sync
```

**2. Start Redis**
```bash
sudo systemctl start redis
```

**3. Run the app**
```bash
uv run fastapi dev
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `URL Shortener` | Application name |
| `DB_NAME` | `urls.db` | Database file name |
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/{short_code}` | Redirect to original URL |
| `GET` | `/urls/` | List all URLs |
| `GET` | `/urls/{short_code}` | Get URL by short code |
| `POST` | `/urls/` | Create short URL |
| `PATCH` | `/urls/{short_code}` | Update URL |
| `DELETE` | `/urls/{short_code}` | Delete URL |

## API Usage

**Create a short URL**
```bash
curl -X POST http://localhost:8000/urls/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://youtube.com"}'
```

**Response**
```json
{
  "id": 1,
  "original_url": "https://youtube.com/",
  "short_code": "aB3xKp",
  "clicks": 0,
  "created_at": "2026-05-01T17:00:00"
}
```

**Redirect**
```bash
curl -L http://localhost:8000/aB3xKp
```

## Running Tests

```bash
uv run pytest -v
```

## Migrations

```bash
# generate migration
uv run alembic revision --autogenerate -m "description"

# apply migrations
uv run alembic upgrade head

# rollback
uv run alembic downgrade -1
```