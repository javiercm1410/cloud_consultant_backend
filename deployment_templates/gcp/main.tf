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
  name     = "wordpress"
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
        image = "wordpress:latest"

        ports {
          container_port = 80
        }
        # env {
        #   name  = "url"
        #   value = "http://localhost:2368"
        # }
        # env {
        #   name  = "database__client"
        #   value = "sqlite3"
        # }
        # env {
        #   name  = "database__connection__filename"
        #   value = "/var/lib/ghost/content/data/ghost.db"
        # }
        # env {
        #   name  = "database__client"
        #   value = "mysql"
        # }
        env {
          name  = "WORDPRESS_DB_HOST"
          value = "${google_sql_database_instance.default.ip_address[0].ip_address}"
        }
        env {
          name  = "WORDPRESS_DB_USER"
          value = "${google_sql_user.default.name}"
        }
        env {
          name  = "WORDPRESS_DB_PASSWORD"
          value = "${google_sql_user.default.password}"
        }
        env {
          name  = "WORDPRESS_DB_NAME"
          value = "${google_sql_database.default.name}"
        }
        # env {
        #   name  = "database__connection__port"
        #   value = "3306"
        # }
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
  name             = "admin-db"
  region           = var.region
  database_version = "MYSQL_5_7"
  deletion_protection = false
  depends_on = [
    google_project_service.sqladmin
  ]

  settings {
    tier = "db-f1-micro"

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
  name     = "admin-user"
  instance = google_sql_database_instance.default.name
  password = var.db_password
  depends_on = [
    google_project_service.sqladmin
  ]
}

// Define the Cloud SQL database
resource "google_sql_database" "default" {
  name       = "admin-db"
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
