# Infrastructure Automation

Our infrastructure automation is divided into two stages: Provisioning and Configuration. 
During Provisioning, we use [Terraform](https://www.terraform.io/) to provider for VMs, DBs and other
resources needed by the project. The resources created are set up during Configuration stage.
All resouces adjustments are made by [Ansible](https://www.ansible.com/).

## Infrastrucuture Description

--> TODO: Figure

Main assets:

| Asset | Description | Physical Name \ ID | 
|-------|-------------|--------------------|
| Training Node | VM responsible for training phase of ML Component pipeline | training-node |
| Tracking Node | VM hosting MLFlow Server | tracking-node |
| Serving Node | VM hosting docker containers and serving models | serving-node |
| VPC | Virtual Network and its subnetwork which define internal and external IPs for each node | englab-vpc |
| Service Account | Service Account with proper permissions to access services and other resources in th Cloud | mlflow-data |
| DB Instance | Postgres DB Instacnce used by MLFLow Server | englab * |
| Database | Postgres Relational datavase used by MLFLow Server | mlflow_db |
| Artifact Repository | Artifact \ Docker Repository where you may store ML Component docker images | englab-repository * | 

<br>
Although this table is informative, you should double check the assets names or ids by using _Terraform outputs_.
Some of the assets may have dynamic names and others may be changed by information in Terraform variables. Check
the [README.md](prov/README.md).

## Set Up

You have to install both tools in order to reproduce the MLFlow experiment:
- Terraform: Just download the binary file from [here](https://www.terraform.io/downloads.html) and
place it in your path;
- Ansible: You may install Ansible using a package from your distribution or from Python. You can also
use [Conda](https://docs.conda.io/en/latest/). We provide a Conda environment file in configuration folder which
you can install by the following command `conda env create -n my_env -f environment.yml`.

You can find the detailed procedure for each phase in the following folders: 
- **[prov](prov/)** Infrastructure definition using Terraform `.tf` files; 
- **[conf](conf/)** Infrastructure configuration using Ansible playbooks.



