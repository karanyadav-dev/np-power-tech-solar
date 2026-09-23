"""
NP POWER TECH SOLAR - Backend API Client
Communicates with Node.js backend via HTTP.
NEVER contains database credentials or backend secrets.
"""

import httpx
from typing import Optional, Any
from config.settings import settings


class APIClient:
    """HTTP client for the Node.js backend API."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or settings.BACKEND_API_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.BACKEND_API_TIMEOUT
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"},
        )

    def _handle_response(self, response: httpx.Response) -> dict:
        """Handle HTTP response. Raises on error."""
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": {
                    "code": f"HTTP_{e.response.status_code}",
                    "message": e.response.text[:200],
                },
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": {"code": "NETWORK_ERROR", "message": str(e)},
            }

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        """GET request."""
        try:
            response = self._client.get(path, params=params)
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": {"code": "REQUEST_FAILED", "message": str(e)}}

    def post(self, path: str, json: Optional[dict] = None) -> dict:
        """POST request."""
        try:
            response = self._client.post(path, json=json)
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": {"code": "REQUEST_FAILED", "message": str(e)}}

    def health_check(self) -> dict:
        """Check backend health."""
        return self.get("/api/health")

    def close(self):
        """Close HTTP client."""
        self._client.close()


# Singleton instance
api_client = APIClient()