# GitHub Actions CI Pipeline

Este arquivo descreve o pipeline de CI/CD configurado através do GitHub Actions.

## 📋 Visão Geral

O pipeline automatiza:

1. **Python Linting** - Verifica qualidade do código Python
2. **Python Tests** - Executa testes automatizados
3. **Terraform Validation** - Valida configurações Terraform
4. **Terraform Plan** - Gera plano Terraform para PRs
5. **Security Scanning** - Verifica vulnerabilidades

## 🔄 Workflow

### Triggers

O pipeline é acionado em:

- `push` para `main` e `develop`
- `pull_request` para `main` e `develop`
- Disparo manual (`workflow_dispatch`)

## 📦 Jobs

### 1. Python Linting (`python-lint`)

**Objetivo**: Verificar qualidade e estilo do código Python

**Ferramentas**:

- **Black**: Formatação de código
- **isort**: Organização de imports
- **Flake8**: Linting estático
- **Pylint**: Análise de código avançada

**Python Versions**: 3.11, 3.12

**Arquivos de Configuração**:

- `.flake8` - Configuração do Flake8
- `pyproject.toml` - Configuração do Black e isort

### 2. Python Tests (`python-tests`)

**Objetivo**: Executar testes automatizados

**Dependência**: Completa após `python-lint`

**Ferramentas**:

- **Pytest**: Framework de testes
- **pytest-cov**: Cobertura de código
- **pytest-asyncio**: Suporte para testes assíncronos

**Serviços**:

- PostgreSQL 16 (banco de dados para testes)

**Saídas**:

- Relatório de cobertura em `coverage.html`
- Upload para Codecov
- Artifacts mantidos por 30 dias

**Variáveis de Ambiente**:

- `DATABASE_URL`: URL de conexão do PostgreSQL

### 3. Terraform Validation (`terraform-validate`)

**Objetivo**: Validar configuração Terraform

**Ferramentas**:

- **Terraform**: Validação e formatação
- **tfsec**: Verificação de segurança Terraform

**Passos**:

1. Verifica formatação com `terraform fmt -check`
2. Inicializa com `terraform init -backend=false`
3. Valida com `terraform validate`
4. Executa tfsec para segurança

**Saídas**:

- Resultados tfsec em formato SARIF

### 4. Terraform Plan (`terraform-plan`)

**Objetivo**: Gerar plano Terraform para pull requests

**Dependência**: Completa após `terraform-validate`

**Disparador**: Apenas em `pull_request`

**Passos**:

1. Configura credenciais AWS (opcional - requer secret)
2. Inicializa Terraform
3. Executa `terraform plan`
4. Comenta PR com resultado do plano
5. Arquiva plan file

**Secrets Necessários** (opcional):

- `AWS_ROLE_TO_ASSUME`: ARN da role IAM para assumir

### 5. Security Scanning (`security-scan`)

**Objetivo**: Verificar vulnerabilidades

**Ferramentas**:

- **Trivy**: Scanner de vulnerabilidades

**Saídas**:

- Resultados em formato SARIF

### 6. Pipeline Summary (`summary`)

**Objetivo**: Resumo do status de todos os jobs

**Depende de**: Todos os outros jobs

## 📋 Arquivo de Configuração

**Localização**: `.github/workflows/ci.yml`

### Estrutura

```yaml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:
```

## 🔐 Secrets Necessários

### Opcional

- `AWS_ROLE_TO_ASSUME`: ARN da role para o Terraform Plan
  - Formato: `arn:aws:iam::123456789:role/github-actions-role`

### Configurar Secrets

1. Vá para Settings > Secrets and variables > Actions
2. Click em "New repository secret"
3. Adicione os secrets necessários

## 🧪 Configuração de Testes

### Estrutura de Diretórios

```
tests/
├── __init__.py
├── conftest.py          # Fixtures do Pytest
└── test_example.py      # Testes de exemplo
```

### Running Tests Localmente

```bash
# Instalar dependências de teste
pip install -r requirements-test.txt

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app --cov-report=html

# Executar testes específicos
pytest tests/test_example.py
pytest -m unit  # Apenas testes marcados como 'unit'
pytest -m "not slow"  # Pular testes lentos
```

### Marcadores de Teste

Disponíveis em `pytest.ini`:

```python
@pytest.mark.unit           # Testes unitários
@pytest.mark.integration    # Testes de integração
@pytest.mark.slow          # Testes lentos
@pytest.mark.database      # Testes com banco de dados
@pytest.mark.asyncio       # Testes assíncronos
```

## 🧹 Configuração de Linting

### Local

```bash
# Instalar ferramentas
pip install black flake8 pylint isort

# Formatar código com Black
black .

# Verificar imports com isort
isort .

# Verificar com Flake8
flake8 .

# Verificar com Pylint
pylint app/
```

### Arquivos de Configuração

- `.flake8` - Configuração Flake8
- `pyproject.toml` - Configuração Black, isort, Pytest
- `pytest.ini` - Configuração Pytest

## 📊 Artefatos

O pipeline gera os seguintes artefatos:

| Artefato        | Retenção | Descrição                        |
| --------------- | -------- | -------------------------------- |
| test-results-\* | 30 dias  | Resultados e cobertura de testes |
| terraform-plan  | 30 dias  | Arquivo de plano Terraform       |

## ⚠️ Limitações

### Terraform Plan sem AWS Credentials

Se `AWS_ROLE_TO_ASSUME` não estiver configurado, o Terraform Plan usará `terraform init -backend=false`.

Para funcionalidade completa:

1. Configure uma role IAM no AWS
2. Adicione o secret `AWS_ROLE_TO_ASSUME`
3. Atualize `.github/workflows/ci.yml`

## 📝 Exemplo de Configuração

### Como adicionar um novo teste

1. Crie um arquivo em `tests/test_*.py`:

```python
import pytest

@pytest.mark.unit
def test_my_feature():
    assert 1 + 1 == 2
```

2. O pipeline executará automaticamente

### Como adicionar um novo lint

Editar `.flake8` ou `pyproject.toml` conforme necessário.

## 🔄 Status do Pipeline

Visite a aba "Actions" do repositório para ver:

- ✅ Sucessos
- ❌ Falhas
- ⏳ Em andamento
- ⊘ Pulado

## 📞 Troubleshooting

### Testes falhando localmente mas passando no CI

1. Verifique as versões do Python (3.11, 3.12)
2. Verifique as dependências em requirements.txt
3. Verifique variáveis de ambiente

### Terraform plan com erro

1. Verifique a formatação com `cd infra && terraform fmt -recursive`
2. Verifique configs em `terraform.tfvars`
3. Valide localmente com `terraform validate`

### Lint errors

Execute localmente:

```bash
black . && isort . && flake8 .
```

## 📚 Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
