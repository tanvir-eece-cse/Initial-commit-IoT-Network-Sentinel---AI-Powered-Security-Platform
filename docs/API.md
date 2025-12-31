# API Documentation

## Overview

IoT Network Sentinel provides a RESTful API for managing IoT devices, monitoring network traffic, and detecting anomalies using machine learning.

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** JWT Bearer Token

---

## Authentication

### Login

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Register

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

---

## Devices

### List Devices

```http
GET /devices
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Max items to return (default: 100)
- `status` (string): Filter by status (online/offline/unknown)
- `device_type` (string): Filter by device type

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Smart Thermostat",
      "device_type": "thermostat",
      "ip_address": "192.168.1.100",
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "status": "online",
      "firmware_version": "2.1.0",
      "last_seen": "2024-01-15T10:30:00Z",
      "risk_score": 0.15,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "pages": 5
}
```

### Get Device

```http
GET /devices/{device_id}
Authorization: Bearer <token>
```

### Create Device

```http
POST /devices
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Smart Camera",
  "device_type": "camera",
  "ip_address": "192.168.1.101",
  "mac_address": "11:22:33:44:55:66",
  "firmware_version": "1.0.0"
}
```

### Update Device

```http
PUT /devices/{device_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Smart Camera - Living Room",
  "firmware_version": "1.1.0"
}
```

### Delete Device

```http
DELETE /devices/{device_id}
Authorization: Bearer <token>
```

---

## Anomalies

### List Anomalies

```http
GET /anomalies
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Max items to return
- `severity` (string): Filter by severity (critical/high/medium/low)
- `status` (string): Filter by status (new/investigating/resolved/false_positive)
- `device_id` (uuid): Filter by device

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "device_id": "uuid",
      "anomaly_type": "port_scan",
      "severity": "high",
      "confidence": 0.92,
      "description": "Unusual port scanning activity detected",
      "source_ip": "192.168.1.100",
      "destination_ip": "192.168.1.1",
      "status": "new",
      "detected_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "pages": 3
}
```

### Get Anomaly Details

```http
GET /anomalies/{anomaly_id}
Authorization: Bearer <token>
```

### Update Anomaly Status

```http
PATCH /anomalies/{anomaly_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "investigating",
  "notes": "Investigating potential false positive"
}
```

---

## Network Traffic

### Get Traffic Statistics

```http
GET /network/stats
Authorization: Bearer <token>
```

**Query Parameters:**
- `time_range` (string): 1h, 6h, 24h, 7d, 30d (default: 24h)

**Response:**
```json
{
  "total_packets": 1500000,
  "total_bytes": 2500000000,
  "protocols": {
    "TCP": 1200000,
    "UDP": 250000,
    "ICMP": 50000
  },
  "top_talkers": [
    {
      "ip": "192.168.1.100",
      "bytes_sent": 500000000,
      "bytes_received": 300000000
    }
  ],
  "traffic_by_hour": [
    {
      "hour": "2024-01-15T10:00:00Z",
      "bytes": 100000000
    }
  ]
}
```

### Get Real-time Traffic

```http
GET /network/realtime
Authorization: Bearer <token>
```

WebSocket connection for real-time traffic data.

---

## ML Predictions

### Predict Anomaly

```http
POST /ml/predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "features": {
    "packet_count": 1500,
    "byte_count": 2500000,
    "duration": 60,
    "protocol": "TCP",
    "src_port": 443,
    "dst_port": 8080,
    "flags": "SYN,ACK"
  }
}
```

**Response:**
```json
{
  "prediction": "anomaly",
  "confidence": 0.87,
  "anomaly_type": "ddos_attack",
  "risk_score": 0.92,
  "recommended_action": "Block traffic and investigate"
}
```

### Batch Prediction

```http
POST /ml/predict/batch
Authorization: Bearer <token>
Content-Type: application/json

{
  "samples": [
    { "features": {...} },
    { "features": {...} }
  ]
}
```

---

## Dashboard

### Get Dashboard Stats

```http
GET /dashboard/stats
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_devices": 150,
  "online_devices": 142,
  "offline_devices": 8,
  "total_anomalies_today": 23,
  "critical_anomalies": 2,
  "high_anomalies": 5,
  "medium_anomalies": 10,
  "low_anomalies": 6,
  "network_health_score": 0.85,
  "total_traffic_today": "2.5 TB"
}
```

---

## Error Responses

All endpoints return errors in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

---

## Rate Limiting

API requests are rate-limited to:
- **Authenticated users:** 1000 requests per hour
- **Unauthenticated users:** 100 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705312800
```

---

## WebSocket Endpoints

### Real-time Anomaly Alerts

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/anomalies');
ws.onmessage = (event) => {
  const anomaly = JSON.parse(event.data);
  console.log('New anomaly:', anomaly);
};
```

### Real-time Network Metrics

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/network');
ws.onmessage = (event) => {
  const metrics = JSON.parse(event.data);
  console.log('Network metrics:', metrics);
};
```
