import pytest
import httpx
from app.main import app


@pytest.mark.asyncio
async def test_health_check_endpoint():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data


@pytest.mark.asyncio
async def test_create_research_session_lifecycle():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # 1. Create a session
        payload = {
            "query": "Compare PostgreSQL vs MongoDB for modern AI agent state storage in 2026.",
            "additional_instructions": "Focus on ACID vs document agility.",
            "research_depth": "quick",
        }
        create_resp = await client.post("/api/v1/research", json=payload)
        assert create_resp.status_code == 201
        session_data = create_resp.json()
        session_id = session_data["id"]
        assert session_id is not None
        assert session_data["status"] == "running"
        assert session_data["research_depth"] == "quick"

        # 2. Get session details
        get_resp = await client.get(f"/api/v1/research/{session_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == session_id

        # 3. Get status
        status_resp = await client.get(f"/api/v1/research/{session_id}/status")
        assert status_resp.status_code == 200
        assert "current_node" in status_resp.json()

        # 4. Get sources
        sources_resp = await client.get(f"/api/v1/research/{session_id}/sources")
        assert sources_resp.status_code == 200
        assert "sources" in sources_resp.json()

        # 5. List sessions
        list_resp = await client.get("/api/v1/research?page=1&page_size=10")
        assert list_resp.status_code == 200
        list_data = list_resp.json()
        assert list_data["total"] >= 1
        assert any(item["id"] == session_id for item in list_data["items"])

        # 6. Cancel session
        cancel_resp = await client.post(f"/api/v1/research/{session_id}/cancel")
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_create_session_validation_error():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Query too short (<10 chars)
        payload = {"query": "short"}
        resp = await client.post("/api/v1/research", json=payload)
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_session_not_found():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/research/non_existent_uuid_12345")
        assert resp.status_code == 404
        error_data = resp.json()
        assert "error" in error_data
        assert error_data["error"]["code"] == "SESSION_NOT_FOUND"
