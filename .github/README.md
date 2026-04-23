# GitHub Configuration

This directory contains GitHub-specific configurations including Actions workflows.

## Secrets Configuration

### Optional Secrets for CI/CD

Add secrets in: Settings > Secrets and variables > Actions

**AWS_ROLE_TO_ASSUME** (Optional)

- Type: Repository Secret
- Format: `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME`
- Purpose: Allows Terraform Plan job to access AWS resources
- Note: Without this, `terraform plan` will run with `-backend=false`

## Workflows

### ci.yml

Main CI/CD pipeline that runs on:

- push to main/develop
- pull requests to main/develop
- manual trigger

See [../CI.md](../CI.md) for detailed documentation.

## Setting Up AWS Role for GitHub Actions

To enable full Terraform planning capabilities:

1. **Create IAM Role**

   ```bash
   aws iam create-role --role-name github-actions-role \
     --assume-role-policy-document file://trust-policy.json
   ```

2. **Create trust-policy.json**

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringLike": {
             "token.actions.githubusercontent.com:sub": "repo:USERNAME/REPO:*"
           }
         }
       }
     ]
   }
   ```

3. **Attach Policies**
   - Terraform needs appropriate AWS permissions
   - Principle of least privilege recommended

4. **Add Secret**
   - Add `AWS_ROLE_TO_ASSUME` secret to repository
   - Value: `arn:aws:iam::ACCOUNT_ID:role/github-actions-role`

## Branch Protection Rules

Consider adding branch protection for `main`:

- Require status checks to pass before merging
- Require reviews
- Require branches to be up to date
- Require code reviews from code owners

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS OIDC with GitHub Actions](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub Secrets Management](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
