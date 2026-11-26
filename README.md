# Product Catalog — Django Take-Home

A Django project modelling **products**, **categories** and **tags**, with an HTML page to
search products by description and filter by category and tags (combinable).

> 🚧 Work in progress. Sections marked _TODO_ are filled in as features land.

## Tech stack

- Python 3.12+ (developed on 3.14), Django 5.2 LTS
- SQLite by default; PostgreSQL via Docker Compose
- Django templates (no front-end framework; no build step)
- pytest + pytest-django, ruff, GitHub Actions CI (lint + tests on SQLite and PostgreSQL)

## Quick start (venv + SQLite)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env               # Windows: copy .env.example .env
python manage.py migrate
python manage.py runserver
```

_TODO: load sample data fixture, create superuser._

## Quick start (Docker + PostgreSQL)

```bash
docker compose up --build
```

App: http://localhost:8000 · Admin: http://localhost:8000/admin/

## Running tests and linting

```bash
pytest
ruff check . && ruff format --check .
```

## Design decisions

_TODO_

## Assumptions

_TODO_

## With more time I would…

_TODO_

## AI usage

_TODO: document how and where AI tools were used (required by the assignment's AI policy)._
