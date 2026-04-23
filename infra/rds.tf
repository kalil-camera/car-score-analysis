# Aurora PostgreSQL Cluster
resource "aws_rds_cluster" "main" {
  cluster_identifier      = "${var.project_name}-cluster"
  engine                  = "aurora-postgresql"
  engine_version          = var.database_engine_version
  database_name           = var.database_name
  master_username         = var.database_username
  master_password         = var.database_password
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  backup_retention_period = var.backup_retention_period
  skip_final_snapshot     = false
  final_snapshot_identifier = "${var.project_name}-cluster-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  # Enable backups and automatic minor version upgrades
  enabled_cloudwatch_logs_exports = ["postgresql"]
  storage_encrypted              = true
  enable_http_endpoint           = false

  tags = {
    Name = "${var.project_name}-aurora-cluster"
  }

  depends_on = [aws_db_subnet_group.main]
}}

# Aurora PostgreSQL Instance 1
resource "aws_rds_cluster_instance" "main-1" {
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = var.database_instance_class
  engine              = aws_rds_cluster.main.engine
  engine_version      = aws_rds_cluster.main.engine_version
  identifier         = "${var.project_name}-instance-1"

  performance_insights_enabled    = true
  performance_insights_retention_period = 7
  monitoring_interval             = 60
  monitoring_role_arn            = aws_iam_role.rds_monitoring.arn
  enable_performance_insights     = true

  tags = {
    Name = "${var.project_name}-aurora-instance-1"
  }
}

# Aurora PostgreSQL Instance 2 (for high availability)
resource "aws_rds_cluster_instance" "main-2" {
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = var.database_instance_class
  engine              = aws_rds_cluster.main.engine
  engine_version      = aws_rds_cluster.main.engine_version
  identifier         = "${var.project_name}-instance-2"

  performance_insights_enabled    = true
  performance_insights_retention_period = 7
  monitoring_interval             = 60
  monitoring_role_arn            = aws_iam_role.rds_monitoring.arn
  enable_performance_insights     = true

  tags = {
    Name = "${var.project_name}-aurora-instance-2"
  }

  depends_on = [aws_rds_cluster_instance.main-1]
}

# IAM Role for RDS Monitoring
resource "aws_iam_role" "rds_monitoring" {
  name = "${var.project_name}-rds-monitoring-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-rds-monitoring-role"
  }
}

# Attach policy to RDS monitoring role
resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# RDS Parameter Group for PostgreSQL 16
resource "aws_rds_cluster_parameter_group" "main" {
  family      = "aurora-postgresql16"
  name        = "${var.project_name}-cluster-params"
  description = "Custom parameter group for Aurora PostgreSQL 16"

  # Common PostgreSQL parameters
  parameter {
    name  = "log_statement"
    value = "all"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "0"
  }

  tags = {
    Name = "${var.project_name}-cluster-param-group"
  }
}

# Update cluster to use the parameter group
resource "aws_rds_cluster" "main_with_params" {
  provider = aws

  cluster_identifier = aws_rds_cluster.main.id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.main.name

  depends_on = [aws_rds_cluster.main]

  lifecycle {
    ignore_changes = [
      master_password,
      database_name,
      master_username,
    ]
  }
}
