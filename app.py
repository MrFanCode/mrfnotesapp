from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, ValidationError

"""

THIS PROJECT IS NOT DONE YET.
WILL BE COMPLETE THIS PROJECT SOON.

"""


app = Flask(__name__)
app.config["SECRET_KEY"] = "117d4b56faf1745201cbf95069437f4f"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"

# initializing sqlalchemy database
db = SQLAlchemy()
db.init_app(app)

# This is the form for sak the username when the user run this app at the first time. But...
# TODO: This functionality is not done yet.
class UserForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()], render_kw="{'placeholder':'Username'}")
    submit = SubmitField("Submit")

# This table will holding username.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column("username", db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.user}"


# Home page route
@app.route('/')
def home():
    return render_template("home.html", title="Home")


# Site that will display all the notes 
@app.route('/notes')
def notes():
    return render_template("notes.html", title="Notes")


# Add note site
@app.route('/add_note')
def add_note():
    pass


if __name__ == "__main__":
    app.run(debug=False) # Set debug to 'True' to get live changes when make some changes.

