"""
NP POWER TECH SOLAR - Admin Service
Wraps admin API calls.
"""

from api.client import api_client
from typing import Dict, Any, Optional


class AdminService:
    # PRODUCTS
    @staticmethod
    def list_products(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/products", params=params)

    @staticmethod
    def get_product(product_id: str) -> Dict[str, Any]:
        return api_client.get(f"/api/v1/products/{product_id}")

    @staticmethod
    def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.post("/api/v1/products", json=data)

    @staticmethod
    def update_product(product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.patch(f"/api/v1/products/{product_id}", json=data)

    @staticmethod
    def delete_product(product_id: str) -> Dict[str, Any]:
        return api_client.delete(f"/api/v1/products/{product_id}")

    # CATEGORIES
    @staticmethod
    def list_categories() -> Dict[str, Any]:
        return api_client.get("/api/v1/products/categories")

    @staticmethod
    def create_category(data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.post("/api/v1/products/categories", json=data)

    # REVIEWS
    @staticmethod
    def list_reviews(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/reviews", params=params)

    @staticmethod
    def update_review(review_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.patch(f"/api/v1/reviews/{review_id}", json=data)

    @staticmethod
    def delete_review(review_id: str) -> Dict[str, Any]:
        return api_client.delete(f"/api/v1/reviews/{review_id}")

    # UPLOADS
    @staticmethod
    def list_documents(**filters) -> Dict[str, Any]:
        return api_client.get("/api/v1/uploads", params=filters)

    @staticmethod
    def delete_document(doc_id: str) -> Dict[str, Any]:
        return api_client.delete(f"/api/v1/uploads/{doc_id}")

    # LEADS
    @staticmethod
    def list_leads(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/leads", params=params)

    @staticmethod
    def update_lead_status(lead_id: str, status: str, notes: Optional[str] = None) -> Dict[str, Any]:
        return api_client.patch(
            f"/api/v1/leads/{lead_id}/status",
            json={"status": status, "notes": notes},
        )

    # CUSTOMERS
    @staticmethod
    def list_customers(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/customers", params=params)


admin_service = AdminService()