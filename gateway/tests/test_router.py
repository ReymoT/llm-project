import pytest
from fastapi import HTTPException
from app.router import BackendRouter

class HealthyBackend:
    name = "healthy"

    async def health(self):
        return True

    async def chat_completions(self, payload):
        return {"backend": self.name, "payload": payload}


class UnhealthyBackend:
    name = "unhealthy"

    async def health(self):
        return False

    async def chat_completions(self, payload):
        return {"backend": self.name, "payload": payload}


@pytest.mark.asyncio
async def test_backend_status_reports_health():
    router = BackendRouter()
    router.backends = {
        "healthy": HealthyBackend(),
        "unhealthy": UnhealthyBackend(),
    }

    status = await router.backend_status()

    assert status == {
        "healthy": True,
        "unhealthy": False,
    }


@pytest.mark.asyncio
async def test_select_backend_returns_healthy_backend(monkeypatch):
    router = BackendRouter()
    healthy_backend = HealthyBackend()

    async def mock_health():
        return True

    monkeypatch.setattr(healthy_backend, "health", mock_health)
    monkeypatch.setattr("app.router.vllm_backend", healthy_backend)

    backend = await router.select_backend()

    assert backend.name == "healthy"


@pytest.mark.asyncio
async def test_select_backend_raises_when_no_backend_healthy(monkeypatch):
    router = BackendRouter()
    unhealthy_backend = UnhealthyBackend()

    async def mock_health():
        return False

    monkeypatch.setattr(unhealthy_backend, "health", mock_health)
    monkeypatch.setattr("app.router.vllm_backend", unhealthy_backend)

    with pytest.raises(HTTPException) as exc:
        await router.select_backend()

    assert exc.value.status_code == 503
    assert exc.value.detail == "No healthy inference backend available"