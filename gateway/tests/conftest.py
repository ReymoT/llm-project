import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["GATEWAY_API_KEY"] = "openserve-key"
os.environ["VLLM_BASE_URL"] = "http://localhost:8001"
os.environ["VLLM_API_KEY"] = "dev-vllm-key"
os.environ["REQUEST_TIMEOUT_SECONDS"] = "60"