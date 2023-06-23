terraform {
	required_version = ">=1.0"
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

# data lake 
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "music-streaming-bucket" {
  name          = var.streams_bucket
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition { 
      age = 90 // days
    }
  }

   force_destroy = true
}

# Dataproc
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/dataproc_cluster
resource "google_dataproc_cluster" "music-streaming-cluster"{
	name = "music-streaming-cluster"
	region = var.region

	cluster_config {
		staging_bucket = "music-streams-staging-bucket"

		software_config {
			override_properties = {
				"dataproc:dataproc.allow.zero.workers" = "true"
			}

			optional_components = ["DOCKER", "JUPYTER"]
		}

		master_config{
      num_instances = 1
      machine_type  = "n1-standard-4"

      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = 500
      }
		}

		worker_config {
			num_instances = 0
			machine_type     = "n1-standard-4"
		}
	}
}

# Compute engine
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance
resource "google_compute_instance" "default" {
  name = var.compute_engine
  # region = var.region
  zone = var.zone
  machine_type = "custom-4-16384" # 4 CPUs and 16GB ram

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      type = "pd-balanced"
      size = 30
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
}