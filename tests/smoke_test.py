"""Repeatable smoke test for the Student Management API.

Run from the project root after installing requirements:
    python tests/smoke_test.py
The test uses a temporary SQLite database and does not touch students.db.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
TEST_DIR = Path(tempfile.mkdtemp(prefix="student_management_smoke_"))
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DIR / 'smoke_test.db'}"
os.environ["AI_ENABLED"] = "false"

from fastapi.testclient import TestClient  # noqa: E402
import main  # noqa: E402


def main_test() -> None:
    passed = 0
    total = 0

    def check(label: str, condition: bool, detail: str = "") -> None:
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"PASS | {label}")
        else:
            print(f"FAIL | {label}" + (f" | {detail}" if detail else ""))

    with TestClient(main.app) as client:
        response = client.get("/health")
        check("health endpoint", response.status_code == 200, response.text)

        response = client.get("/")
        check("root endpoint", response.status_code == 200 and "/docs" in response.json().get("docs", ""), response.text)

        response = client.get("/students")
        check("initial student list is empty", response.status_code == 200 and response.json() == [], response.text)

        payload = {
            "name": "  Aarav Sharma  ",
            "date_of_birth": "2005-04-12",
            "email": "aarav.test@example.com",
            "phone": "9876543210",
            "course": "Python",
            "address": "Test address",
            "enrollment_date": "2025-01-10",
        }
        response = client.post("/students", json=payload)
        created = response.json() if response.status_code == 201 else {}
        student_id = created.get("id")
        check("create student and trim whitespace", response.status_code == 201 and created.get("name") == "Aarav Sharma", response.text)

        response = client.post("/students", json={**payload, "name": "Another Student"})
        check("duplicate email returns 409", response.status_code == 409, response.text)

        response = client.get(f"/students/{student_id}")
        check("retrieve student by ID", response.status_code == 200 and response.json().get("id") == student_id, response.text)

        response = client.get("/students?name=AARAV")
        check("case-insensitive name filter", response.status_code == 200 and len(response.json()) == 1, response.text)

        response = client.get("/students?course=yth")
        check("course filter", response.status_code == 200 and len(response.json()) == 1, response.text)

        check("pagination validation", client.get("/students?limit=0").status_code == 422)
        check("contact method is required", client.post("/students", json={"name": "No Contact", "date_of_birth": "2000-01-01"}).status_code == 422)
        check("invalid email is rejected", client.post("/students", json={"name": "Bad Email", "date_of_birth": "2000-01-01", "email": "not-an-email"}).status_code == 422)
        check("unknown create fields are rejected", client.post("/students", json={**payload, "unexpected": "x"}).status_code == 422)
        check("blank name is rejected", client.post("/students", json={**payload, "name": "   ", "email": "blank@example.com"}).status_code == 422)

        response = client.put(f"/students/{student_id}", json={"course": "FastAPI"})
        check("PUT update", response.status_code == 200 and response.json().get("course") == "FastAPI", response.text)

        response = client.patch(f"/students/{student_id}", json={"address": "Updated address"})
        check("PATCH update", response.status_code == 200 and response.json().get("address") == "Updated address", response.text)

        check("empty update is rejected", client.patch(f"/students/{student_id}", json={}).status_code == 422)
        check("null name is rejected safely", client.patch(f"/students/{student_id}", json={"name": None}).status_code == 422)
        check("null date of birth is rejected safely", client.patch(f"/students/{student_id}", json={"date_of_birth": None}).status_code == 422)
        check("unknown update fields are rejected", client.patch(f"/students/{student_id}", json={"unexpected": "x"}).status_code == 422)
        check("removing all contact methods is rejected", client.patch(f"/students/{student_id}", json={"email": None, "phone": None}).status_code == 422)
        check("missing GET returns 404", client.get("/students/99999").status_code == 404)
        check("missing PUT returns 404", client.put("/students/99999", json={"name": "Nobody"}).status_code == 404)
        check("missing DELETE returns 404", client.delete("/students/99999").status_code == 404)
        check("AI endpoint safely returns 503 when disabled", client.post("/query-ai", json={"question": "How many students?"}).status_code == 503)
        check("OpenAPI schema is generated", client.get("/openapi.json").status_code == 200)

        response = client.delete(f"/students/{student_id}")
        check("delete existing student returns 204", response.status_code == 204, response.text)
        check("deleted student cannot be retrieved", client.get(f"/students/{student_id}").status_code == 404)

    print(f"\nRESULT: {passed}/{total} checks passed")
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main_test()
