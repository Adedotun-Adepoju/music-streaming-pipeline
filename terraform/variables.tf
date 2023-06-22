variable project {
	description = "Your GCP project ID"
}

variable credentials {
	description = "path to service key account"
	default = "~/.google/credentials/music-streaming-pipeline-d1ee678646bb.json"
}

variable region {
	description = "Region for GCP resources"
  default = "europe-west1"
  type = string
}

variable "zone"{
    description = "Zone for GCP resources"
    default = "europe-west1-b"
}

variable streams_bucket {
	description = "Bucket for storing files from dataproc"
	default = "music-streams-staging-bucket"
}

variable "storage_class" {
    description = "Storage class type for your bucket"
    default = "STANDARD"
}

