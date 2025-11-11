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
git clone https://github.com/your-org/codebreaker-api.git
cd codebreaker-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
- Copy `codebreaker/settings.py` to a dedicated production settings module or use environment variables.
- Set `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASES` via environment variables for production.
- Example SQLite development settings are already included.

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
Tests use Django’s test runner and DRF’s APIClient:
```sh
python manage.py test games.tests
```

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

