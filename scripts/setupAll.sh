# git clone
sudo apt-get install git

git clone https://github.com/glacierscse/cs207ddl.git

#install all packages
bash ./cs207ddl/scripts/cs207_aws_ec2_stack.sh

#set up the databases
python ./cs207ddl/setup.py

#set up the server
bash ./cs207ddl/scripts/serversetup.sh

#chmod +x setupAll.sh
#Put in readme, hitting yes 1+1+1