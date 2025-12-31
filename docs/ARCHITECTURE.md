# Architecture Documentation

## System Overview

IoT Network Sentinel is a microservices-based platform designed for real-time IoT network security monitoring and anomaly detection. The system combines traditional security practices with machine learning to provide intelligent threat detection.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              LOAD BALANCER                               │
│                            (Nginx Ingress)                               │
└─────────────────────────────────────────────────────────────────────────┘
                    │                                  │
                    ▼                                  ▼
┌─────────────────────────────┐       ┌─────────────────────────────────┐
│        FRONTEND             │       │         BACKEND API             │
│   React + TypeScript        │       │          FastAPI                │
│   - Dashboard               │       │   - Authentication              │
│   - Device Management       │       │   - Device Management           │
│   - Anomaly Viewer          │       │   - Anomaly Detection           │
│   - Network Monitor         │◀─────▶│   - Network Analytics           │
│   - Alert System            │       │   - ML Integration              │
│   - Settings                │       │   - WebSocket Support           │
└─────────────────────────────┘       └─────────────────────────────────┘
                                                      │
                                                      │
                    ┌─────────────────────────────────┼─────────────────┐
                    │                                 │                 │
                    ▼                                 ▼                 ▼
┌─────────────────────────┐  ┌─────────────────────────┐  ┌────────────────┐
│      ML SERVICE         │  │      POSTGRESQL         │  │     REDIS      │
│   FastAPI + Sklearn     │  │   - User Data           │  │  - Caching     │
│   - Isolation Forest    │  │   - Devices             │  │  - Sessions    │
│   - Random Forest       │  │   - Anomalies           │  │  - Rate Limit  │
│   - Model Management    │  │   - Network Events      │  │  - Pub/Sub     │
│   - Batch Processing    │  │   - Audit Logs          │  │                │
└─────────────────────────┘  └─────────────────────────┘  └────────────────┘
                                        │
                                        ▼
                            ┌─────────────────────────┐
                            │       INFLUXDB          │
                            │   - Time Series Data    │
                            │   - Network Metrics     │
                            │   - Traffic Analytics   │
                            └─────────────────────────┘
