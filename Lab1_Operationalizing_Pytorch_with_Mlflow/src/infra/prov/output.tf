output "training_node" {
  value = google_compute_instance.training_node.network_interface.0.access_config.0.nat_ip
}

output "tracking_node" {
  value = google_compute_instance.tracking_node.network_interface.0.access_config.0.nat_ip
}

output "serving_node" {
  value = google_compute_instance.serving_node.network_interface.0.access_config.0.nat_ip
}

output "sql_connection_name" {
  value = google_sql_database_instance.englab_db_instance.connection_name
}

output "sql_public_ip" {
  value = google_sql_database_instance.englab_db_instance.public_ip_address
}

output "inventory" {
  value = templatefile("inventory.tmpl", { trainer = google_compute_instance.training_node,
    tracker = google_compute_instance.tracking_node
  server = google_compute_instance.serving_node })
}

output "registry_url" {
  value = "${google_artifact_registry_repository.englab_repository.location}-docker.pkg.dev"
}
