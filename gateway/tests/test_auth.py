from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_missing_api_key():
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen3-0.6B",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        },
    )

    assert response.status_code == 401