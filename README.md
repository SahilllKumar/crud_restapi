# Task Management REST API

A CRUD REST API built with Flask and SQLite for managing tasks, with input validation, pagination, and pytest coverage.

## Tech Stack
- **Framework:** Flask 3
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Marshmallow
- **Testing:** pytest

## Features
- Full CRUD operations (GET, POST, PUT, DELETE)
- Input validation with clean 400 error responses
- Pagination with `page` and `per_page` query params
- Blueprint + application factory pattern for testability
- 85%+ test coverage with pytest

## Project Structure
```
crud_restapi/
├── app.py            # Application factory
├── extensions.py     # db instance
├── models.py         # Task model
├── routes.py         # API endpoints (blueprint)
├── schemas.py        # Marshmallow validation
└── tests/test_api.py # Unit tests
```

## Setup

```bash
git clone https://github.com/<your-username>/crud_restapi.git
cd crud_restapi
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server runs at `http://localhost:5000`.

## Run Tests
```bash
pytest -v
```

## API Endpoints

| Method | Endpoint        | Description              | Body                              |
|--------|-----------------|--------------------------|-----------------------------------|
| GET    | /tasks          | List tasks (paginated)   | —                                 |
| POST   | /tasks          | Create a task            | `{"title": "string"}`             |
| PUT    | /tasks/\<id\>   | Update a task            | `{"title": "string", "done": bool}` |
| DELETE | /tasks/\<id\>   | Delete a task            | —                                 |

### Sample Requests

```bash
# Create
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# List with pagination
curl "http://localhost:5000/tasks?page=1&per_page=10"

# Update
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy bread", "done": true}'

# Delete
curl -X DELETE http://localhost:5000/tasks/1
```

## Docker

```bash
docker build -t crud-restapi .
docker run -p 5000:5000 crud-restapi
```

## License
MIT
