# Real-Time Patient Monitoring System on Kubernetes

A production-grade, scalable real-time patient monitoring platform deployed on Kubernetes with comprehensive observability, automated CI/CD pipelines, and infrastructure-as-code.

## 🏗️ Architecture Overview

### System Components

- **Backend API**: FastAPI-based REST API for patient data ingestion and queries
- **Real-Time Monitoring Service**: WebSocket service for real-time patient metrics streaming
- **Database**: PostgreSQL for persistent patient records and PostgreSQL TimescaleDB for time-series metrics
- **Message Queue**: Redis for real-time data streaming and caching
- **Kubernetes**: Multi-node cluster with automatic scaling and self-healing
- **Observability Stack**: Prometheus, Grafana, ELK Stack for monitoring and logging
- **Service Mesh**: Istio for advanced traffic management (optional)

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  FastAPI     │  │  Real-Time   │  │  TimeSeries  │      │
│  │  Backend     │  │  Monitor     │  │  DB          │      │
│  │  (Replicas)  │  │  (Replicas)  │  │  (Replicas)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                  │               │
│         └─────────────────┼──────────────────┘               │
│                           ▼                                  │
│                    ┌─────────────┐                           │
│                    │   Redis     │ (Caching)                │
│                    │  (Replicas) │                           │
│                    └─────────────┘                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Observability Stack                          │   │
│  │  Prometheus ─► Grafana ─► ELK Stack                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         │                        │                │
         ▼                        ▼                ▼
    Ingress         External DB Access      CI/CD Pipeline
```

## 🚀 Quick Start

### Prerequisites

- Kubernetes 1.21+
- Helm 3.x
- Docker 20.x
- Terraform (for infrastructure)
- Python 3.9+

### Local Development

```bash
# Clone the repository
git clone <repo-url>
cd real-time-patient-monitoring

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run backend locally
cd backend
python -m uvicorn app.main:app --reload
```

### Deploy to Kubernetes

```bash
# Using Helm (Recommended)
helm install patient-monitoring ./helm/patient-monitoring \
  --namespace patient-monitoring \
  --create-namespace

