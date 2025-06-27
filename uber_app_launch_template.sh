#!/bin/bash

sudo apt-get update -y

sudo apt-get install ruby -y

wget https://aws-codedeploy-eu-north-1.s3.eu-north-1.amazonaws.com/latest/install

chmod +x ./install

sudo ./install auto

sudo service codedeploy-agent start