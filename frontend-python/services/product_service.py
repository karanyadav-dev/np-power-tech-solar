"""
NP POWER TECH SOLAR - Product Service
"""

from api.client import api_client
from typing import Dict, Any


class ProductService:
    @staticmethod
    def list(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/products", params=params)

    @staticmethod
    def get(product_id: str) -> Dict[str, Any]:
        return api_client.get(f"/api/v1/products/{product_id}")

    @staticmethod
    def get_by_slug(slug: str) -> Dict[str, Any]:
        return api_client.get(f"/api/v1/products/slug/{slug}")

    @staticmethod
    def list_categories() -> Dict[str, Any]:
        return api_client.get("/api/v1/products/categories")


product_service = ProductService()