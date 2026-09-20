# -*- coding: utf-8 -*-
"""
KAMA AI 6.0 - Official Python SDK
Origin Edge Deep Neural Architecture
"""

import requests
from typing import Dict, Any, Optional

class KamaAI:
    """Official Python Client for KAMA AI 6.0 API & Local Engine."""
    
    def __init__(self, api_url: str = "https://ai.oedge.xyz", api_key: Optional[str] = None):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Performs full cognitive analysis on text."""
        endpoint = f"{self.api_url}/api/v6/analyze"
        res = requests.post(endpoint, json={"metin": text}, headers=self.headers, timeout=10)
        res.raise_for_status()
        return res.json()

    def rewrite_diplomat(self, text: str, tone: str = "KURUMSAL") -> Dict[str, Any]:
        """Rewrites hostile/toxic text into a polite, diplomatic tone."""
        endpoint = f"{self.api_url}/api/v6/diplomat"
        res = requests.post(endpoint, json={"metin": text, "ton": tone}, headers=self.headers, timeout=10)
        res.raise_for_status()
        return res.json()

    def mask_pii(self, text: str) -> Dict[str, Any]:
        """Masks sensitive KVKK data (TC Kimlik, IBAN, Phone, Cards)."""
        endpoint = f"{self.api_url}/api/v6/mask-pii"
        res = requests.post(endpoint, json={"metin": text}, headers=self.headers, timeout=10)
        res.raise_for_status()
        return res.json()

    def check_child_safety(self, text: str) -> bool:
        """Returns True if text is safe for kids (EdgeMail Çocuk)."""
        res = self.analyze(text)
        return res.get("cocuk_icin_guvenli_mi", False)
