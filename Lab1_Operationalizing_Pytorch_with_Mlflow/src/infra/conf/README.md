# Infrastructure Configuration

After going through Provisioning you should have all nodes, networking and data storage created. Before
starting Configuration, you should _source_ Conda and activate your _environment_. Here are the Configuration
steps:

1. Install required Collections and Roles 
    ```sh
    ansible-galaxy install -r requirements.yml`
    ```

1. Fulfill inventory and required variables. You can check them [here](group_vars/all.yml). You can gather the
information from Terraform outputs. Check README in [prov](../prov)

1. Run Ansible playbook
    
    - ANSIBLE_HOST_KEY_CHECKING: If you want to disable SSH Host checking
    - inventory.ini: Ansible inventory with the nodes to be configured
    - --private-key: Private SSH key generated before
    - play.yml: The Playbook
    - ansible: Remote User
    - --become: Become root during the process

    ```sh
    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini --private-key=~/devel/mlops-comm/keys/ssh/englabs-ansible/ansible-key play.yml -u ansible --become
    ```

After that, All your Infrastructure should be configured.