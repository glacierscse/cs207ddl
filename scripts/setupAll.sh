# git clone
sudo apt-get install git

sudo git clone https://github.com/glacierscse/cs207ddl.git

#install all packages
./scripts/cs207_aws_ec2_stack.sh

#set up the database
python3 setup.py

#set up the server
./scripts/serversetup.sh
