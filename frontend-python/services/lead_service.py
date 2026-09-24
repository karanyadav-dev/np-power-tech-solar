"""
NP POWER TECH SOLAR - Lead Service
Wraps lead-related API calls.
"""

from api.client import api_client
from typing import Dict, Any, Optional


class LeadService:
    """Service for managing leads through backend API."""

    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead (public — no auth required)."""
        return api_client.post("/api/v1/leads", json=data)

    @staticmethod
    def list(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        """List leads (requires auth)."""
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/leads", params=params)

    @staticmethod
    def get(lead_id: str) -> Dict[str, Any]:
        return api_client.get(f"/api/v1/leads/{lead_id}")

    @staticmethod
    def update(lead_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.patch(f"/api/v1/leads/{lead_id}", json=data)

    @staticmethod
    def update_status(lead_id: str, status: str, notes: Optional[str] = None) -> Dict[str, Any]:
        return api_client.patch(
            f"/api/v1/leads/{lead_id}/status",
            json={"status": status, "notes": notes},
        )

    @staticmethod
    def assign(lead_id: str, assigned_to: str) -> Dict[str, Any]:
        return api_client.post(f"/api/v1/leads/{lead_id}/assign", json={"assignedTo": assigned_to})

    @staticmethod
    def add_followup(lead_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.post(f"/api/v1/leads/{lead_id}/followups", json=data)

    @staticmethod
    def list_followups(lead_id: str) -> Dict[str, Any]:
        return api_client.get(f"/api/v1/leads/{lead_id}/followups")


lead_service = LeadService()