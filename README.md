# Capstone-Project

**instructions:**
 - Install latest version of Python and select the option to add to path during install
 - Open a terminal and type **"pip install flask"** to install flask mini-framework
 - Navigate to project folder and type **"Flask run --debug"** to start the local server (--debug option allows for automatic server updates)
 - Copy and paste the url or ctrl click on the link to view the website
 - Type **"set FLASK_APP=app.py"** (Windows CMD) to let flask know where to find the application (**"export FLASK_APP=app.py"** for Linux, Mac)

**database setup**
 - Type **"pip install flask-sqlalchemy"** for database setup
 - Type **"flask shell"** to open python interactive shell
 - Next, type **"from app import db"** to import the database object
 - Lastly, type **"db.create_all()"** to create the database (NOTE: db.create_all() does not recreate or update tables that already exist. You will need to drop the database with **"db.drop_all()"** and then recreate it again if changes are made to the database)

**NOTE:**
 - when committing files, do not commit the database file (with .db suffix)
