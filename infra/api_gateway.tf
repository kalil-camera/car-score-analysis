# API Gateway REST API
resource "aws_api_gateway_rest_api" "main" {
  name        = "${var.project_name}-api"
  description = "API Gateway for ${var.project_name}"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "${var.project_name}-api"
  }
}

# API Gateway Resource
resource "aws_api_gateway_resource" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "app"
}

# API Gateway Proxy Resource
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.main.id
  path_part   = "{proxy+}"
}

# API Gateway Method for proxy
resource "aws_api_gateway_method" "proxy" {
  rest_api_id      = aws_api_gateway_rest_api.main.id
  resource_id      = aws_api_gateway_resource.proxy.id
  http_method      = "ANY"
  authorization    = "NONE"
  request_parameters = {
    "method.request.path.proxy" = true
  }
}

# API Gateway Integration - ALB
resource "aws_api_gateway_integration" "proxy" {
  rest_api_id      = aws_api_gateway_rest_api.main.id
  resource_id      = aws_api_gateway_resource.proxy.id
  http_method      = aws_api_gateway_method.proxy.http_method
  type             = "HTTP_PROXY"
  uri              = "http://${aws_lb.main.dns_name}/{proxy}"
  integration_http_method = "ANY"

  request_parameters = {
    "integration.request.path.proxy" = "method.request.path.proxy"
  }
}

# Root proxy resource
resource "aws_api_gateway_method" "root_proxy" {
  rest_api_id      = aws_api_gateway_rest_api.main.id
  resource_id      = aws_api_gateway_resource.main.id
  http_method      = "ANY"
  authorization    = "NONE"
}

resource "aws_api_gateway_integration" "root_proxy" {
  rest_api_id      = aws_api_gateway_rest_api.main.id
  resource_id      = aws_api_gateway_resource.main.id
  http_method      = aws_api_gateway_method.root_proxy.http_method
  type             = "HTTP_PROXY"
  uri              = "http://${aws_lb.main.dns_name}/"
  integration_http_method = "ANY"
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "main" {
  depends_on = [
    aws_api_gateway_integration.proxy,
    aws_api_gateway_integration.root_proxy
  ]

  rest_api_id = aws_api_gateway_rest_api.main.id
}

# API Gateway Stage
resource "aws_api_gateway_stage" "main" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = var.api_gateway_stage

  xray_tracing_enabled = true

  access_log_settings {
    cloudwatch_log_group_arn = "${aws_cloudwatch_log_group.api_gateway.arn}:*"
    format                   = "$context.requestId $context.extendedRequestId $context.identity.sourceIp $context.requestTime $context.httpMethod $context.resourcePath $context.protocol $context.status $context.responseLength"
  }

  depends_on = [aws_api_gateway_account.main]

  tags = {
    Name = "${var.project_name}-${var.api_gateway_stage}-stage"
  }
}

# CloudWatch Log Group for API Gateway
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/${var.project_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-api-gateway-logs"
  }
}

# API Gateway Account (for CloudWatch logging)
resource "aws_api_gateway_account" "main" {
  cloudwatch_role_arn = aws_iam_role.api_gateway_cloudwatch.arn
}

# IAM Role for API Gateway CloudWatch Logs
resource "aws_iam_role" "api_gateway_cloudwatch" {
  name = "${var.project_name}-api-gateway-cloudwatch-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-api-gateway-cloudwatch-role"
  }
}

# IAM Policy for API Gateway CloudWatch Logs
resource "aws_iam_role_policy" "api_gateway_cloudwatch" {
  name = "${var.project_name}-api-gateway-cloudwatch-policy"
  role = aws_iam_role.api_gateway_cloudwatch.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Stage settings with logging
resource "aws_api_gateway_method_settings" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = aws_api_gateway_stage.main.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled        = true
    data_trace_enabled     = true
    logging_level          = "INFO"
  }
}

# Usage Plan for rate limiting
resource "aws_api_gateway_usage_plan" "main" {
  name       = "${var.project_name}-usage-plan"
  depends_on = [aws_api_gateway_stage.main]

  api_stages {
    api_id      = aws_api_gateway_rest_api.main.id
    stage       = var.api_gateway_stage
  }

  throttle_settings {
    burst_limit = 5000
    rate_limit  = 2000
  }

  quota_settings {
    limit  = 100000
    period = "DAY"
  }
}
