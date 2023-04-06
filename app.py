from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import hashlib
import string
import random
import time

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:testpwd@capstone5.cs.kent.edu/test'
db = SQLAlchemy(app)

def hash_password(password):
    word = password
    password_bytes = word.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(password_bytes)
    word = sha256.hexdigest()
    return word

def random_string():
    chars=string.ascii_letters + string.digits
    choices = random.choices(chars, k=20)
    result = ''.join(choices)
    return result

# database table models
#modify to be one to many 
class Login(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    class_number = db.Column(db.Integer, nullable=False)
    account_type = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    salt = db.Column(db.String(25), nullable=False)

#figure out many to many or define a units table for each class --> one to many
class Units(db.Model):
    unit_number = db.Column(db.Integer, primary_key=True)
    class_number = db.Column(db.Integer, db.ForeignKey('Login.class_number'))
    #more stuff here 

#the many
class Card_Sets(db.Model):
    word = db.Column(db.String(50), primary_key=True)
    letter = db.Column(db.String(10), nullable=False)
    unit_number = db.Column(db.Integer, db.ForeignKey('Units.unit_number'))
    gif_path = db.Column(db.String(100), nullable=False)
    #more stuff here

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
        time.sleep(1)
        infoRecords = Login.query.with_entities(Login.email, Login.password, Login.salt).all()
        print(infoRecords)
        for infoRecord in infoRecords:
            if (email == infoRecord.email) and (hash_password(password + (infoRecord.salt)) == infoRecord.password):
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
        tempSalt = random_string()
        tempPassword = hash_password(tempPassword + tempSalt)
        newUser = Login(email=tempEmail, class_number=int(tempClassNumber), account_type=bool(int(tempAccountType)), password=tempPassword, salt=tempSalt)

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

@app.route('/flashcard_add')
def flashcard_add():
    return render_template("flashcard_add.html")
