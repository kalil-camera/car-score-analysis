output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "database_subnet_ids" {
  description = "Database subnet IDs"
  value       = aws_subnet.database[*].id
}

# RDS Outputs
output "rds_cluster_id" {
  description = "RDS Cluster ID"
  value       = aws_rds_cluster.main.id
}

output "rds_cluster_endpoint" {
  description = "RDS Cluster Write Endpoint"
  value       = aws_rds_cluster.main.endpoint
}

output "rds_cluster_reader_endpoint" {
  description = "RDS Cluster Read Endpoint"
  value       = aws_rds_cluster.main.reader_endpoint
}

output "rds_database_name" {
  description = "RDS Database Name"
  value       = var.database_name
}

output "rds_database_username" {
  description = "RDS Database Master Username"
  value       = var.database_username
  sensitive   = true
}

output "rds_port" {
  description = "RDS Port"
  value       = 5432
}

# ALB Outputs
output "alb_dns_name" {
  description = "ALB DNS Name"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ALB ARN"
  value       = aws_lb.main.arn
}

output "alb_zone_id" {
  description = "ALB Zone ID"
  value       = aws_lb.main.zone_id
}

output "alb_target_group_arn" {
  description = "ALB Target Group ARN"
  value       = aws_lb_target_group.main.arn
}

# ECS Outputs
output "ecs_cluster_id" {
  description = "ECS Cluster ID"
  value       = aws_ecs_cluster.main.id
}

output "ecs_cluster_name" {
  description = "ECS Cluster Name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_id" {
  description = "ECS Service ID"
  value       = aws_ecs_service.main.id
}

output "ecs_service_name" {
  description = "ECS Service Name"
  value       = aws_ecs_service.main.name
}

output "ecs_task_definition_arn" {
  description = "ECS Task Definition ARN"
  value       = aws_ecs_task_definition.main.arn
}

output "ecs_task_execution_role_arn" {
  description = "ECS Task Execution Role ARN"
  value       = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_task_role_arn" {
  description = "ECS Task Role ARN"
  value       = aws_iam_role.ecs_task_role.arn
}

# API Gateway Outputs
output "api_gateway_id" {
  description = "API Gateway ID"
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_invoke_url" {
  description = "API Gateway Invoke URL"
  value       = "${aws_api_gateway_stage.main.invoke_url}/app"
}

output "api_gateway_stage_name" {
  description = "API Gateway Stage Name"
  value       = aws_api_gateway_stage.main.stage_name
}

# Security Groups
output "alb_security_group_id" {
  description = "ALB Security Group ID"
  value       = aws_security_group.alb.id
}

output "ecs_security_group_id" {
  description = "ECS Security Group ID"
  value       = aws_security_group.ecs.id
}

output "rds_security_group_id" {
  description = "RDS Security Group ID"
  value       = aws_security_group.rds.id
}

# Connection String
output "rds_connection_string" {
  description = "RDS PostgreSQL Connection String"
  value       = "postgresql://${var.database_username}:PASSWORD@${aws_rds_cluster.main.endpoint}:5432/${var.database_name}"
  sensitive   = true
}

# SQS Outputs
output "sqs_queue_id" {
  description = "SQS Queue ID"
  value       = aws_sqs_queue.main.id
}

output "sqs_queue_arn" {
  description = "SQS Queue ARN"
  value       = aws_sqs_queue.main.arn
}

output "sqs_queue_url" {
  description = "SQS Queue URL"
  value       = aws_sqs_queue.main.url
}

output "sqs_dlq_id" {
  description = "SQS Dead Letter Queue ID"
  value       = aws_sqs_queue.main_dlq.id
}

output "sqs_dlq_arn" {
  description = "SQS Dead Letter Queue ARN"
  value       = aws_sqs_queue.main_dlq.arn
}

output "sqs_dlq_url" {
  description = "SQS Dead Letter Queue URL"
  value       = aws_sqs_queue.main_dlq.url
}

# Useful links and information
output "deployment_info" {
  description = "Deployment Information"
  value = {
    alb_dns               = aws_lb.main.dns_name
    api_gateway_url       = "${aws_api_gateway_stage.main.invoke_url}/app"
    rds_endpoint          = aws_rds_cluster.main.endpoint
    ecs_cluster_name      = aws_ecs_cluster.main.name
    cloudwatch_log_group  = aws_cloudwatch_log_group.ecs.name
    sqs_queue_url         = aws_sqs_queue.main.url
    sqs_dlq_url           = aws_sqs_queue.main_dlq.url
    region                = var.aws_region
  }
}
