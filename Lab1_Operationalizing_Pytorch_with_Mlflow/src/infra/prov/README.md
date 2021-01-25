# Infrastructure Provisioning

Here follows the steps to put everything up and running:

1. Install Terraform

1. Create a service account add set the following permissions:
    - Compute Admin
    - Compute Instance Admin (v1)
    - Cloud SQL Admin
    - Service Account Admin
    - Service Account User
    - Artifact Registry Administrator
    - Storage Admin
    - Project IAM Admin
    
1. Create and download the service account key

1. Enable the following APIs: 
    - Cloud Resource Manager API
    - Identity and Access Management (IAM) API
    - IAM Service Account Credentials API
    - Cloud SQL Admin API
    - Cloud Storage API
    - Artifact Registry API

1. Adjust terraform variables. You may pass them by command line or create a `.tfvars` definition file. All vars are declared in [vars](vars.tf) file. Terraform will load `terraform.tfvars` automatically and set the variables. Here's a sample:

    ```
    gcp_region = "southamerica-east1"
    gcp_zone   = "southamerica-east1-a"

    ansible_ssh = {
    user     = "ansible"
    key_file = "/path/to/ssh_pub_key/ansible-key.pub"
    }

    mlflow_db_user = "mlflow_server_db_user"
    mlflow_db_pass = "mlflow_server_db_pass"
    ```

1. This example uses a GCP Service Account credential to perform operations in the Cloud. Export GOOGLE_APPLICATION_CREDENTIALS env variable with the path to service account key 
(More on this [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started)).

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
    - MLFlow Server URL Connection:
    ```sh
    terraform output sql_url_conn
    ```
    - Docker Registry URL:
    ```sh
    terraform output registry_url
    ```
    
