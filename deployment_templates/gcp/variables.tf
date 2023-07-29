variable "name" {
  description = "Name for the load balancer resources"
  type        = string
  default    = "load-balancer"
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
  default = "cloudconsultant"
}

variable "region" {
  description = "Region to deploy the Cloud Run service"
  type        = string
  default  = "us-central1"
}

variable "db_password" {
  description = "Database password"
  type        = string
  default  = "admin123!"
}

variable credentials_path {
  description = "credential for gcp"
  type        = string
  default  = "/Users/simon/.google/credentials/cloudconsultant-fc0ed56f2037.json"
}
