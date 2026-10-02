"""
NP POWER TECH SOLAR - Project Service
"""

from api.client import api_client
from typing import Dict, Any, List


class ProjectService:
    @staticmethod
    def list(page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        params = {"page": page, "limit": limit}
        params.update({k: v for k, v in filters.items() if v is not None})
        return api_client.get("/api/v1/projects", params=params)

    @staticmethod
    def get(project_id: str) -> Dict[str, Any]:
        return api_client.get(f"/api/v1/projects/{project_id}")

    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.post("/api/v1/projects", json=data)

    @staticmethod
    def update(project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return api_client.patch(f"/api/v1/projects/{project_id}", json=data)

    @staticmethod
    def delete(project_id: str) -> Dict[str, Any]:
        return api_client.delete(f"/api/v1/projects/{project_id}")


project_service = ProjectService()