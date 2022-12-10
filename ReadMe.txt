Used packages:
psycopg2: used to connect to the datbase and preform actions with the database.
Please make sure that you have this package install using pip.
If your isntallation of python does have tkinter please intsall that as well



To use:
change the username and password within the psycopg2.conenct call to match your localhost postgres server.


uses tkinter for the GUI, to run make sure your postgres service is running, change the username, password and possibly the port id found in the config file tothe settings of your local host postgres server
Then run DBinit.py to inialize the DB, afterwards the run UIscript.py to start the GUI, from there you should be able to interface with the database.

Some premade users that you can log into afterwards are
            Username    password
ADMIN USER: bookowner   admin 
CUSTOMER :  joe         2



