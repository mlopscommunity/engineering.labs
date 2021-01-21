# Infrastructure Automation

We are mixing [Terraform](https://www.terraform.io/) and [Ansible](https://www.ansible.com/) to build 
our infrastructure. Here follows the steps to put everything up and running:

1. Install Terraform and Ansible

1. Create a service account add set the following permissions:
    - Compute Admin
    <!-- - Storage Admin -->

1. Create and download the service account key

1. Enable the following APIs: 
    - Cloud Resource Manager API
    - Identity and Access Management (IAM) API
    - Cloud SQL Admin API

1. Adjust terraform variables

    `terraform.tfvars`  file will be automatically loaded with the configured variables. 

1. Export GOOGLE_APPLICATION_CREDENTIALS env variable with the path to service account key

    `export GOOGLE_APPLICATION_CREDENTIALS=/PATH_TO/SERVICE_ACCOUNT_KEY/file.json`

1. Intialize Terraform

    `terraform init`

1. Plan and Apply your Infrastructure

    ```sh
    terraform plan
    terraform apply
    ```