#!/bin/bash

# Run using ./setup.sh

if ! [ -d ./bin ];
then 
    echo -e '\nCreating ~/bin directory\n'
    mkdir -p bin
fi 

echo -e "\nRunning sudo apt-get update...\n"
sudo apt-get update 

echo -e "\nInstalling Docker...\n"
sudo apt-get -y install docker.io 

echo -e "\nInstalling docker-compose...\n"
cd 
cd bin 

wget https://github.com/docker/compose/releases/download/v2.12.0/docker-compose-linux-x86_64 -O docker-compose
sudo chmod +x docker-compose 

echo -e "\nSetup .bashrc...\n"

echo -e ''>> ~/.bashrc
echo -e 'export PATH=${HOME}/bin:${PATH}' >> ~/.bashrc
echo -e ''>> ~/.bashrc
# echo -e 'export GOOGLE_APPLICATION_CREDENTIALS="${HOME}/.google/credentials/google_credentials.json"' >> ~/.bashrc

sudo docker --version
docker-compose --version 

echo -e "\nSetting up Docker without sudo setup...\n"
sudo groupadd docker 
sudo usermod -aG docker $USER
newgrp docker