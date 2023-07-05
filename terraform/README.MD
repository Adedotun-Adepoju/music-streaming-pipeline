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
