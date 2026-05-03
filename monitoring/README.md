"""
Monitoring and Observability README
"""

# Monitoring & Observability Stack

This directory contains configurations for the complete monitoring and observability setup.

## Components

### Prometheus
- **Directory**: `prometheus/`
- **Config**: `prometheus.yml` - Metric scraping configuration
- **Rules**: `alerting-rules.yaml` - Alert definitions
- **Deployment**: StatefulSet with persistent storage
- **Retention**: 15 days of metrics

### Grafana
- **Directory**: `grafana/`
- **Dashboards**: Pre-built patient monitoring dashboards
- **Datasources**: Prometheus integration
- **Alerts**: Grafana alert notifications

### Elasticsearch & Kibana (ELK Stack)
- **Directory**: `elasticsearch/` and `kibana/`
- **Logs**: Centralized application and system logs
- **Indexing**: Daily indices by application and level
- **Retention**: 30 days

### Alert Manager
- Alert routing and grouping
- Slack/PagerDuty/Email notifications
- Alert deduplication and aggregation

## Key Metrics Monitored

### Application Metrics
- HTTP request count and latency
- Error rates by status code
- Database query performance
- Redis cache hit ratios
- WebSocket connection count

### Infrastructure Metrics
- Node CPU, memory, disk usage
- Pod resource utilization
- Container restart counts
- Network I/O
- Disk I/O

### Business Metrics
- Patient records created/updated
- Real-time patient monitors active
- API response times (p50, p95, p99)
- System availability (uptime %)

## Dashboards

### Patient Monitoring Dashboard
- Real-time patient count
- Active monitors
- Latest metrics from connected patients
- System health overview

### Infrastructure Dashboard
- Node utilization
- Pod resource usage
- Network performance
- Storage usage

### Application Performance Dashboard
- Request latency percentiles
- Error rates by endpoint
- Database performance
- Cache hit ratios

## Alerts

See `prometheus/alerting-rules.yaml` for complete alert definitions.

### Critical Alerts
- Backend service down (immediate notification)
- Database unavailable
- Redis cache down
- Disk space critical

### Warning Alerts
- High error rate (>5%)
- High memory usage (>80%)
- High CPU usage (>80%)
- Connection pool nearing limit

## Access URLs

- **Prometheus**: http://prometheus.patient-monitoring.svc.cluster.local:9090
- **Grafana**: http://grafana.patient-monitoring.svc.cluster.local:3000
- **Kibana**: http://kibana.patient-monitoring.svc.cluster.local:5601

## Deployment

Deploy monitoring stack:
```bash
kubectl apply -f monitoring/
```

## Scaling Considerations

- Prometheus retention: Increase `--storage.tsdb.retention.time` for longer history
- Elasticsearch: Scale by adding more nodes for high volume
- Grafana: Horizontal scaling via replicas
