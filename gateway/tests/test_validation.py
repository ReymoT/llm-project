from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_rejects_empty_model():
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer openserve-key"},
        json={
            "model": "",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_empty_messages():
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer openserve-key"},
        json={
            "model": "Qwen/Qwen3-0.6B",
            "messages": [],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_invalid_role():
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer openserve-key"},
        json={
            "model": "Qwen/Qwen3-0.6B",
            "messages": [
                {
                    "role": "developer",
                    "content": "Hello",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_empty_content():
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer openserve-key"},
        json={
            "model": "Qwen/Qwen3-0.6B",
            "messages": [
                {
                    "role": "user",
                    "content": "",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_invalid_temperature():
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer openserve-key"},
        json={
            "model": "Qwen/Qwen3-0.6B",
            "temperature": 3.0,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        },
    )

    assert response.status_code == 422