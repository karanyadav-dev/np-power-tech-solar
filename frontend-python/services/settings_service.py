"""
NP POWER TECH SOLAR - Settings Service
Fetches website settings from backend API with caching.
"""

from api.client import api_client
from typing import Dict, Any, Optional
import time


class SettingsService:
    """Website settings — cached for performance."""

    _cache: Optional[Dict[str, str]] = None
    _cache_time: float = 0
    CACHE_TTL = 300  # 5 minutes

    @staticmethod
    def get_public(force_refresh: bool = False) -> Dict[str, str]:
        """Get public settings (cached for 5 minutes)."""
        now = time.time()
        if (
            not force_refresh
            and SettingsService._cache is not None
            and (now - SettingsService._cache_time) < SettingsService.CACHE_TTL
        ):
            return SettingsService._cache

        resp = api_client.get("/api/v1/settings/public")
        if resp.get("success"):
            SettingsService._cache = resp.get("data", {})
            SettingsService._cache_time = now
            return SettingsService._cache

        return SettingsService._cache or {}

    @staticmethod
    def get(key: str, default: str = "") -> str:
        """Get a single setting value."""
        settings = SettingsService.get_public()
        return settings.get(key, default)

    @staticmethod
    def clear_cache():
        """Clear cached settings."""
        SettingsService._cache = None
        SettingsService._cache_time = 0


settings_service = SettingsService()