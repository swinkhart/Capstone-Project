This code uses flask to do all the routing and to determine what HTML template page to load for the user. 
The backend (flask) uses jinja to pass variable to and from the HTML pages to then display.
This flask app is set up to use flask-sqlalchemy which is different from regular sqlalchemy in that it meshes with flask better.
All the required python packages are in requirements.txt.
Currently the flask app is set up to interface with a maria db database however that can be changed in the app.py file.
Currently hosting is setup using a mod_wsgi server hence the wsgi.py file, this works by running the app.py on the wsgi server,
and then using a reverse proxy in the appache ssl.conf config file to redirect all requests to localhost:8000. We did this because flask 
does not like to play nicely with reverse proxy.