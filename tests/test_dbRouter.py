from fastapi.testclient import TestClient
from fastapi import status

from subjectflow_backend.main import app

client = TestClient(app)


def test_get_subject():
    response = client.post("/db/subject")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
