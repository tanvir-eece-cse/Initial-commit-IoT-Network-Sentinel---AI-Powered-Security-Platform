# Deployment Guide

This guide covers deploying IoT Network Sentinel to various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Production Checklist](#production-checklist)

---

## Prerequisites

### Required Tools

- Docker 24.0+
- Docker Compose 2.20+
- kubectl 1.28+
- Helm 3.12+ (optional)
- Git

### Hardware Requirements

**Development:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 20GB

**Production (per node):**
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 100GB+ SSD

---

## Local Development

### 1. Clone Repository

```bash
git clone https://github.com/tanvir-eece-cse/iot-network-sentinel.git
cd iot-network-sentinel
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=sentinel
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=iot_sentinel

# Redis
REDIS_PASSWORD=your-redis-password

# JWT
SECRET_KEY=your-jwt-secret-key-minimum-32-characters

# InfluxDB
INFLUXDB_USER=admin
INFLUXDB_PASSWORD=your-influx-password
INFLUXDB_ORG=iot-sentinel
INFLUXDB_BUCKET=network_metrics
INFLUXDB_TOKEN=your-influx-token

# Environment
ENVIRONMENT=development
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Applications

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **ML Service:** http://localhost:8001
- **API Docs:** http://localhost:8000/docs
- **Grafana:** http://localhost:3001

---

## Docker Deployment

### Building Images

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build ml-service
docker-compose build frontend
```

### Pushing to Registry

```bash
# Tag images
docker tag iot-sentinel-backend:latest ghcr.io/tanvir-eece-cse/iot-sentinel-backend:latest
docker tag iot-sentinel-ml:latest ghcr.io/tanvir-eece-cse/iot-sentinel-ml:latest
docker tag iot-sentinel-frontend:latest ghcr.io/tanvir-eece-cse/iot-sentinel-frontend:latest

# Push to registry
docker push ghcr.io/tanvir-eece-cse/iot-sentinel-backend:latest
docker push ghcr.io/tanvir-eece-cse/iot-sentinel-ml:latest
docker push ghcr.io/tanvir-eece-cse/iot-sentinel-frontend:latest
```

### Production Docker Compose

For production, use environment-specific compose files:

```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Kubernetes Deployment

### 1. Cluster Setup

Ensure you have a Kubernetes cluster ready:

```bash
# Verify cluster connection
kubectl cluster-info
kubectl get nodes
```

### 2. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 3. Configure Secrets

**Important:** Update the secrets in `k8s/configmap.yaml` before applying!

```bash
# Create secrets (update values first!)
kubectl apply -f k8s/configmap.yaml
```

For production, use sealed-secrets or external secret management:

```bash
# Using kubectl to create secrets
kubectl create secret generic iot-sentinel-secrets \
  --namespace=iot-sentinel \
  --from-literal=POSTGRES_USER=sentinel \
  --from-literal=POSTGRES_PASSWORD=$(openssl rand -base64 32) \
  --from-literal=POSTGRES_DB=iot_sentinel \
  --from-literal=REDIS_PASSWORD=$(openssl rand -base64 32) \
  --from-literal=SECRET_KEY=$(openssl rand -base64 64) \
  --from-literal=INFLUXDB_TOKEN=$(openssl rand -base64 48)
```

### 4. Deploy Database Layer

```bash
kubectl apply -f k8s/database.yaml

# Wait for databases to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n iot-sentinel --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n iot-sentinel --timeout=300s
```

### 5. Deploy Application Services

```bash
# Deploy backend
kubectl apply -f k8s/backend-deployment.yaml

# Deploy ML service
kubectl apply -f k8s/ml-service-deployment.yaml

# Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml

# Verify deployments
kubectl get pods -n iot-sentinel
kubectl get services -n iot-sentinel
```

### 6. Configure Ingress

Update the hostnames in `k8s/ingress.yaml` to match your domain:

```bash
# Apply ingress
kubectl apply -f k8s/ingress.yaml

# Verify ingress
kubectl get ingress -n iot-sentinel
```

### 7. TLS Configuration

For production, configure cert-manager:

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: tanvir.eece.mist@gmail.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### 8. Monitoring Setup

```bash
# Deploy Prometheus and Grafana
kubectl apply -f monitoring/prometheus.yml

# Or use Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

---

## Production Checklist

### Security

- [ ] Change all default passwords
- [ ] Enable TLS/HTTPS
- [ ] Configure network policies
- [ ] Enable audit logging
- [ ] Set up security scanning in CI/CD
- [ ] Configure rate limiting
- [ ] Enable CORS properly
- [ ] Use secrets management (Vault, AWS Secrets Manager)

### Performance

- [ ] Configure resource requests/limits
- [ ] Enable horizontal pod autoscaling
- [ ] Set up caching properly
- [ ] Configure database connection pooling
- [ ] Enable compression
- [ ] Set up CDN for static assets

### Reliability

- [ ] Configure health checks
- [ ] Set up database backups
- [ ] Configure pod disruption budgets
- [ ] Enable multi-zone deployment
- [ ] Set up disaster recovery

### Monitoring

- [ ] Configure Prometheus metrics
- [ ] Set up Grafana dashboards
- [ ] Configure alerting rules
- [ ] Enable distributed tracing
- [ ] Set up log aggregation

### Compliance

- [ ] Enable audit logging
- [ ] Configure data retention policies
- [ ] Document security controls
- [ ] Regular vulnerability assessments

---

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name> -n iot-sentinel
kubectl logs <pod-name> -n iot-sentinel
```

**Database connection issues:**
```bash
# Check database pod
kubectl exec -it <postgres-pod> -n iot-sentinel -- psql -U sentinel -d iot_sentinel

# Verify connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- nc -zv postgres 5432
```

**Service not accessible:**
```bash
# Check service endpoints
kubectl get endpoints -n iot-sentinel

# Port forward for testing
kubectl port-forward svc/backend 8000:8000 -n iot-sentinel
```

### Support

For issues and support:
- **GitHub Issues:** [Report Issues](https://github.com/tanvir-eece-cse/iot-network-sentinel/issues)
- **Email:** tanvir.eece.mist@gmail.com
- **LinkedIn:** [tanvir-eece](https://www.linkedin.com/in/tanvir-eece/)
