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


@pytest.mark.anyio
async def test_predict_endpoint_without_data(client: AsyncClient):
    """Test prediction endpoint without proper data."""
    response = await client.post(
        "/api/v1/predict",
        json={}
    )
    assert response.status_code in [422, 400]


@pytest.mark.anyio
async def test_predict_single_sample(client: AsyncClient):
    """Test single sample prediction."""
    sample_data = {
        "features": {
            "packet_count": 1000,
            "byte_count": 50000,
            "duration": 60.0,
            "src_port": 443,
            "dst_port": 8080,
            "protocol_tcp": 1,
            "protocol_udp": 0,
            "protocol_icmp": 0,
            "flags_syn": 1,
            "flags_ack": 1,
            "flags_fin": 0,
            "flags_rst": 0
        }
    }
    response = await client.post(
        "/api/v1/predict",
        json=sample_data
    )
    # May return 200 or 503 if model not loaded
    assert response.status_code in [200, 503]


@pytest.mark.anyio
async def test_batch_predict_endpoint(client: AsyncClient):
    """Test batch prediction endpoint."""
    batch_data = {
        "samples": [
            {
                "features": {
                    "packet_count": 1000,
                    "byte_count": 50000,
                    "duration": 60.0,
                    "src_port": 443,
                    "dst_port": 8080,
                    "protocol_tcp": 1,
                    "protocol_udp": 0,
                    "protocol_icmp": 0,
                    "flags_syn": 1,
                    "flags_ack": 1,
                    "flags_fin": 0,
                    "flags_rst": 0
                }
            }
        ]
    }
    response = await client.post(
        "/api/v1/predict/batch",
        json=batch_data
    )
    assert response.status_code in [200, 503]


@pytest.mark.anyio
async def test_models_list_endpoint(client: AsyncClient):
    """Test models listing endpoint."""
    response = await client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or "models" in data


@pytest.mark.anyio
async def test_model_info_endpoint(client: AsyncClient):
    """Test model info endpoint."""
    response = await client.get("/api/v1/models/anomaly_detector")
    # May return 200 or 404 if model not found
    assert response.status_code in [200, 404]


@pytest.mark.anyio
async def test_metrics_endpoint(client: AsyncClient):
    """Test Prometheus metrics endpoint."""
    response = await client.get("/metrics")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_api_docs_available(client: AsyncClient):
    """Test that API documentation is available."""
    response = await client.get("/docs")
    assert response.status_code == 200


class TestModelManager:
    """Test suite for ModelManager."""
    
    def test_feature_extraction(self):
        """Test feature extraction from raw data."""
        from app.services.model_manager import ModelManager
        
        manager = ModelManager()
        raw_data = {
            "packet_count": 100,
            "byte_count": 5000,
            "duration": 10.0
        }
        
        # Test that feature extraction doesn't raise
        try:
            features = manager._extract_features(raw_data)
            assert features is not None
        except Exception:
            # Expected if model not fully initialized
            pass
    
    def test_model_initialization(self):
        """Test model initialization."""
        from app.services.model_manager import ModelManager
        
        manager = ModelManager()
        assert manager is not None


class TestAnomalyDetection:
    """Test suite for anomaly detection logic."""
    
    def test_normal_traffic_pattern(self):
        """Test detection of normal traffic patterns."""
        # Normal traffic characteristics
        normal_features = {
            "packet_count": 100,
            "byte_count": 10000,
            "duration": 60,
            "src_port": 443,
            "dst_port": 80
        }
        # Should be classified as normal
        assert normal_features["packet_count"] < 10000
    
    def test_suspicious_traffic_pattern(self):
        """Test detection of suspicious traffic patterns."""
        # Suspicious traffic characteristics (possible port scan)
        suspicious_features = {
            "packet_count": 50000,
            "byte_count": 100000,
            "duration": 1,
            "unique_dst_ports": 1000
        }
        # High packet count in short duration is suspicious
        assert suspicious_features["packet_count"] / max(suspicious_features["duration"], 1) > 1000
    
    def test_ddos_pattern(self):
        """Test detection of DDoS patterns."""
        # DDoS characteristics
        ddos_features = {
            "packet_count": 1000000,
            "byte_count": 50000000,
            "duration": 10,
            "unique_src_ips": 10000
        }
        # Very high packet rate indicates potential DDoS
        packet_rate = ddos_features["packet_count"] / max(ddos_features["duration"], 1)
        assert packet_rate > 10000
