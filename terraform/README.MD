# Terraform set up for GCP 
- Install the gcloud CLI [gcloud cli installation](https://cloud.google.com/sdk/docs/install)
- Install Terraform [terraform installation](https://developer.hashicorp.com/terraform/downloads)
- Create a service account. For development purposes, you can create an admin service account so you can have full access to GCP resources
- Download service-account json keys. Note the file directory. We will be using this for authentication
- Set environment varibales to point to the GCP keys:
```sh
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

# Refresh token/session, and verify authentication
gcloud auth application-default login
```
- Deploy Infrastructure
```sh
# Initialize the state file (.tfstate)
terraform init 

# Check the changes to be applied. You will be asked to enter your GCP ID
terraform plan 

# Deploy the changes to GCP
terraform apply 
```

Running this will deploy the following infrastructure to GCP:
- GCS bucket. You can set the name of the bucket in the variables.tf file
- Dataproc cluster for running Spark jobs with just 1 node
- VM instance to be used for running Kafka and Apache Airflow
- Firewall to expose port 9092 on the VM instace for the Spark cluster to connect
- BigQuery Data set to store the processed data 


