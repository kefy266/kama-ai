# -*- coding: utf-8 -*-
"""
KAMA AI 1.0 Official Python SDK
Fast, reliable client for KAMA AI Foundation Model & Content Moderation API
Release 1.0.0
"""

import json
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

class KamaAI:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _post(self, endpoint: str, payload: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise RuntimeError(f"KAMA API Error ({e.code}): {err_body}") from e
        except Exception as e:
            raise RuntimeError(f"KAMA Connection Error: {str(e)}") from e

    def analyze(self, text: str) -> dict:
        """Analyzes single text for 7 toxicity classes, PII and rephrasing."""
        return self._post("/v1/analyze", {"text": text})

    def denetle(self, mesaj: str) -> dict:
        """Alias for analyze."""
        return self.analyze(mesaj)

    def batch(self, items: List[str]) -> dict:
        """Batch analyze multiple sentences in a single call."""
        return self._post("/v1/batch", {"items": items})

    def diplomat(self, text: str) -> dict:
        """Generates 4 polite tones from toxic content."""
        return self._post("/v1/diplomat", {"text": text})

    def mask_pii(self, text: str) -> dict:
        """Sanitizes KVKK / PII sensitive data."""
        return self._post("/v1/mask-pii", {"text": text})

    def model_info(self) -> dict:
        """Returns model specifications and architecture."""
        url = f"{self.base_url}/v1/model-info"
        with urllib.request.urlopen(url, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