```

## Component Details

### Frontend (React + TypeScript)

**Technology Stack:**
- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Zustand for state management
- React Query for server state
- Recharts for visualizations
- Framer Motion for animations

**Key Features:**
- Real-time dashboard with network overview
- Device inventory management
- Anomaly detection visualization
- Alert management system
- Network traffic monitoring
- User settings and preferences

**Directory Structure:**
```
frontend/
├── src/
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API service layer
│   ├── store/         # State management
│   ├── types/         # TypeScript type definitions
│   └── __tests__/     # Test files
```

### Backend API (FastAPI)

**Technology Stack:**
- Python 3.11+
- FastAPI framework
- SQLAlchemy ORM
- Pydantic for validation
- JWT for authentication
- WebSocket support

**Key Features:**
- RESTful API design
- JWT-based authentication
- Role-based access control
- Rate limiting
- Request validation
- Comprehensive logging
- Health checks

**API Structure:**
```
/api/v1/
├── /auth           # Authentication endpoints
├── /users          # User management
├── /devices        # Device CRUD operations
├── /anomalies      # Anomaly management
├── /network        # Network analytics
├── /ml             # ML predictions
└── /dashboard      # Dashboard statistics
```

### ML Service

**Technology Stack:**
- Python 3.11+
- FastAPI framework
- scikit-learn
- TensorFlow/Keras
- NumPy/Pandas

**Machine Learning Models:**

1. **Isolation Forest** (Anomaly Detection)
   - Unsupervised learning for detecting outliers
   - Effective for high-dimensional data
   - Low false positive rate

2. **Random Forest** (Classification)
   - Attack type classification
   - Feature importance analysis
   - Multi-class prediction

**Model Pipeline:**
```
Raw Network Data → Feature Extraction → Normalization → 
Model Inference → Post-processing → Alert Generation
```

### Database Layer

**PostgreSQL (Primary Database):**
- User accounts and authentication
- Device inventory
- Anomaly records
- Audit logs
- Configuration data

**Redis (Cache & Session Store):**
- Session management
- API response caching
- Rate limiting counters
- Real-time pub/sub messaging

**InfluxDB (Time Series Database):**
- Network traffic metrics
- Performance monitoring
- Historical trend analysis

## Security Architecture

### Authentication Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│  Login   │───▶│  Verify  │───▶│  Issue   │
│          │    │ Request  │    │ Creds    │    │  JWT     │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
                                                      ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Access  │◀───│  Verify  │◀───│  API     │◀───│  Store   │
│ Resource │    │  Token   │    │ Request  │    │  Token   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Security Layers

1. **Network Security**
   - TLS/HTTPS encryption
   - Network policies in Kubernetes
   - Ingress rate limiting

2. **Application Security**
   - JWT token authentication
   - RBAC authorization
   - Input validation
   - SQL injection prevention
   - XSS protection

3. **Infrastructure Security**
   - Non-root containers
   - Read-only file systems
   - Resource limits
   - Security contexts

## Deployment Architecture

### Kubernetes Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    NAMESPACE: iot-sentinel              │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │
│  │  │   Backend   │  │ ML Service  │  │  Frontend   │    │ │
│  │  │  Replicas:3 │  │ Replicas:2  │  │ Replicas:2  │    │ │
│  │  │   HPA: 2-10 │  │  HPA: 2-5   │  │             │    │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │
│  │  │ PostgreSQL  │  │    Redis    │  │  InfluxDB   │    │ │
│  │  │  Replicas:1 │  │ Replicas:1  │  │ Replicas:1  │    │ │
│  │  │  PVC: 10Gi  │  │             │  │  PVC: 20Gi  │    │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │ │
│  │                                                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 INGRESS CONTROLLER                    │   │
│  │              (TLS Termination, Routing)               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### CI/CD Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Push   │───▶│   Test   │───▶│  Build   │───▶│   Scan   │
│  Code    │    │  Suite   │    │  Images  │    │ Security │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
                                                      ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Prod   │◀───│  Approve │◀───│  Staging │◀───│   Push   │
│  Deploy  │    │  Manual  │    │  Deploy  │    │ Registry │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## Data Flow

### Anomaly Detection Flow

```
1. Network traffic captured by IoT devices
2. Traffic data sent to Backend API
3. Data preprocessed and normalized
4. Features extracted and sent to ML Service
5. ML models predict anomaly probability
6. Results stored in PostgreSQL
7. Real-time alerts via WebSocket
8. Dashboard updated with new anomalies
```

### Monitoring Stack

```
┌─────────────────────────────────────────────────────────┐
│                    MONITORING STACK                      │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                 │
│  │  Prometheus  │─────▶│   Grafana    │                 │
│  │  (Metrics)   │      │ (Dashboards) │                 │
│  └──────────────┘      └──────────────┘                 │
│         ▲                                                │
│         │                                                │
│  ┌──────┴───────┬──────────────┬──────────────┐        │
│  │              │              │              │        │
│  ▼              ▼              ▼              ▼        │
│ Backend     ML Service     PostgreSQL      Redis       │
│ /metrics    /metrics       Exporter      Exporter     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Scalability Considerations

1. **Horizontal Scaling**
   - Stateless services (Backend, ML Service, Frontend)
   - Horizontal Pod Autoscaler based on CPU/Memory
   - Load balancing across replicas

2. **Database Scaling**
   - Read replicas for PostgreSQL
   - Redis clustering for caching
   - InfluxDB retention policies

3. **Performance Optimization**
   - Response caching with Redis
   - Database query optimization
   - Batch processing for ML predictions
   - CDN for static assets

## Future Enhancements

1. **Deep Learning Models**
   - LSTM for time-series analysis
   - Autoencoder for anomaly detection
   - Transformer models for pattern recognition

2. **Edge Computing**
   - Lightweight models on edge devices
   - Federated learning support
   - Real-time processing at the edge

3. **Advanced Features**
   - Threat intelligence integration
   - Automated incident response
   - Compliance reporting
   - Multi-tenant support
