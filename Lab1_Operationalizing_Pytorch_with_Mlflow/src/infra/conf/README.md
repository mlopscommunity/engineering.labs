# Infrastructure Configuration

Check inventory: `ANSIBLE_HOST_KEY_CHECKING=False ansible -i inventory.ini --private-key=<PATH_TO_PRIVATE_KEY> all -m ping -u <ansible_user>`


1. Install Collections and Roles: `ansible-galaxy install -r requirements.yml`
