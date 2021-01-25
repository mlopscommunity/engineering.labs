output "training_node" {
  description = "Training Node public IP"
  value       = google_compute_instance.training_node.network_interface.0.access_config.0.nat_ip
}

output "tracking_node" {
  description = "Tracking Node public IP"
  value       = google_compute_instance.tracking_node.network_interface.0.access_config.0.nat_ip
}

output "serving_node" {
  description = "Serving Node public IP"
  value       = google_compute_instance.serving_node.network_interface.0.access_config.0.nat_ip
}

output "sql_url_conn" {
  description = "Possible URL conection for this resource"
  sensitive   = true
  value       = "postgresql://${var.mlflow_db_user}:${var.mlflow_db_pass}@${google_sql_database_instance.englab_db_instance.public_ip_address}:5432/${var.mlflow_db_name}"
}

output "sql_connection_name" {
  description = "Cloud SQL Connection Name for other uses"
  value       = google_sql_database_instance.englab_db_instance.connection_name
}

output "sql_public_ip" {
  description = "Cloud SQL DB Instance Public IP"
  value       = google_sql_database_instance.englab_db_instance.public_ip_address
}

output "registry_url" {
  description = "Private Docker Registry URI"
  value       = "${google_artifact_registry_repository.englab_repository.location}-docker.pkg.dev"
}

# output "storage_url" {
#   description = "MLFLow Data Storage URL"
#   value = google_storage_bucket.mlflow_data_bucket.url
# }

output "inventory" {
  description = "Inventory file for Ansible"
  sensitive   = true
  value = templatefile("inventory.tmpl", { trainer = google_compute_instance.training_node,
    tracker = google_compute_instance.tracking_node
  server = google_compute_instance.serving_node })
}