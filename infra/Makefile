.PHONY: init plan apply destroy fmt validate docs help

help:
	@echo "Available commands:"
	@echo "  make init     - Initialize Terraform"
	@echo "  make validate - Validate Terraform configuration"
	@echo "  make fmt      - Format Terraform files"
	@echo "  make plan     - Plan infrastructure changes"
	@echo "  make apply    - Apply infrastructure changes"
	@echo "  make destroy  - Destroy infrastructure"
	@echo "  make output   - Show Terraform outputs"
	@echo "  make fmt-check - Check if files are formatted correctly"

init:
	terraform init

validate:
	terraform validate

fmt:
	terraform fmt -recursive

fmt-check:
	terraform fmt -recursive -check

plan:
	terraform plan -out=tfplan

apply:
	terraform apply tfplan

destroy:
	terraform destroy

output:
	terraform output deployment_info

state-list:
	terraform state list

clean:
	rm -rf .terraform tfplan .terraform.lock.hcl

graph:
	terraform graph | dot -Tsvg > graph.svg
	@echo "Graph saved to graph.svg"

workspace-list:
	terraform workspace list

workspace-new:
	@read -p "Enter workspace name: " ws; \
	terraform workspace new $$ws

workspace-select:
	@read -p "Enter workspace name: " ws; \
	terraform workspace select $$ws
