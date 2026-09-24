"""
NP POWER TECH SOLAR - Backend API Client
Communicates with Node.js backend via HTTP.
NEVER contains database credentials or backend secrets.
"""

import httpx
from typing import Optional, Any, Dict
from config.settings import settings


class APIClient:
    """HTTP client for the Node.js backend API."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or settings.BACKEND_API_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.BACKEND_API_TIMEOUT
        self._access_token: Optional[str] = None

    def set_token(self, token: Optional[str]) -> None:
        self._access_token = token

    def clear_token(self) -> None:
        self._access_token = None

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        return headers

    def _handle(self, response: httpx.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            data = {"success": False, "error": {"code": "INVALID_RESPONSE", "message": response.text[:200]}}
        if response.status_code >= 400 and isinstance(data, dict):
            data.setdefault("success", False)
            data.setdefault("_status", response.status_code)
        return data

    def get(self, path: str, params: Optional[dict] = None) -> Dict[str, Any]:
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.get(path, params=params, headers=self._headers())
                return self._handle(response)
        except Exception as e:
            return {"success": False, "error": {"code": "REQUEST_FAILED", "message": str(e)}}

    def post(self, path: str, json: Optional[dict] = None) -> Dict[str, Any]:
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.post(path, json=json, headers=self._headers())
                return self._handle(response)
        except Exception as e:
            return {"success": False, "error": {"code": "REQUEST_FAILED", "message": str(e)}}

    def patch(self, path: str, json: Optional[dict] = None) -> Dict[str, Any]:
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.patch(path, json=json, headers=self._headers())
                return self._handle(response)
        except Exception as e:
            return {"success": False, "error": {"code": "REQUEST_FAILED", "message": str(e)}}

    def delete(self, path: str, json: Optional[dict] = None) -> Dict[str, Any]:
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.request("DELETE", path, json=json, headers=self._headers())
                return self._handle(response)
        except Exception as e:
            return {"success": False, "error": {"code": "REQUEST_FAILED", "message": str(e)}}

    def health_check(self) -> Dict[str, Any]:
        return self.get("/api/health")


api_client = APIClient()