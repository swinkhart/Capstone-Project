from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, SubmitField, SelectField, IntegerField, StringField
from wtforms.validators import InputRequired, DataRequired, NumberRange
import pymysql
import hashlib
import string
import random
import time
import os

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:testpwd@capstone5.cs.kent.edu/main'
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'static/images'

class UploadFileForm(FlaskForm):
    ASLClass = SelectField('ASLClass', validators=[InputRequired()], choices = [(1, "ASL 1"), (2, "ASL 2"), (3, "ASL 3"), (4, "ASL 4")])
    setNumber= IntegerField('SetNum', validators=[InputRequired(), DataRequired(), NumberRange(min=1)])
    GIFWord = StringField ('Word', validators=[InputRequired()])
    file = FileField('image', validators=[FileRequired(), FileAllowed(['gif'], 'GIFs only!')])
    submit = SubmitField("Upload File")

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
class Login(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    account_type = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    salt = db.Column(db.String(25), nullable=False)

class asl_1_units(db.Model):
    unit_number = db.Column(db.Integer, primary_key=True)

class asl_2_units(db.Model):
    unit_number = db.Column(db.Integer, primary_key=True)

class asl_3_units(db.Model):
    unit_number = db.Column(db.Integer, primary_key=True)

class asl_4_units(db.Model):
    unit_number = db.Column(db.Integer, primary_key=True)

class asl_1_set(db.Model):
    word = db.Column(db.String(50), primary_key=True)
    unit_number = db.Column(db.Integer, db.ForeignKey('asl_1_units.unit_number'))
    gif_path = db.Column(db.String(100), nullable=False)

class asl_2_set(db.Model):
    word = db.Column(db.String(50), primary_key=True)
    unit_number = db.Column(db.Integer, db.ForeignKey('asl_2_units.unit_number'))
    gif_path = db.Column(db.String(100), nullable=False)

class asl_3_set(db.Model):
    word = db.Column(db.String(50), primary_key=True)
    unit_number = db.Column(db.Integer, db.ForeignKey('asl_3_units.unit_number'))
    gif_path = db.Column(db.String(100), nullable=False)

class asl_4_set(db.Model):
    word = db.Column(db.String(50), primary_key=True)
    unit_number = db.Column(db.Integer, db.ForeignKey('asl_4_units.unit_number'))
    gif_path = db.Column(db.String(100), nullable=False)

# website routes

@app.route('/', methods=["GET", "POST"])
def index():
    
    tempEmail = ""
    if "userEmail" in session:
        tempEmail = session["userEmail"]

    return render_template("index.html", email=tempEmail)

@app.route('/login', methods=["GET", "POST"])
def login():
    tempIncorrectLoginInfo = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        time.sleep(1)
        infoRecords = Login.query.with_entities(Login.email, Login.password, Login.account_type, Login.salt).all()
        for infoRecord in infoRecords:
            if (email == infoRecord.email) and (hash_password(password + (infoRecord.salt)) == infoRecord.password):
                session["userEmail"] = email
                
                if (infoRecord.account_type == 1):
                    session["isTeacher"] = True
                else:
                    session["isTeacher"] = False

                print(session["isTeacher"])
                
                return redirect(url_for("index"))
        tempIncorrectLoginInfo = "incorrect email or password"
        return render_template("login.html", incorrectLoginInfo=tempIncorrectLoginInfo)
    else:
        return render_template("login.html")
    
@app.route('/logout')
def logout():
    session.pop("userEmail", None)
    session.pop("isTeacher", None)
    return redirect(url_for("login"))
    
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signupResponse', methods=["POST"])
def signupResponse():
    tempClassNumber = request.form.get("classNumber")
    tempEmail = request.form.get("email")
    tempPassword = request.form.get("password")
    tempPasswordVerify = request.form.get("passwordVerify")
    tempBlankInputError = ""
    tempPasswordMismatchError = ""

    if not tempClassNumber or not tempEmail or not tempPassword or not tempPasswordVerify:
        tempBlankInputError = "please fill in all fields"
    
    if tempPassword != tempPasswordVerify:
        tempPasswordMismatchError = "passwords do not match"

    if tempBlankInputError or tempPasswordMismatchError:
        return render_template("signup.html", classNumber=tempClassNumber, email=tempEmail, password=tempPassword, passwordVerify=tempPasswordVerify,
                               blankInputError=tempBlankInputError, passwordMismatchError=tempPasswordMismatchError)
    else:
        # add to database class
        tempSalt = random_string()
        tempPassword = hash_password(tempPassword + tempSalt)
        newUser = Login(email=tempEmail, account_type=0, password=tempPassword, salt=tempSalt)

        # push and commit to database
        try:
            db.session.add(newUser)
            db.session.commit()
            return render_template("signupResponse.html"), {"Refresh": "2; url=/login"}
        except:
            return "error adding user to database"

@app.route('/Classes')
def Classes():
    if "class_number" in session:
        session.pop("class_number", None)
    return render_template("Classes.html")

@app.route('/Units')
def Units():
    return render_template("Units.html")

@app.route('/flashcard')
def flashcard():
    return render_template("classes.html")

@app.route('/flashcard_units/<class_number>')
def flashcard_units(class_number):
    if class_number == "asl_1_units":
        session["class_number"] = "asl_1_units"
        tempSets = asl_1_units.query.with_entities(asl_1_units.unit_number).all()
        return render_template("flashcard_units.html", sets=tempSets)
    elif class_number == "asl_2_units":
        session["class_number"] = "asl_2_units"
        tempSets = asl_2_units.query.with_entities(asl_2_units.unit_number).all()
        return render_template("flashcard_units.html", sets=tempSets)
    elif class_number == "asl_3_units":
        session["class_number"] = "asl_3_units"
        tempSets = asl_3_units.query.with_entities(asl_3_units.unit_number).all()
        return render_template("flashcard_units.html", sets=tempSets)
    elif class_number == "asl_4_units":
        session["class_number"] = "asl_4_units"
        tempSets = asl_4_units.query.with_entities(asl_4_units.unit_number).all()
        return render_template("flashcard_units.html", sets=tempSets)

@app.route('/flashcard_cards/<unit_number>')
def flashcard_cards(unit_number):
    if session["class_number"] == "asl_1_units":
        tempCards = asl_1_set.query.filter(asl_1_set.unit_number == unit_number).all()
        return render_template("flashcard_cards.html", cards=tempCards)
    elif session["class_number"] == "asl_2_units":
        tempCards = asl_2_set.query.filter(asl_2_set.unit_number == unit_number).all()
        return render_template("flashcard_cards.html", cards=tempCards)
    elif session["class_number"] == "asl_3_units":
        tempCards = asl_3_set.query.filter(asl_3_set.unit_number == unit_number).all()
        return render_template("flashcard_cards.html", cards=tempCards)
    elif session["class_number"] == "asl_4_units":
        tempCards = asl_4_set.query.filter(asl_4_set.unit_number == unit_number).all()
        return render_template("flashcard_cards.html", cards=tempCards)

@app.route('/flashcard_add', methods=["GET", "POST"])
def flashcard_add():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        ClassNum = form.ASLClass.data
        setNum = form.setNumber.data
        WordGIF = form.GIFWord.data
        FilePath = ClassNum + "_" + str(setNum) + "_" + WordGIF
        match int(ClassNum):
            case 1:
                check_one = False
                sets = asl_1_units.query.with_entities(asl_1_units.unit_number).all()
                for set in sets:
                    if setNum == set.unit_number:
                        check_one = True
                if check_one == False:
                    newSet = asl_1_units(unit_number = setNum)
                    try:
                        db.session.add(newSet)
                        db.session.commit()
                    except:
                        return "error adding Set to database"
                check_one = False
                newFlashcard = asl_1_set(word = WordGIF, unit_number = setNum, gif_path = FilePath)
                try:
                    db.session.add(newFlashcard)
                    db.session.commit()
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(WordGIF)))
                    return render_template("flashcard_added.html"), {"Refresh": "2; url=/flashcard_add"}
                except:
                    return "error adding Flashcard to database"
            case 2:
                check_two = False
                sets = asl_2_units.query.with_entities(asl_2_units.unit_number).all()
                for set in sets:
                    if setNum == set.unit_number:
                        check_two = True
                if check_two == False:
                    newSet = asl_2_units(unit_number = setNum)
                    try:
                        db.session.add(newSet)
                        db.session.commit()
                    except:
                        return "error adding Set to database"
                check_two = False
                newFlashcard = asl_2_set(word = WordGIF, unit_number = setNum, gif_path = FilePath)
                try:
                    db.session.add(newFlashcard)
                    db.session.commit()
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(WordGIF)))
                    return render_template("flashcard_added.html"), {"Refresh": "2; url=/flashcard_add"}
                except:
                    return "error adding user to database"
            case 3:
                check_three = False
                sets = asl_3_units.query.with_entities(asl_3_units.unit_number).all()
                for set in sets:
                    if setNum == set.unit_number:
                        check_three = True
                if check_three == False:
                    newSet = asl_3_units(unit_number = setNum)
                    try:
                        db.session.add(newSet)
                        db.session.commit()
                    except:
                        return "error adding Set to database"
                check_three = False
                newFlashcard = asl_3_set(word = WordGIF, unit_number = setNum, gif_path = FilePath)
                try:
                    db.session.add(newFlashcard)
                    db.session.commit()
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(WordGIF)))
                    return render_template("flashcard_added.html"), {"Refresh": "2; url=/flashcard_add"}
                except:
                    return "error adding user to database"
            case 4:
                check_four = False
                sets = asl_4_units.query.with_entities(asl_4_units.unit_number).all()
                for set in sets.unit_number:
                    if setNum == set:
                        check_four = True
                if check_four == False:
                    newSet = asl_4_units(unit_number = setNum)
                    try:
                        db.session.add(newSet)
                        db.session.commit()
                    except:
                        return "error adding Set to database"
                check_four = False
                newFlashcard = asl_4_set(word = WordGIF, unit_number = setNum, gif_path = FilePath)
                try:
                    db.session.add(newFlashcard)
                    db.session.commit()
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(WordGIF)))
                    return render_template("flashcard_added.html"), {"Refresh": "2; url=/flashcard_add"}
                except:
                    return "error adding user to database"
    return render_template("flashcard_add.html", form=form)

@app.route('/flashcard_added', methods=["GET", "POST"])
def flashcard_added():
    return render_template("flashcard_added.html")
