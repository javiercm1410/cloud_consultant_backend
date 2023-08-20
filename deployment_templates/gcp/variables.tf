variable "project" {
  description = "Google Cloud Project ID"
  type        = string
  default = "cloudconsultant"
}

variable "region" {
  description = "Region to deploy the Cloud Run service"
  type        = string
  default  = "us-east1"
}

variable "credentials_path" {
  description = "credential for gcp"
  type        = string
  default  = "/Users/simon/.google/credentials/cloudconsultant-fc0ed56f2037.json"
}

variable "db_password" {
  description = "Database password"
  type        = string
  default  = "admin123!"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default  = "admin-db"
}

variable "db_user" {
  description = "Database name"
  type        = string
  default  = "admin-user"
}

variable "db_version" {
  description = "Database version"
  type        = string
  default  = "MYSQL_5_7"
}

variable "env_db_host" {
  description = "DB host name"
  type        = string
  default  = "WORDPRESS_DB_HOST"
}

variable "env_db_name" {
  description = "DB name"
  type        = string
  default  = "WORDPRESS_DB_NAME"
}

variable "env_db_password" {
  description = "DB password"
  type        = string
  default  = "WORDPRESS_DB_PASSWORD"
}

variable "env_db_user" {
  description = "DB user"
  type        = string
  default  = "WORDPRESS_DB_USER"
}

variable "image" {
  description = "Image name"
  type        = string
  default  = "wordpress"
}

variable "image_port" {
  description = "Image port"
  type        = number
  default  = 80
}
