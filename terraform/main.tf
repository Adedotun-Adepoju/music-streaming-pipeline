terraform {
  backend "local" {}
	required_providers {
		google = {
			source = "hashicorp/google"
		}
	}
}

provider "google" {
	credentials = file(var.credentials)
	project = var.project
	region = var.region
}

# Dataproc