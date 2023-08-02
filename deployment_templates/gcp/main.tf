provider "google" {
  credentials = file(var.credentials_path)
  project     = var.project
  region      = var.region
}

provider "google-beta" {
  project = var.project
  credentials = file(var.credentials_path)
}

// Define the Cloud Run service

resource "google_cloud_run_service" "default" {
  name     = var.image
  location = var.region
  depends_on = [
    google_sql_database_instance.default,
    google_sql_database.default,
    google_sql_user.default,
    google_project_service.run
  ]

  template {
    spec {
      containers {
        image = var.image

        ports {
          container_port = var.image_port
        }
        env {
          name  = var.env_db_host
          value = "${google_sql_database_instance.default.ip_address[0].ip_address}"
        }
        env {
          name  = var.env_db_user
          value = "${google_sql_user.default.name}"
        }
        env {
          name  = var.env_db_password
          value = "${google_sql_user.default.password}"
        }
        env {
          name  = var.env_db_name
          value = "${google_sql_database.default.name}"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
  
}

resource "google_cloud_run_service_iam_binding" "public" {
  service  = google_cloud_run_service.default.name
  location = google_cloud_run_service.default.location
  role     = "roles/run.invoker"

  members = [
    "allUsers",
  ]
}


// Define the Cloud SQL instance
resource "google_sql_database_instance" "default" {
  name             = var.db_name
  region           = var.region
  database_version = var.db_version
  deletion_protection = false

  depends_on = [
    google_project_service.sqladmin
  ]

  settings {
    tier = "db-f1-micro"
    availability_type    = "REGIONAL" // Enable high availability

    backup_configuration {
      enabled            = true
      binary_log_enabled = true // Required for MySQL
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "all_ips"
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_user" "default" {
  name     = var.db_user
  instance = google_sql_database_instance.default.name
  password = var.db_password
  depends_on = [
    google_project_service.sqladmin
  ]
}

// Define the Cloud SQL database
resource "google_sql_database" "default" {
  name       = var.db_name
  instance   = google_sql_database_instance.default.name
  project    = var.project
  charset    = "utf8"
  collation  = "utf8_general_ci"
  depends_on = [
    google_project_service.sqladmin
  ]
}

// enable services
resource "google_project_service" "run" {
  service = "run.googleapis.com"

  disable_dependent_services = true
}

resource "google_project_service" "sqladmin" {
  service = "sqladmin.googleapis.com"

  disable_dependent_services = true
}

resource "google_project_service" "cloudresourcemanager" {
  service = "cloudresourcemanager.googleapis.com"
  disable_dependent_services = true
}
