from fastapi import HTTPException, status
from app.backends.vllm import vllm_backend


class BackendRouter:
    def __init__(self):
        self.backends = {"vllm": vllm_backend}

    async def backend_status(self) -> dict[str, bool]:
        status_map = {}

        for name, backend in self.backends.items():
            status_map[name] = await backend.health()

        return status_map

    async def select_backend(self):
        if await vllm_backend.health():
            return vllm_backend

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No healthy inference backend available",
        )


backend_router = BackendRouter()
