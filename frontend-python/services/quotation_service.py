"""
NP POWER TECH SOLAR - Quotation Service
Wraps quotation API calls.
"""

from api.client import api_client
from typing import Dict, Any, Optional


class QuotationService:
    """Service for managing quotations."""

    # ---------- Customer / Public ----------
    @staticmethod
    def create_request(data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit wizard data (public)."""
        return api_client.post("/api/v1/quotations", json=data)

    @staticmethod
    def view_quotation(quotation_id: str) -> Dict[str, Any]:
        """Customer views quotation by ID (marks as viewed)."""
        return api_client.get(f"/api/v1/quotations/{quotation_id}/view")

    @staticmethod
    def respond(quotation_id: str, action: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Customer accepts or rejects."""
        return api_client.post(
            f"/api/v1/quotations/{quotation_id}/respond",
            json={"action": action, "reason": reason},
        )

    # ---------- Admin ----------
    @staticmethod
    def list(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        """List quotations (auth required)."""
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/quotations", params=params)

    @staticmethod
    def get(quotation_id: str) -> Dict[str, Any]:
        """Get single quotation with items and versions."""
        return api_client.get(f"/api/v1/quotations/{quotation_id}")

    @staticmethod
    def start_review(quotation_id: str) -> Dict[str, Any]:
        return api_client.post(f"/api/v1/quotations/{quotation_id}/review")

    @staticmethod
    def request_info(quotation_id: str, message: str, required_fields: list = None) -> Dict[str, Any]:
        return api_client.post(
            f"/api/v1/quotations/{quotation_id}/request-info",
            json={"message": message, "requiredFields": required_fields or []},
        )

    @staticmethod
    def verify_info(quotation_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        return api_client.post(
            f"/api/v1/quotations/{quotation_id}/verify",
            json={"notes": notes} if notes else {},
        )

    @staticmethod
    def configure_pricing(quotation_id: str, pricing: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.post(
            f"/api/v1/quotations/{quotation_id}/pricing",
            json=pricing,
        )

    @staticmethod
    def approve(quotation_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        return api_client.post(
            f"/api/v1/quotations/{quotation_id}/approve",
            json={"notes": notes} if notes else {},
        )

    @staticmethod
    def send_to_customer(quotation_id: str) -> Dict[str, Any]:
        return api_client.post(f"/api/v1/quotations/{quotation_id}/send")


quotation_service = QuotationService()