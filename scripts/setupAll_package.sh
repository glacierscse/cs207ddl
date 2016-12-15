# git clone
sudo apt-get install git

git clone https://github.com/glacierscse/cs207ddl.git

#install all packages
bash ./cs207ddl/scripts/setuppackage.sh

#set up the databases
bash ./cs207ddl/setupEC2.sh

#set up the server
bash ./cs207ddl/scripts/serversetup.sh

#chmod +x setupAll.sh
#Put in readme, hitting yes 1+1+1
