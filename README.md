# cs207ddl project for CS207

## How to use it
start with running the bash file as follow in the main directory:
bash setup.sh 
This file deletes the old databases (if exists) and generate the 3 new database. 

Then from sockets/dir run: (cd sockets/)
python Server.py

and from main directory run:
python run.py

This creates the connection between the server and client

Now copy the website link from the terminal (something like: http://127.0.0.1:5000/)
Now we can upload the json file or id onto the server and return the 5 most similar time series in the database. This uses the connection between flask and server and the UI. 

## How use the website
On the website, there are three buttons: Upload a JSON File, Get Similar and Display button. If the user input a valid timeseries ID into the window, and then click the the Get Similar button, then the top five most similar timeseries IDs will show on the website. If the user then click the Display button, then the plots of the five nearest timeseries will be displayed. The website UI also support JSON file upload. If the user upload a valid JSON file, and then click the Display button, the top five most similar timeseries from the database will be plotted. 

## pip setup package
Create a pip setup package for the project by using Pyscaffold in the dist/glacierscse-1.0.tar.gz. Also setup.cfg, setup.py and glacierscse.egg-info/* are included.


## EC2 platform
We try to install the program on EC2 and we created three shell scripts. Run the file “setupAll_package.sh” will set up everything, and you can get it from a S3 bucket.

1. $wget https://s3-us-west-2.amazonaws.com/fall16/cs207project/setupAll_package.sh
2. $chmod +x  setupAll_package.sh
3. $./setupAll_package.sh

The setupAll_package.sh will first clone our git repository to the EC2 instance. Then it will call “./cs207ddl/scripts/setuppackage.sh” to install all required packages. Then it will call “./cs207ddl/setup.sh” to set up all databases. Last, it will call “./cs207ddl/scripts/serversetup.sh” to set up the server and the web server on EC2 instance. 
