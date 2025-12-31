import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    """Test the health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_root_endpoint(client: AsyncClient):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "IoT Network Sentinel" in data["message"]


@pytest.mark.anyio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "invalid@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code in [401, 400]


@pytest.mark.anyio
async def test_protected_endpoint_without_auth(client: AsyncClient):
    """Test accessing protected endpoint without authentication."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_devices_endpoint_without_auth(client: AsyncClient):
    """Test accessing devices endpoint without authentication."""
    response = await client.get("/api/v1/devices")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_anomalies_endpoint_without_auth(client: AsyncClient):
    """Test accessing anomalies endpoint without authentication."""
    response = await client.get("/api/v1/anomalies")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_api_docs_available(client: AsyncClient):
    """Test that API documentation is available."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_openapi_schema(client: AsyncClient):
    """Test that OpenAPI schema is available."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
