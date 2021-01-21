resource "google_sql_database_instance" "englab_db_instance" {
  name             = "englab"
  database_version = "POSTGRES_12"

  # CAREFUL: Just uncomment line below if you know what you're doing!
  deletion_protection=false

  settings {
    tier = "db-f1-micro"
    backup_configuration {
      enabled    = true
      start_time = "04:30"
    }
  }
}
resource "google_sql_user" "users" {
  name     = var.mlflow_db_user
  instance = google_sql_database_instance.englab_db_instance.name
  password = var.mlflow_db_pass
}
resource "google_sql_database" "database" {
  name     = var.mlflow_db_name
  instance = google_sql_database_instance.englab_db_instance.name
}