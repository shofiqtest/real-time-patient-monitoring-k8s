"""
Quick Start Guide for Real-Time Patient Monitoring System
"""

# Real-Time Patient Monitoring System - Quick Start Guide

## 🎯 Project Overview

This is a **production-ready**, **scalable** real-time patient monitoring platform built with:
- **FastAPI** backend
- **PostgreSQL** + **TimescaleDB** for time-series data
- **Redis** for caching and real-time streaming
- **Kubernetes** for orchestration
- **Helm** for package management
- **Terraform** for infrastructure-as-code
- **Prometheus/Grafana** for monitoring
- **GitHub Actions** for CI/CD

## 📦 Project Structure

```
├── backend/                    # FastAPI application
│   ├── app/                   # Application code
│   │   ├── main.py           # Entry point
│   │   ├── api/              # API endpoints (patients, metrics, websocket)
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── database.py       # Database setup
│   │   ├── redis_client.py   # Redis client
│   │   └── config.py         # Configuration
│   ├── Dockerfile            # Multi-stage build
│   └── requirements.txt       # Python dependencies
│
├── kubernetes/               # Kubernetes manifests
│   ├── namespace.yaml       # Namespace & network policies
│   ├── backend-deployment.yaml
│   ├── database-statefulset.yaml
│   ├── redis-deployment.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── ...
│
├── helm/                     # Helm charts
│   └── patient-monitoring/  # Chart package
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── terraform/                # Infrastructure as Code
│   ├── main.tf              # EKS cluster
│   ├── variables.tf
│   ├── security.tf          # Security groups & KMS
│   └── ...
│
├── .github/workflows/        # GitHub Actions CI/CD
│   ├── build-and-test.yml
│   ├── deploy-staging.yml
│   └── deploy-production.yml
│
├── monitoring/               # Observability
│   ├── prometheus/
│   ├── grafana/
│   └── elasticsearch/
│
└── docker-compose.yml        # Local development
```

## 🚀 Getting Started

### Option 1: Local Development (Quickest)

```bash
# Prerequisites: Docker and Docker Compose

# 1. Start services
docker-compose up

# 2. Access the application
# API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

### Option 2: Kubernetes (Local)

```bash
# Prerequisites: Minikube, kubectl, helm

# 1. Start Minikube
minikube start --cpus 4 --memory 8192

# 2. Create namespace
kubectl create namespace patient-monitoring

# 3. Deploy with Helm
helm install patient-monitoring ./helm/patient-monitoring \
  --namespace patient-monitoring \
  --values helm/patient-monitoring/values.yaml

# 4. Access via port-forward
kubectl port-forward svc/patient-monitoring-backend 8000:80 -n patient-monitoring
```

### Option 3: AWS Kubernetes (Production)

```bash
# Prerequisites: AWS CLI, Terraform, kubectl

# 1. Configure variables
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# 2. Deploy infrastructure
terraform init
terraform plan
terraform apply

# 3. Deploy application
chmod +x ../deploy.sh
../deploy.sh production
```

## 📝 Core API Endpoints

### Patients
- `GET /api/patients` - List all patients
- `GET /api/patients/{id}` - Get specific patient
- `POST /api/patients` - Create patient
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

### Health & Monitoring
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Swagger documentation

### Real-Time
- `WS /ws/patient/{patient_id}` - WebSocket for real-time monitoring

## 🔧 Development

### Running Tests
```bash
cd backend
pytest tests/ -v
```

### Running Backend Locally
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Code Style
```bash
# Format
black backend/

# Lint
flake8 backend/

# Type check
mypy backend/
```

## 🐳 Building Docker Image

```bash
cd backend
docker build -t patient-monitoring-backend:latest .
docker run -p 8000:8000 patient-monitoring-backend:latest
```

## 📊 Monitoring & Observability

### Prometheus Metrics
- Application: HTTP requests, errors, latency
- Infrastructure: Node, pod, container metrics
- Business: Patient operations, active connections

### Grafana Dashboards
- Patient Monitoring Dashboard
- Infrastructure Dashboard
- Application Performance Dashboard

### Alerts
- Backend service down → Critical
- High error rate (>5%) → Warning
- Memory/CPU high (>80%) → Warning
- Database issues → Critical

## 🚀 CI/CD Pipeline

### Automatic Triggers
1. **Push to develop** → Build & test → Deploy to staging
2. **Push to main** → Build & test → Deploy to production
3. **Pull requests** → Run tests & security scans

### Manual Deployment
```bash
./deploy.sh staging    # Deploy to staging
./deploy.sh production # Deploy to production
```

## 🔐 Security Best Practices

- ✅ RBAC for Kubernetes access
- ✅ Network policies
- ✅ Secret management (sealed-secrets)
- ✅ TLS/SSL for external communications
- ✅ Container image scanning
- ✅ Pod security policies
- ✅ Non-root containers

## 📈 Scalability

- Horizontal scaling: Kubernetes HPA (3-10 replicas)
- Database scaling: Read replicas, TimescaleDB compression
- Caching: Redis for hot data
- CDN: For static content

## 🛠️ Common Tasks

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Scale Application
```bash
kubectl scale deployment patient-monitoring-backend -n patient-monitoring --replicas=5
```

### View Logs
```bash
kubectl logs -f deployment/patient-monitoring-backend -n patient-monitoring
```

### Execute Database Commands
```bash
kubectl exec -it patient-monitoring-db-0 -n patient-monitoring -- \
  psql -U postgres -d patient_monitoring
```

### Update Configuration
```bash
kubectl edit configmap patient-monitoring-config -n patient-monitoring
```

## 📚 Documentation

- README.md - Comprehensive system documentation
- CONTRIBUTING.md - Contribution guidelines
- LICENSE - MIT License

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check logs
kubectl logs deployment/patient-monitoring-backend -n patient-monitoring

# Check events
kubectl describe pod <pod-name> -n patient-monitoring
```

### Database connection issues
```bash
# Test database connectivity
kubectl exec -it <backend-pod> -n patient-monitoring -- \
  python -c "import psycopg2; psycopg2.connect('...')"
```

### Memory/CPU issues
```bash
# Check resource usage
kubectl top pods -n patient-monitoring
kubectl top nodes
```

## 📞 Support

- GitHub Issues: Report bugs and feature requests
- Discussions: Ask questions and share ideas
- Security: Email security@patient-monitoring.example.com for security issues

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Ready to deploy?** Start with `docker-compose up` for local testing, then scale to production with Kubernetes! 🚀
