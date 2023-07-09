variable "client_id" {
  type        = string
  default     = ""
  description = "Azure Client ID"
}

variable "client_secret" {
  type        = string
  default     = ""
  description = "Azure Client Secret"
  sensitive   = true
}

variable "tenant_id" {
  type        = string
  default     = ""
  description = "Azure Tenant ID"
}

variable "subscription_id" {
  type        = string
  default     = ""
  description = "Azure Subscription ID"
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.64.0"
    }
  }
}

provider "azurerm" {
  features {}
  client_id                  = var.client_id
  client_secret              = var.client_secret
  tenant_id                  = var.tenant_id
  subscription_id            = var.subscription_id
  skip_provider_registration = true
}

resource "azurerm_resource_group" "cc-rg-1" {
  name     = "cc-rg-1"
  location = "East US 2"
}
