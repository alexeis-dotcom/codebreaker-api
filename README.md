# Codebreaker API

Codebreaker API is a Django-based backend for a number guessing game. Players create a game with a 4-digit secret code and submit guesses to receive feedback on well-placed and misplaced digits. The API is built with Django REST Framework and documented automatically with drf-spectacular.

## Features
- Create games with validated 4-digit codes
- Submit guesses and receive well-placed/misplaced feedback
- Track guess history, attempts used, and solved status
- Swagger UI (`/docs/swagger/`) and OpenAPI schema (`/docs/schema/`)
- SQLite default database; easily switch to PostgreSQL or others

## Requirements
- Python 3.11+
- pip / virtualenv or Poetry
- Recommended: PostgreSQL for production deployments

## Installation
```sh
git clone https://github.com/alexeis-dotcom/codebreaker-api.git
cd codebreaker-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
- Copy `example.env` to `.env` and update the values for your environment.
  - `DJANGO_SECRET_KEY` – generate a unique value for production.
  - `DJANGO_DEBUG` – set to `False` in production.
  - `DJANGO_ALLOWED_HOSTS` – comma-separated list (no spaces) of allowed hosts.
  - Database variables (`DJANGO_DB_*`) control the default connection; defaults target SQLite.
- Environment variables are loaded automatically via `python-dotenv` in `codebreaker/settings.py`.
- For advanced setups, override any additional Django settings using environment variables or dedicated settings modules.

## Database Setup
```sh
python manage.py migrate
```

To create a superuser for the Django admin:
```sh
python manage.py createsuperuser
```

## Running the Server
```sh
python manage.py runserver
```
- API base path: `http://localhost:8000/api/`
- Swagger UI: `http://localhost:8000/docs/swagger/`
- OpenAPI JSON: `http://localhost:8000/docs/schema/`

All endpoints return JSON and use DRF serializers. Swagger docs show request and response schemas.

## Testing
Tests use pytest with pytest-django and DRF’s `APIClient`. Activate your virtual environment, then run:
```sh
pytest
```

You can also target individual apps or files:
```sh
pytest games/tests/test_views.py
```

## Linting
Run Flake8 to ensure code style consistency:
```sh
flake8
```

## Docker
Build and run the API in a container:
```sh
docker compose up --build
```

The service listens on `http://localhost:8000`. Existing `.env` values are loaded automatically. To run management commands inside the container, use:
```sh
docker compose run --rm web python manage.py migrate
```

### Docker + PostgreSQL
The compose stack includes a `db` service (PostgreSQL 16). Default credentials live in `example.env`; copy to `.env` before starting:
```sh
cp example.env .env
docker compose up --build
```
Override `DJANGO_DB_*` or `POSTGRES_*` variables in `.env` as needed for a different database setup.

## Production Notes
- Configure a real database (e.g., PostgreSQL) in `DATABASES`
- Set up WSGI/ASGI server (e.g., Gunicorn or Uvicorn) behind a reverse proxy
- Run `collectstatic` and serve static files via CDN or web server
- Use HTTPS, secure cookies, and monitor logs/errors

## Contributing
1. Fork the repository
2. Create feature branches (`git checkout -b feature/my-change`)
3. Write tests and ensure they pass
4. Submit a pull request with a clear description

## License
This project is released under the MIT License. See `LICENSE` for details.

