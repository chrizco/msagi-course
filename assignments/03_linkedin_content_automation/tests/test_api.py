from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "LinkedIn Content Automation API is running"
    }

# This test:

## calls the / endpoint;
## checks that it returns HTTP 200;
## checks that the response text is correct.