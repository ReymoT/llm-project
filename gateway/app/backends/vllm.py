import httpx
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from app.config import settings


class VLLMBackend:
    name = "vllm"

    def __init__(self):
        self.base_url = settings.vllm_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.vllm_api_key}",
            "Content-Type": "application/json",
        }

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def chat_completions(self, payload: dict):
        url = f"{self.base_url}/v1/chat/completions"
        timeout = httpx.Timeout(settings.request_timeout_seconds)

        try:
            if payload.get("stream") is True:
                client = httpx.AsyncClient(timeout=timeout)

                request = client.build_request(
                    "POST", url, json=payload, headers=self.headers
                )

                response = await client.send(request, stream=True)

                if response.status_code >= 400:
                    body = await response.aread()
                    await client.aclose()
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=body.decode("utf-8", errors="ignore"),
                    )

                async def stream_response():
                    try:
                        async for chunk in response.aiter_bytes():
                            yield chunk
                    finally:
                        await response.aclose()
                        await client.aclose()

                return StreamingResponse(
                    stream_response(), media_type="text/event-stream"
                )

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=payload, headers=self.headers)

            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )

            return response.json()

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Backend request timed out",
            )

        except httpx.ConnectError:
            # Integration point for backend health tracking.
            # Later, mark vLLM unhealthy here so the router can fail over to Triton.
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="vLLM backend unavailable",
            )


vllm_backend = VLLMBackend()
