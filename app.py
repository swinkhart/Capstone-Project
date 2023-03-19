from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# database tables
class Users(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    classNumber = db.Column(db.String(200), nullable=False)
    accountType = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.email

# website routes

@app.route('/', methods=["GET", "POST"])
def index():
    email = ""
    if "userEmail" in session:
        email = session["userEmail"]

    usersInDatabase = Users.query.all()
    return render_template("index.html", email=email, usersInDatabase=usersInDatabase)

@app.route('/login', methods=["GET", "POST"])
def login():
    incorrectLoginInfo = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        infoRecords = Users.query.with_entities(Users.email, Users.password).all()
        for infoRecord in infoRecords:
            if (email == infoRecord.email) and (password == infoRecord.password):
                session["userEmail"] = email
                return redirect(url_for("index"))
        incorrectLoginInfo = "incorrect email or password"
        return render_template("login.html", incorrectLoginInfo=incorrectLoginInfo)
    else:
        return render_template("login.html")
    
@app.route('/logout')
def logout():
    session.pop("userEmail", None)
    return redirect(url_for("login"))

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signupResponse', methods=["POST"])
def signupResponse():
    classNumber = request.form.get("classNumber")
    accountType = request.form.get("accountType")
    email = request.form.get("email")
    password = request.form.get("password")
    passwordVerify = request.form.get("passwordVerify")
    blankInputError = ""
    passwordMismatchError = ""

    if not classNumber or not accountType or not email or not password or not passwordVerify:
        blankInputError = "please fill in all fields"
    
    if password != passwordVerify:
        passwordMismatchError = "passwords do not match"

    if blankInputError or passwordMismatchError:
        return render_template("signup.html", classNumber=classNumber, accountType=accountType, email=email, password=password, passwordVerify=passwordVerify,
                               blankInputError=blankInputError, passwordMismatchError=passwordMismatchError)
    else:
        # add to database class
        newUser = Users(classNumber=classNumber, accountType=accountType, email=email, password=password)

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