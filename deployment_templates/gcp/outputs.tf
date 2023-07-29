output "db_ip_addr" {
  value       = google_sql_database_instance.default.ip_address[0].ip_address
  description = "Database IP number"
}

output "db_connection_name" {
  value       = google_sql_database_instance.default.connection_name
  description = "Database identifier in GCP"
}

output "container_url" {
  value       = google_cloud_run_service.default.status[0].url
  description = "Container access url"
}

output "container_name" {
  value       = google_cloud_run_service.default.name
  description = "Container name"
}


