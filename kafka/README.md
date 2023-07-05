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
- After setting this up, you can then SSH into the new servers using the command below
```sh
ssh vm-instance
```
- If you use VS code as your editor, you can install the Remote-SSH extension. This allows you to open any folder on a remote machine using SSH.