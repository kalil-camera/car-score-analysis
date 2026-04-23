# Car Score

Aggregates, processes, and disseminates data regarding vehicle price history, reliability index, and safety ratings. 

Backend: Python with Fast API
SQL Database.
Infra is AWS with Terraform.

### Infrastructure Components

- **VPC**: Custom VPC with public, private, and database subnets
- **Aurora PostgreSQL 16**: Multi-AZ database cluster
- **Application Load Balancer**: Distributes traffic to ECS tasks
- **ECS Fargate**: Container orchestration for Python applications
- **API Gateway**: RESTful API interface with rate limiting
- **SQS**: Simple Queue Service for async message processing
- **Auto Scaling**: Scales based on CPU/Memory utilization
- **CloudWatch**: Comprehensive logging and monitoring

### CI/CD Pipeline

- **Python Linting**: Black, Flake8, Pylint, isort
- **Automated Tests**: Pytest with coverage reporting
- **Terraform Validation**: tfsec and terraform validate
- **Security Scanning**: Trivy vulnerability scanner
- **PR Comments**: Terraform plan comments on PRs

##Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI pipeline
├── app/                            # Python application code
├── infra/                          # Terraform infrastructure
│   ├── main.tf                     # VPC, subnets, security groups
│   ├── rds.tf                      # Aurora PostgreSQL
│   ├── alb.tf                      # Application Load Balancer
│   ├── ecs.tf                      # ECS clusters and services
│   ├── sqs.tf                      # SQS queues
│   ├── api_gateway.tf              # API Gateway
│   ├── outputs.tf                  # Terraform outputs
│   ├── providers.tf                # Provider configuration
│   ├── variables.tf                # Input variables
│   ├── terraform.tfvars            # Configuration values
│   └── README.md                   # Infrastructure documentation
├── tests/                          # Test suite
│   ├── conftest.py                 # Pytest configuration
│   ├── test_example.py             # Example tests
│   └── __init__.py
├── .bandit                         # Bandit security config
├── .editorconfig                   # Editor configuration
├── .flake8                         # Flake8 configuration
├── .gitignore                      # Git ignore rules
├── .pre-commit-config.yaml         # Pre-commit hooks
├── .prettierignore                 # Prettier ignore rules
├── CI.md                           # CI/CD documentation
├── pyproject.toml                  # Python project config
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
├── requirements-test.txt           # Test dependencies
└── README.md                       # This file
```

##  Run on local machine

### Prerequisites

- Python 3.11+
- Terraform >= 1.0
- AWS Account with appropriate permissions
- Docker (for local testing)

### Local Development Setup

1. **Clone and setup Python environment**

```bash
git clone <repository>
cd pythonbackend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt -r requirements-test.txt
```

2. **Setup pre-commit hooks**

```bash
pip install pre-commit
pre-commit install
```

3. **Run tests locally**

```bash
pytest
pytest --cov=app --cov-report=html  # With coverage
```

4. **Run linting**

```bash
black .
isort .
flake8 .
pylint app/
```

### Infrastructure Deployment

1. **Initialize Terraform**

```bash
cd infra
terraform init
```

2. **Review deployment**

```bash
terraform plan
```

3. **Deploy infrastructure**

```bash
terraform apply
```

4. **Get outputs**

```bash
terraform output deployment_info
```

##  GitHub Actions CI Pipeline

The pipeline automatically runs on:

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via workflow dispatch

### Pipeline Jobs

1. **Python Linting** (python-lint)
   - Black format checking
   - isort import sorting
   - Flake8 linting
   - Pylint analysis
   - Python 3.11 & 3.12

2. **Python Tests** (python-tests)
   - Pytest execution
   - Coverage reporting
   - PostgreSQL 16 service
   - Codecov upload

3. **Terraform Validation** (terraform-validate)
   - Format checking
   - terraform validate
   - tfsec security scan

4. **Terraform Plan** (terraform-plan)
   - Generates plan on PRs
   - Posts plan in PR comments
   - Archives plan file

5. **Security Scanning** (security-scan)
   - Trivy vulnerability scan

See [CI.md](CI.md) for detailed documentation.

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_example.py

# Specific marker
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.database` - Database tests
- `@pytest.mark.asyncio` - Async tests
- `@pytest.mark.slow` - Slow tests

### Coverage Reports

Generate HTML coverage report:

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View in browser
```

## Code Quality

### Linting Tools

- **Black**: Code formatter (line length: 120)
- **isort**: Import organizer
- **Flake8**: Style guide enforcement
- **Pylint**: Code analysis

### Running Locally

```bash
# Format code
black .
isort .

# Check code
flake8 .
pylint app/

# All at once
pre-commit run --all-files
```

### Configuration Files

- `.flake8` - Flake8 rules
- `pyproject.toml` - Black, isort, Pytest config
- `.editorconfig` - Editor settings
- `.pre-commit-config.yaml` - Pre-commit hooks


### Useful Commands

```bash
cd infra

# View infrastructure
terraform state list
terraform state show aws_rds_cluster.main

# Plan and apply
terraform plan -out=tfplan
terraform apply tfplan

# Destroy
terraform destroy

# Format and validate
terraform fmt -recursive
terraform validate
```

## Security

### Pre-Built Security Features

- IAM roles with least-privilege policies
- Security groups restrictive by default
- Encrypted RDS storage and transit
- SQS DLQ for failed messages
- CloudWatch monitoring and alarms
- API Gateway rate limiting

### Secrets Management

For sensitive values (database passwords, API keys):

1. **Local Development**: Use `.env` file 
2. **GitHub Secrets**: Store in repository secrets
3. **AWS Secrets Manager**: For production secrets

### Pre-commit Security Checks

```bash
# Install pre-commit hooks
pre-commit install

# Manual run
pre-commit run --all-files
```

Includes:

- Bandit (Python security)
- tfsec (Terraform security)
- Private key detection

##  Development Workflow

1. **Create feature branch**

```bash
git checkout -b feature/my-feature
```

2. **Make changes and commit**

```bash
git add .
pre-commit run --all-files  # Runs linting
git commit -m "feat: add my feature"
```

3. **Push and create PR**

```bash
git push origin feature/my-feature
```

4. **GitHub Actions runs automatically**
   - Python linting
   - Tests
   - Terraform validation
   - Security scan
   - Terraform plan comment on PR

5. **Merge to main**
   - Infrastructure updates deployed after merge

## Documentation

- [Infrastructure Documentation](infra/README.md)
- [CI/CD Pipeline Documentation](CI.md)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🐛 Troubleshooting

### Tests failing locally

1. Check Python version (3.13+)
2. Install all dependencies: `pip install -r requirements.txt -r requirements-test.txt`
3. Set environment variables if needed
4. Clear cache: `rm -rf .pytest_cache __pycache__`

### Terraform issues

1. Format files: `cd infra && terraform fmt -recursive`
2. Validate: `terraform validate`
3. Check credentials: `aws sts get-caller-identity`

### Linting errors

Run formatters first:

```bash
black . && isort .
```

Then check results:

```bash
flake8 .
```

## 📈 Monitoring and Logging

All services log to CloudWatch:

- `/ecs/pythonbackend` - Application logs
- `/aws/alb/pythonbackend` - Load balancer logs
- `/aws/apigateway/pythonbackend` - API Gateway logs
- RDS performance insights and enhanced monitoring
