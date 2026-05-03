#!/bin/bash
# Deployment helper script

set -e

ENVIRONMENT=${1:-staging}
CLUSTER_NAME="patient-monitoring-${ENVIRONMENT}"
NAMESPACE="patient-monitoring"
REGION="eu-west-1"

echo "🚀 Deploying to ${ENVIRONMENT} environment..."

# Check prerequisites
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm not found. Please install Helm."
    exit 1
fi

# Configure kubectl
echo "📋 Configuring kubectl..."
aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${REGION}

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Deploy with Helm
echo "🎯 Deploying with Helm..."
helm upgrade --install patient-monitoring ./helm/patient-monitoring \
  --namespace ${NAMESPACE} \
  --values ./helm/patient-monitoring/values-${ENVIRONMENT}.yaml \
  --wait \
  --timeout 10m

# Verify deployment
echo "✅ Verifying deployment..."
kubectl rollout status deployment/patient-monitoring-backend -n ${NAMESPACE}

echo "🎉 Deployment completed successfully!"
echo "📊 Access the application at: https://patient-monitoring-${ENVIRONMENT}.example.com"
