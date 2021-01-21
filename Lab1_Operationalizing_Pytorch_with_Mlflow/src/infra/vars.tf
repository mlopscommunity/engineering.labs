# Configurations for Google Cloud Provider
variable "gcp_project" {
  description = "GCP Project Id"
  default     = "engineeringlab"
}

variable "gcp_region" {
  description = "GCP Region to use"
  default     = "us-east1"
}

variable "gcp_zone" {
  description = "GCP Zone to use"
  default     = "us-east1-a"
}

variable "ip_cidr_range" {
  description = "IP CIDR range for the subnetwork"
  default     = "10.20.30.0/24"
}

variable "vm_image" {
  description = "SO Image to be used"
  default     = "ubuntu-1804-bionic-v20201014"
}

variable "ansible_ssh" {
  type        = map(string)
  description = "SSH public key file used by ansible to configure the server"
  default = {
    user     = "ansible"
    key_file = "ansible-key.pub"
  }
}