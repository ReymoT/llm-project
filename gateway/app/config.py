from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    gateway_api_key: str = "openserve-key"
    vllm_base_url: str = "http://localhost:8001"
    vllm_api_key: str = "dev-vllm-key"
    request_timeout_seconds: int = 60


settings = Settings()
