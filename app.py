from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, logout_user, LoginManager, current_user, login_required

db = SQLAlchemy()
bcrypt = Bcrypt()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'af64399870dabbbd9ba3af48c7c5fcbc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)
bcrypt.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Database Section
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Notes', backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.id}, {self.username}, {self.email}>"


class Notes(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.date_added}')"

#End Database Section


# Form Section

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=2,max=20)], render_kw={'placeholder':'Username'})
    email = StringField("Email", validators=[InputRequired(), Length(min=2,max=20), Email()], render_kw={'placeholder':'Email'})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=2,max=20)], render_kw={'placeholder':'Password'})
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=2,max=20), EqualTo('password')], render_kw={'placeholder':'Confirm Password'})
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("Username already exist. Please choose another one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Length(min=2,max=20), Email()], render_kw={'placeholder':'Email'})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=2,max=20)], render_kw={'placeholder':'Password'})
    submit = SubmitField("Login")


# Form End Section

# User After Logged in Forms

class AddNotes(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=2,max=35)], render_kw={'placeholder':'title'})
    note = TextAreaField("Note", validators=[InputRequired()], render_kw={'placeholder':'Note'})

    submit = SubmitField("Add note.")

# User After Logged in Forms End

@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account has been created for {form.username.data}.You can login now.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', title='Login', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    note = Notes()
    return render_template('dashboard.html', title='Dashboard', note=note)



@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

