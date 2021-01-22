# Infrastructure Automation

Our infrastructure automation is divided into two stages: Provisioning and Configuration. 
During Provisioning, we use [Terraform](https://www.terraform.io/) to provider for VMs, DBs and other
resources needed by the project. The resources created are set up during Configuration stage.
All resouces adjustments are made by [Ansible](https://www.ansible.com/).

### Organization

- **[prov](prov/)**: Infrastructure definition organized into Terraform `.tf` files
- **[conf](conf/)**: Ansible playbooks.

