terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.52.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "google_compute_instance" "training_node" {
  name         = "training-node"
  machine_type = "c2-standard-8"
  tags         = ["ssh", "web"]
  zone         = var.gcp_zone

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20210105"
      size  = 100
      type  = "pd-ssd"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.englab_subnet.name

    access_config {
      // Ephemeral IP
    }
  }

  metadata = {
    "ssh-keys" = "${var.ansible_ssh.user}:${file(var.ansible_ssh.key_file)}"
  }
}

resource "google_compute_instance" "tracking_node" {
  name         = "tracking-node"
  machine_type = "g1-small"
  tags         = ["ssh", "tracking"]
  zone         = "southamerica-east1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20210105"
      size  = 100
      type  = "pd-ssd"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.englab_subnet.name

    access_config {
      // Ephemeral IP
    }
  }

  metadata = {
    "ssh-keys" = "${var.ansible_ssh.user}:${file(var.ansible_ssh.key_file)}"
  }
}

resource "google_compute_instance" "serving_node" {
  name         = "serving-node"
  machine_type = "e2-standard-2"
  tags         = ["ssh", "serving"]
  zone         = "southamerica-east1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20210105"
      size  = 100
      type  = "pd-ssd"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.englab_subnet.name

    access_config {
      // Ephemeral IP
    }
  }

  metadata = {
    "ssh-keys" = "${var.ansible_ssh.user}:${file(var.ansible_ssh.key_file)}"
  }
}