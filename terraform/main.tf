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
resource "google_dataproc_cluster" "music-streaming-cluster"{
	name = "music-streaming-cluster"
	region = var.region
	zone = var.zone

	cluster_config {
		staging_bucket = "dataproc-staging-bucket"

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
		}
	}
}