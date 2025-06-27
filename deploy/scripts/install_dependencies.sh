#!/bin/bash

# Update and install Docker
sudo apt-get update -y
sudo apt-get install docker.io -y

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Install unzip and curl
sudo apt-get install unzip curl -y

# Download and install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -o awscliv2.zip
sudo ./aws/install

# Add ubuntu user to the docker group (so you can run docker without sudo)
sudo usermod -aG docker ubuntu

# Clean up installer files
rm -rf awscliv2.zip aws
