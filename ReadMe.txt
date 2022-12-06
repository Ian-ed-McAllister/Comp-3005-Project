Used packages:
psycopg2: used to connect to the datbase and preform actions with the database.



To use:
change the username and password within the psycopg2.conenct call to match your localhost postgres server.



uses tkinter for the GUI, to run make sure your postgres service is running, change the username, password and possibly the port id found in the config file tothe settings of your local host postgres server
Then run DBinit.py to inialize the DB, afterwards the run UIscript.py to start the GUI, from there you should be able to interface with the database.

Some premade users that you can log into afterwards are

ADMIN USER:
CUSTOMER 1:
CUSTOMER 2:




TODO: 

FINISH MAIN PAGE: add to cart (add more columns, select book + quantity,search (title, publisher, etc...), button to login, button to user info)
TO START: CHECKOUT, USER INFO, ADMIN INFO, LOGIN PAGE,
