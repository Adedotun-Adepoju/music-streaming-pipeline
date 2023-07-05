# Kafka set up on VM instance
- Set up SSH to connect to the VM instance from your local machine [SSH guide](https://cloud.google.com/compute/docs/connect/create-ssh-keys#linux-and-macos)
- Add the public key (.pub) to your VM instance [guide](https://cloud.google.com/compute/docs/connect/add-ssh-keys#expandable-2)
- create a config file in the ssh folder. This will be used to store the ssh keys that allows you to connect to a vm instance
```sh
cd ~/.ssh
touch config
```
- Open the config file and add the following lines to the file. You can modify the host name to anything you like 
```sh
Host vm-instance
    HostName <External Ip Address of the Instance>
    User <username used to create the ssh key>
    IdentityFIle <path to the private ssh key>
```
- Transfer your service account JSON file from your local machine to the VM instance
```sh
# Connect to the instance using SFTP
sftp vm-instance
mkdir -p .google/credentials
cd .google/credentials
# dump the google credential file to the google/credentials directory on the VM instance
put <path to your google credentials>
```
- After setting this up, you can then SSH into the new servers using the command below
```sh
ssh vm-instance
```

- If you use VS code as your editor, you can install the Remote-SSH extension. This allows you to open any folder on a remote machine using SSH.
- Once you establish a connection, you can clone the git repo 
```sh
git clone https://github.com/Adedotun-Adepoju/music-streaming-pipeline.git
cd music-streaming-pipeline
```
- Install necessary dependencies
```sh
# Run the VM setup script to install needed dependencies
bash vm_setup.sh
```
- Set environment varibales to point to the GCP keys:
``` sh
export GOOGLE_APPLICATION_CREDENTIALS="${HOME}/.google/credentials/<name-of/credential-file.json>"' >> ~/.bashrc
```
- Copy the contents in the env.example file to the environment file
```sh 
cat env.example >> .env
```
- Edit the external IP address in the env file. Locate the "KAFKA_ADVERTISED_LISTENERS. Change the External-IP-Address to the External IP of the VM

- Start the docker containers for Kafka
```sh
docker-compose -f docker-compose-kafka.yaml up -d
```
- Forward port 9021 to your local machine to access the control center on your local machine. If using Remote-ssh on VS code, go to the ports tab beside the terminal and forward port 9021.

- Try visiting the address http://localhost:9021. The Kafka control center should open.

- With that, the kafka server has been started and we can start publishing events to it and consuming from it
