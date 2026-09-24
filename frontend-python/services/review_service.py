"""
NP POWER TECH SOLAR - Review Service
"""

from api.client import api_client
from typing import Dict, Any


class ReviewService:
    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Public review submission."""
        return api_client.post("/api/v1/reviews", json=data)

    @staticmethod
    def list_public(limit: int = 6) -> Dict[str, Any]:
        """Public published reviews (for homepage)."""
        return api_client.get("/api/v1/reviews/public", params={"limit": limit})


review_service = ReviewService()