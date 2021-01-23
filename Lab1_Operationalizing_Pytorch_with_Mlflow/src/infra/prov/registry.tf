resource "google_artifact_registry_repository" "englab_repository" {
  provider = google-beta

  location      = var.gcp_region
  repository_id = "englab-repository"
  description   = "EngLabs private Repository"
  format        = "DOCKER"
}

resource "google_service_account" "repo_account" {
  provider     = google-beta
  account_id   = "repo-account"
  display_name = "Repository Service Account"
}

resource "google_artifact_registry_repository_iam_member" "repo-iam" {
  provider = google-beta

  location   = google_artifact_registry_repository.englab_repository.location
  repository = google_artifact_registry_repository.englab_repository.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.repo_account.email}"
}