# Infrastructure Provisioning

Here follows the steps to put everything up and running. Some of them require interaction with 
Google Cloud Platform (GCP). You may find a detailed description about those tasks in the very Cloud
documentation.

1. [GCP] Create a service account and set the following permissions:
    - Compute Admin
    - Compute Instance Admin (v1)
    - Cloud SQL Admin
    - Service Account Admin
    - Service Account User
    - Artifact Registry Administrator
    - Storage Admin
    - Project IAM Admin
    
1. [GCP] Create and download the service account key

1. [GCP] Enable the following APIs: 
    - Cloud Resource Manager API
    - Identity and Access Management (IAM) API
    - IAM Service Account Credentials API
    - Cloud SQL Admin API
    - Cloud Storage API
    - Artifact Registry API

1. [Control Machine] Generate SSH Keys. These keys should be added to the nodes. They will be used during Configuration phase.
    ```sh
    ssh-keygen -t rsa -N "" -b 2048 -C "my_user" -f ./my_key
    ```

1. [Control Machine] Adjust terraform variables. All vars are declared in [vars](vars.tf) file. 
You may pass them by command line or create a `.tfvars` definition file. Terraform will load `terraform.tfvars` automatically and set the variables. Here's a sample:

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

1. [Control Machine] This example uses a GCP Service Account credential to perform operations in the Cloud. 
Export GOOGLE_APPLICATION_CREDENTIALS env variable with the path to service account key 
(More on this [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started)).

    `export GOOGLE_APPLICATION_CREDENTIALS=/PATH_TO/SERVICE_ACCOUNT_KEY/file.json`

1. [Control Machine] Intialize Terraform. Terraform will download plugins, modules and register the version for each one
of them in a `locl.hcl`file.

    `terraform init`

1. [Control Machine] Plan and Apply your Infrastructure. Terraform creates all Infra.

    ```sh
    terraform plan
    terraform apply
    ```

1. [Control Machine] Extract important information from tfstate
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