# Or using kubectl directly
kubectl apply -f kubernetes/
```

## 📦 Project Structure

```
.
├── backend/                      # FastAPI application
│   ├── app/
│   │   ├── main.py              # Application entry point
│   │   ├── api/                 # API endpoints
│   │   │   ├── patients.py      # Patient endpoints
│   │   │   ├── metrics.py       # Metrics endpoints
│   │   │   └── websocket.py     # WebSocket handlers
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── config.py            # Configuration
│   ├── tests/                   # Unit tests
│   ├── Dockerfile               # Application container
│   ├── requirements.txt          # Python dependencies
│   └── .dockerignore            # Docker ignore file
│
├── kubernetes/                   # Kubernetes manifests
│   ├── backend-deployment.yaml  # Backend deployment
│   ├── monitoring-deployment.yaml
│   ├── database-statefulset.yaml
│   ├── redis-deployment.yaml
│   ├── services.yaml            # Services
│   ├── ingress.yaml             # Ingress configuration
│   ├── configmap.yaml           # Configuration
│   ├── secrets.yaml             # Secrets (base64)
│   ├── hpa.yaml                 # Horizontal Pod Autoscaler
│   ├── pvc.yaml                 # Persistent Volume Claims
│   └── namespace.yaml           # Namespace setup
│
├── helm/                         # Helm charts
│   └── patient-monitoring/
│       ├── Chart.yaml           # Chart metadata
│       ├── values.yaml          # Default values
│       ├── templates/           # Chart templates
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   ├── ingress.yaml
│       │   ├── configmap.yaml
│       │   └── hpa.yaml
│       └── README.md
│
├── terraform/                    # Infrastructure as Code
│   ├── main.tf                  # Main configuration
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Outputs
│   ├── kubernetes.tf            # Kubernetes provider
│   ├── rds.tf                   # Database configuration
│   ├── redis.tf                 # Redis configuration
│   └── terraform.tfvars         # Variables (sensitive)
│
├── .github/workflows/           # GitHub Actions CI/CD
│   ├── build-and-test.yml
│   ├── deploy-staging.yml
│   ├── deploy-production.yml
│   └── security-scan.yml
│
├── monitoring/                   # Observability
│   ├── prometheus/
│   │   └── prometheus.yml       # Prometheus config
│   ├── grafana/
│   │   ├── dashboards/          # Dashboard definitions
│   │   └── datasources.yaml
│   ├── elasticsearch/           # ELK configuration
│   ├── kibana/
│   └── alerting-rules.yaml
│
├── docker-compose.yml           # Local development
├── .dockerignore
├── .gitignore
├── LICENSE
└── CONTRIBUTING.md
```

## 🔧 Core Features

### Backend API

- **FastAPI** with async support for high throughput
- **RESTful endpoints** for patient CRUD operations
- **WebSocket support** for real-time metrics streaming
- **Database models** using SQLAlchemy ORM
- **Request validation** with Pydantic
- **JWT authentication** and RBAC
- **Comprehensive logging** and error handling

### Kubernetes Deployment

- **Horizontal Pod Autoscaling** based on CPU/memory metrics
- **Health checks** (liveness and readiness probes)
- **Resource limits** and requests for predictable scheduling
- **Multi-zone deployment** for high availability
- **Persistent storage** for databases
- **Network policies** for security

### Observability

- **Prometheus** metrics collection
- **Grafana** dashboards for visualization
- **ELK Stack** for centralized logging
- **Distributed tracing** with Jaeger (optional)
- **Custom alerting** for SLA violations

### CI/CD Pipeline

- **GitHub Actions** for automation
- **Automated testing** on every commit
- **Security scanning** (SAST/DAST)
- **Docker image building** and push to registry
- **Automated deployment** to staging/production
- **Helm chart updates** and validation

## 📊 Database Schema

### Patients Table
```sql
patients (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  age INT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

### Patient Metrics Table (TimescaleDB)
```sql
patient_metrics (
  time TIMESTAMP NOT NULL,
  patient_id UUID NOT NULL,
  heart_rate INT,
  blood_pressure_systolic INT,
  blood_pressure_diastolic INT,
  temperature FLOAT,
  oxygen_saturation FLOAT,
  created_at TIMESTAMP
)
```

## 🔐 Security

- **RBAC** for Kubernetes access
- **Network policies** to restrict pod-to-pod traffic
- **Secret management** with sealed-secrets or HashiCorp Vault
- **Container image scanning** for vulnerabilities
- **Pod security policies** for runtime constraints
- **TLS/SSL** for all external communications
- **Regular security audits** and compliance checks

## 📈 Scalability

- **Horizontal scaling** via Kubernetes HPA
- **Database replication** for read scaling
- **Redis caching** to reduce database load
- **CDN integration** for static content
- **Load balancing** with NGINX Ingress

## 🚦 Deployment Workflow

1. **Development** → Commit to feature branch
2. **CI Pipeline** → Run tests, security scans, build Docker image
3. **Staging** → Auto-deploy to staging environment
4. **Manual Testing** → QA validation
5. **Production** → Approved merge to main triggers production deployment
6. **Monitoring** → Grafana dashboards track performance

## 📚 API Documentation

Once deployed, access Swagger UI at:
```
http://<ingress-host>/docs
```

## 🛠️ Configuration

### Environment Variables

Create `.env` file:
```bash
DATABASE_URL=postgresql://user:pass@postgres:5432/patient_db
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
JWT_SECRET=your-secret-key
```

### Kubernetes ConfigMap

Update `kubernetes/configmap.yaml` for cluster-specific settings.

## 📝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👨‍💼 Author

Md Shofiqul Islam - DevOps & Platform Engineering

## 🤝 Support

For issues and questions, please open an issue on GitHub.

---

**Last Updated**: May 3, 2026  
**Version**: 1.0.0
