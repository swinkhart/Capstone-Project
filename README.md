# Capstone-Project

**instructions:**

- Install latest version of Python and select the option to add to path during install
- Create a python virtual enviroment with the command **pyhton -m venv env** to isolate the installed packages from the global enviroment
- activate the virtual enviroment using a cmd terminal with the command **env\Scripts\activate.bat** on windows or zsh terminal and the command **env/Scripts/activate** on mac
- once acitavated, in the terminal type **"pip install -r requirements.txt"** to install all the necessary packages
- Navigate to project folder and type **"Flask run --debug"** to start the local server (--debug option allows for automatic server updates)
- Copy and paste the url or ctrl click on the link to view the website
- Type **"set FLASK_APP=app.py"** (Windows CMD) to let flask know where to find the application (**"export FLASK_APP=app.py"** for Linux, Mac)
- Once done make sure to deactiave the virtual envirment using a cmd terminal and the command **env\Scripts\deactivate.bat** on windows or a zsh terminal and the command **env/Scripts/deactivate**

**database setup**

- Type **"flask shell"** to open python interactive shell
- Next, type **"from app import db"** to import the database object
- Lastly, type **"db.create_all()"** to create the database (NOTE: db.create_all() does not recreate or update tables that already exist. You will need to drop the database with **"db.drop_all()"** and then recreate it again if changes are made to the database)
