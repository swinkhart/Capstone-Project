from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:testpwd@capstone5.cs.kent.edu/test'
db = SQLAlchemy(app)

# database table models
class Login(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    class_number = db.Column(db.Integer, nullable=False)
    account_type = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# website routes

@app.route('/', methods=["GET", "POST"])
def index():
    
    tempEmail = ""
    if "userEmail" in session:
        tempEmail = session["userEmail"]

    tempUsersInDatabase = db.session.query(Login.email)
    return render_template("index.html", email=tempEmail, usersInDatabase=tempUsersInDatabase)
    #return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    tempIncorrectLoginInfo = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        infoRecords = Login.query.with_entities(Login.email, Login.password).all()
        for infoRecord in infoRecords:
            if (email == infoRecord.email) and (password == infoRecord.password):
                session["userEmail"] = email
                return redirect(url_for("index"))
        tempIncorrectLoginInfo = "incorrect email or password"
        return render_template("login.html", incorrectLoginInfo=tempIncorrectLoginInfo)
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
    tempClassNumber = request.form.get("classNumber")
    tempAccountType = request.form.get("accountType")
    tempEmail = request.form.get("email")
    tempPassword = request.form.get("password")
    tempPasswordVerify = request.form.get("passwordVerify")
    tempBlankInputError = ""
    tempPasswordMismatchError = ""

    if not tempClassNumber or not tempAccountType or not tempEmail or not tempPassword or not tempPasswordVerify:
        tempBlankInputError = "please fill in all fields"
    
    if tempPassword != tempPasswordVerify:
        tempPasswordMismatchError = "passwords do not match"

    if tempBlankInputError or tempPasswordMismatchError:
        return render_template("signup.html", classNumber=tempClassNumber, accountType=tempAccountType, email=tempEmail, password=tempPassword, passwordVerify=tempPasswordVerify,
                               blankInputError=tempBlankInputError, passwordMismatchError=tempPasswordMismatchError)
    else:
        # add to database class
        newUser = Login(email=tempEmail, class_number=int(tempClassNumber), account_type=bool(int(tempAccountType)), password=tempPassword)

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

