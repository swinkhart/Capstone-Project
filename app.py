from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# database tables
class Users(db.Model):
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.email

# website routes
isLoggedIn = False

@app.route('/', methods=["GET", "POST"])
def index():
    #email = request.form.get("email")
    #password = request.form.get("password")

    usersInDatabase = Users.query.all()
    return render_template("index.html", isLoggedIn=isLoggedIn, usersInDatabase=usersInDatabase)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signupResponse', methods=["POST"])
def signupResponse():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")
    passwordVerify = request.form.get("passwordVerify")
    blankInputError = ""
    passwordMismatchError = ""

    if not firstName or not lastName or not email or not password or not passwordVerify:
        blankInputError = "please fill in all fields"
    
    if password != passwordVerify:
        passwordMismatchError = "passwords do not match"

    if blankInputError or passwordMismatchError:
        return render_template("signup.html", firstName=firstName, lastName=lastName, email=email, password=password, passwordVerify=passwordVerify,
                               blankInputError=blankInputError, passwordMismatchError=passwordMismatchError)
    else:
        # add to database class
        newUser = Users(firstName=firstName, lastName=lastName, email=email, password=password)

        # push and commit to database
        try:
            db.session.add(newUser)
            db.session.commit()
            return render_template("signupResponse.html"), {"Refresh": "2; url=/login"}
        except:
            return "error adding user to database"

@app.route('/flashcard')
def flashcard():
    return render_template("flashcard.html")