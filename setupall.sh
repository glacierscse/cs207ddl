#!/bin/bash

printf "\n*******************************************************"
printf "\nGit Clone ...\n"
sudo apt-get install git

git clone https://github.com/glacierscse/cs207ddl.git


printf "\n*******************************************************"
printf "\nSet up all packages...\n"
# CS207 AWS EC2 Ubuntu 16.04 instance provisioning script (for final project)
# Installs final project stack: numpy, Flask, SQL Alchemy, nginx, and PostgreSQL
# Also configures firewall for nginx HTTP access, starts nginx server,
# and runs basic checks to ensure installation completed and services started.

# show the current Python 3 version (if any)
python3 --version

# update / upgrade the current software libraries
sudo apt-get update
sudo apt-get --upgrade

# install Python3 pip and development essentials + the psycopg2 library for PostgreSQL access
printf "\n*******************************************************"
printf "\nInstalling virtualenv, python3-pip, python3-dev, and psycopg2 ...\n"
sudo apt-get install virtualenv python3-pip python3-dev python3-psycopg2

# "~" specifies the AWS EC2 instance home directory for virtual environment
cd ~
mkdir venvs

# use the AWS EC2 Ubuntu 16.04 instance python3 installation
virtualenv --python=/usr/bin/python3 venvs/flaskproj

printf "\n*******************************************************"
printf "\nUpgrading pip ...\n"
pip3 install --upgrade pip

# install numpy for Python3
printf "\n*******************************************************"
printf "\nInstalling numpy ...\n"
sudo pip3 install numpy

# install portalocker for Python3
printf "\n*******************************************************"
printf "\nInstalling portalocker ...\n"
sudo pip3 install portalocker

# install scipy for Python3
printf "\n*******************************************************"
printf "\nInstalling scipy ...\n"
sudo pip3 install scipy

printf "\n*******************************************************"
printf "\nInstalling Flask and SQL Alchemy ...\n"
source ~/venvs/flaskproj/bin/activate

# install flask and SQLAlchemy for Python3
sudo pip3 install flask Flask-SQLAlchemy


# install PostgreSQL
printf "\n*******************************************************"
printf "\nInstalling PostgreSQL ...\n"
sudo apt-get install postgresql postgresql-contrib
echo "PostgreSQL installed"


# install and configure nginx
printf "\n*******************************************************"
printf "\nInstalling and starting nginx ...\n"
sudo apt-get install nginx
sudo service nginx start

printf "\nConfiguring firewall for nginx HTTP access ...\n"
sudo ufw app list # show current firewall settings
sudo ufw allow 'Nginx HTTP' # allow nginx to use HTTP port
printf "\nAfter configuring firewall for nginx HTTP access ...\n"
sudo ufw status

echo "nginx installed and configured \n"

# Installation should be complete and services started
# Run checks to be sure
printf "\n*******************************************************"
printf "\nINSTALLATION AND SERVICE CHECKS ...\n"
printf "\n*******************************************************"

printf "\nCan import numpy, Flask, SQLAlchemy, and psycopg2 in Python3?\n"
sudo python3 cs207_aws_ec2_stack_test.py

#printf "\nIs nginx running?\n"
#sudo service nginx status

printf "\nFINISHED!\n"


printf "\n*******************************************************"
printf "\nSet up all databases...\n"
rm -r timeseriesDB
rm -r ts_db_index
rm id.json
rm -r ts_data
rm API/app.db
python3 setup_DB.py


printf "\n*******************************************************"
printf "\nSet up all servers...\n"
# printf "\n*******************************************************"
# printf "\nInstalling gunicorn ...\n"
#
# sudo apt-get --yes --force-yes install gunicorn
# gunicorn --version
#
# printf "\nSetting up Gunicorn Configurationr\n"

# DANGEROUS but not for new instances
sudo pkill -f httpd
sudo pkill -f python

sudo rm /etc/nginx/sites-enabled/*
sudo rm /etc/nginx/sites-available/app_server_nginx.conf
sudo rm /etc/nginx/sites-available/api_server_nginx.conf
sudo cp /home/ubuntu/cs207ddl/conf/app_server_nginx.conf /etc/nginx/sites-available/
# sudo cp eztodo/api-server/conf/api_server_nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/app_server_nginx.conf /etc/nginx/sites-enabled/app_server_nginx.conf
# sudo ln -s /etc/nginx/sites-available/api_server_nginx.conf /etc/nginx/sites-enabled/api_server_nginx.conf

sudo service nginx restart

printf "\nMoving Repos Assets to www...\n"

#sudo mkdir /home/www  ???
#sudo rm /home/www/app-server -r
#sudo rm /home/www/api-server -r
#sudo cp ~/eztodo/app-server/ /home/www/ -r
#sudo cp ~/eztodo/api-server/ /home/www/ -r

printf "\nStarting Application Servers...\n"

# cd /home/www/app-server/ && nohup gunicorn app:app -b localhost:8000 & disown
# cd /home/www/api-server/ && nohup gunicorn flaskr:app -b localhost:5001 & disown

cd /home/ubuntu/cs207ddl && nohup python3 run.py & disown
cd /home/ubuntu/cs207ddl/sockets && nohup python3 Server.py & disown

printf "\nPython Processes...\n"
ps aux|grep python3

printf "\nFINISHED!\n"

printf "\nTry hitting the public domain now!\n"

printf "\nIs nginx running?\n"
sudo service nginx status
