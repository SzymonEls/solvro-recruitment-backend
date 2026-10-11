# Cocktails API (Solvro recruitment task)

REST API for managing cocktails and their ingredients, built with Django, Django REST Framework and SQLite.

## Setup

Requires Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.