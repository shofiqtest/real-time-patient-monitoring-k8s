"""
Terraform configuration for Real-Time Patient Monitoring System
Main infrastructure setup
"""

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  backend "s3" {
    bucket         = "patient-monitoring-terraform"
    key            = "prod/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = "PatientMonitoring"
      ManagedBy   = "Terraform"
    }
  }
}

# Local variables
locals {
  cluster_name = "patient-monitoring-${var.environment}"
  tags = {
    Environment = var.environment
    Project     = "PatientMonitoring"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = local.cluster_name
  cluster_version = var.kubernetes_version

  cluster_endpoint_public_access       = true
  cluster_endpoint_private_access      = true
  cluster_endpoint_public_access_cidrs  = var.cluster_endpoint_cidrs

  vpc_id     = module.vpc.vpc_id
  subnet_ids = concat(module.vpc.private_subnets, module.vpc.public_subnets)

  # EKS Addons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    ebs-csi-driver = {
      most_recent = true
    }
  }

  # EKS Managed Node Group
  eks_managed_node_groups = {
    patient_monitoring = {
      name         = "patient-monitoring-ng"
      min_size     = var.node_group_min_size
      max_size     = var.node_group_max_size
      desired_size = var.node_group_desired_size

      instance_types = var.node_instance_types
      disk_size      = 50

      labels = {
        Environment = var.environment
        Workload    = "application"
      }

      tags = local.tags
    }
  }

  manage_aws_auth_configmap = true
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${local.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = data.aws_availability_zones.available.names
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = false
  enable_vpn_gateway = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }

  tags = local.tags
}

# RDS PostgreSQL
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${local.cluster_name}-postgres"

  engine               = "postgres"
  engine_version       = var.postgres_version
  family               = "postgres${split(".", var.postgres_version)[0]}"
  major_engine_version = split(".", var.postgres_version)[0]
  instance_class       = var.rds_instance_class

  allocated_storage     = var.rds_allocated_storage
  max_allocated_storage = var.rds_max_allocated_storage

  db_name  = "patient_monitoring"
  username = var.rds_username
  password = var.rds_password
  port     = 5432

  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql"]

  multi_az            = true
  storage_encrypted   = true
  kms_key_id          = aws_kms_key.rds.arn

  publicly_accessible = false
  skip_final_snapshot = false
  final_snapshot_identifier = "${local.cluster_name}-snapshot"

  tags = local.tags
}

# ElastiCache Redis
module "redis" {
  source  = "terraform-aws-modules/elasticache/aws"
  version = "~> 1.0"

  cluster_id      = "${local.cluster_name}-redis"
  engine          = "redis"
  engine_version  = var.redis_version
  node_type       = var.redis_node_type
  num_cache_nodes = var.redis_num_nodes
  parameter_group_family = "redis${split(".", var.redis_version)[0]}"

  port                    = 6379
  subnet_group_name       = module.vpc.elasticache_subnet_group_name
  security_group_ids      = [aws_security_group.redis.id]
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  automatic_failover_enabled = true

  tags = local.tags
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Output for kubeconfig
output "cluster_id" {
  value = module.eks.cluster_id
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  value = module.rds.db_instance_endpoint
}

output "redis_endpoint" {
  value = module.redis.redis_endpoint_address
}
