"""
NP POWER TECH SOLAR - Auth Service
Wraps authentication API calls.
"""

from api.client import api_client
from typing import Dict, Any, Optional


class AuthService:
    @staticmethod
    def register(data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.post("/api/v1/auth/register", json=data)

    @staticmethod
    def login(email: str, password: str) -> Dict[str, Any]:
        result = api_client.post("/api/v1/auth/login", json={"email": email, "password": password})
        # Auto-set token on success
        if result.get("success") and "data" in result:
            token = result["data"].get("accessToken")
            if token:
                api_client.set_token(token)
        return result

    @staticmethod
    def logout(refresh_token: Optional[str] = None) -> Dict[str, Any]:
        result = api_client.post("/api/v1/auth/logout", json={"refreshToken": refresh_token} if refresh_token else {})
        api_client.clear_token()
        return result

    @staticmethod
    def me() -> Dict[str, Any]:
        return api_client.get("/api/v1/auth/me")


auth_service = AuthService()