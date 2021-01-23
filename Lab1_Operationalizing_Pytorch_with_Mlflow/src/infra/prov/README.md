# Infrastructure Provisioning

Here follows the steps to put everything up and running:

1. Install Terraform

1. Create a service account add set the following permissions:
    - Compute Admin
    - Cloud SQL Admin
    - Service Account Admin
    - Artifact Registry Administrator
    
1. Create and download the service account key

1. Enable the following APIs: 
    - Cloud Resource Manager API
    - Identity and Access Management (IAM) API
    - Cloud SQL Admin API
    - Artifact Registry API

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

1. Extract important information from tfstate
    - Ansible Inventory: 
    ```sh
    terraform output -raw inventory > ../conf/inventory.ini
    ```
    - Docker Registry URL: 
    ```sh
    terraform output registry_url
    ```
