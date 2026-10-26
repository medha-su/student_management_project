# Student Management API

An individual Python backend project for the EWB internship assignment. It implements student-record CRUD with **FastAPI**, **SQLite**, **SQLAlchemy**, **Pydantic validation**, modular routers, environment-based configuration, and interactive Swagger documentation. An optional local AI endpoint can use **Ollama + LangChain**.

## Assignment coverage

- **Create:** `POST /students`
- **Read/list/filter:** `GET /students`, `GET /students/{student_id}`
- **Update:** `PUT /students/{student_id}` and `PATCH /students/{student_id}`
- **Delete:** `DELETE /students/{student_id}`
- Required fields: unique database ID, name, date of birth, and at least one contact method (email or phone).
- Optional fields: course, address, enrollment date.
- SQLite persistence; SQLAlchemy ORM models; Pydantic request/response schemas.
- Missing-record errors (`404`), duplicate email (`409`), invalid input (`422`).
- Swagger UI at `/docs`; health endpoint at `/health`.
- Optional AI: `POST /query-ai`, grounded in retrieved records and disabled by default.

## Project structure

```text
student_management_project/
├── main.py
├── requirements.txt
├── requirements-ai.txt
├── requirements-dev.txt
├── tests/
│   └── smoke_test.py
├── .env.example
├── .gitignore
├── README.md
└── app/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    └── routes/
        ├── __init__.py
        ├── base.py
        ├── create_student.py
        ├── get_student.py
        ├── update_student.py
        ├── delete_student.py
        └── ai_query.py
```

## Prerequisites

- Python 3.10 or newer
- `pip`
- Optional AI extension: Ollama installed locally

## Installation and run

Run commands from the project root.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn main:app --reload
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore and test the API. The SQLite database file (`students.db`) is created automatically on startup. Keep `.env` and database files out of Git.

## Run the automated smoke test

After installing the main requirements, run this from the project root:

```bash
python tests/smoke_test.py
```

The test creates a separate temporary SQLite database and checks the CRUD endpoints, filtering, validation errors, missing records, duplicate email handling, optional-AI-disabled behavior, and OpenAPI generation. It does not modify your `students.db` file. The optional Ollama integration requires a running local Ollama service and an installed model, so it is not exercised by this smoke test.

## API examples

### Create a student

`POST /students`

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2007-04-15",
  "email": "aarav.demo@example.com",
  "phone": "9000000001",
  "course": "Python Backend Development",
  "address": "Sample address",
  "enrollment_date": "2026-10-01"
}
```

This is fictional sample data. Do not enter real student personal information into a public demo.

### List and filter

- `GET /students`
- `GET /students?name=aarav`
- `GET /students?course=python&limit=20&offset=0`

### Retrieve one

`GET /students/1`

### Update selected fields

`PATCH /students/1`

```json
{
  "course": "FastAPI Development"
}
```

### Delete

`DELETE /students/1`

A successful deletion returns `204 No Content`.

## Optional local AI extension (not required by assignment)

The core CRUD application works without Ollama or LangChain. To enable the bonus endpoint:

1. Install Ollama from its official website.
2. Start the local service if it is not already running.
3. Download a model, for example:

   ```bash
   ollama pull llama3.2
   ```

4. Install optional dependencies:

   ```bash
   pip install -r requirements-ai.txt
   ```

5. In `.env`, set:

   ```dotenv
   AI_ENABLED=true
   OLLAMA_MODEL=llama3.2
   OLLAMA_BASE_URL=http://localhost:11434
   ```

6. Restart Uvicorn and test `POST /query-ai` with:

   ```json
   {
     "question": "How many students are in the available records?"
   }
   ```

The backend fetches records from SQLite and passes a bounded JSON context to the local model. The model is not allowed to execute SQL. AI responses can still be imperfect; verify answers against `GET /students`. Use only fictional/demo data.

## Troubleshooting

- **`ModuleNotFoundError`:** Activate the project's virtual environment and run `pip install -r requirements.txt`.
- **Uvicorn not found:** Run `python -m uvicorn main:app --reload` from the project root.
- **Import errors:** Confirm `main.py` is at the root and the `app/` and `app/routes/` folders contain `__init__.py`.
- **Port already in use:** Stop the other process or run `python -m uvicorn main:app --reload --port 8001`.
- **AI endpoint returns 503:** This is expected while AI is disabled or Ollama/model/dependencies are unavailable. The mandatory CRUD endpoints do not depend on AI.
- **Validation returns 422:** Check the JSON field names, date format (`YYYY-MM-DD`), required name/date of birth, and that at least one of email or phone is supplied.

## GitHub submission checklist

1. Run the API locally and exercise all CRUD routes in `/docs`.
2. Verify missing IDs return `404` and malformed input returns `422`.
3. Keep `.env`, `venv/`, and `*.db` out of the repository.
4. Push the complete source directory to your GitHub repository.
5. Submit the repository URL through the channel specified by your trainer.

## Architecture notes

- `main.py`: application entry point and startup table creation.
- `app/config.py`: Pydantic Settings reads `.env` values.
- `app/database.py`: SQLAlchemy engine, session factory, and dependency.
- `app/models.py`: persistent database table definition.
- `app/schemas.py`: Pydantic input/output validation.
- `app/routes/`: isolated route modules for each CRUD operation and optional AI.
