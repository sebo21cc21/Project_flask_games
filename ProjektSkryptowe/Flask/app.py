from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from kolkokrzyzyk import *

app = Flask(__name__)

#logowanie 
db = SQLAlchemy(app) #instancja bazy danych
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #łączy naszą bazę danych
app.config['SECRET_KEY'] = 'faksjhkajshfuD(#!*)(*@AKJSD*#@()#' #zabezpieczenie ciasteczek

#menadzer logowania
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#bierze id od użytkownika i ładuje go
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Klasa posiadająca dane uzytkownika
    id- identyfikator użytkownika (int, klucz główny w bazie danych), 
    username- nazwa użytkownika(40 znaków, musi być zawarte i unikalne), 
    password- hasło (40 znaków, musi być podane)
    w bazie zobaczymy poprzez komendę sqlite3 database.db -> select * from user;
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)


class Register(FlaskForm):
    """
    Klasa tworząca rejestracje użytkownika, jego zasoby pamiętane są w datasecie
    username- nazwa użytkownika (5- 25 znaków, musi być wprowadzone), 
    password- hasło (8-25 znaków, musi być wprowadzone)
    submit- przycisk zatwierdzający wprowadzone dane

    metoda validate_username: sprawdza czy istnieje w bazie danych czy istnieje użytkownik, 
    jeśli tak podnosi się wyjątek, jeśli nie przeprowadzona jest pozytywnie rejestracja

    """
    username = StringField(validators=[InputRequired(), Length(min=5, max=25)], render_kw={"placeholder": "Nazwa użytkownika"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=25)], render_kw={"placeholder": "Hasło"})
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError('Użytkownik istnieje. Wprowadź inną nazwę')


class Login(FlaskForm):
    """
    Klasa tworząca logowanie, jego zasoby pamiętane są w datasecie
    username- nazwa użytkownika (5- 25 znaków, musi być wprowadzone), 
    password- hasło (8-25 znaków, musi być wprowadzone)
    submit- przycisk zatwierdzający wprowadzone dane
    """
    username = StringField(validators=[InputRequired(), Length(min=5, max=25)], render_kw={"placeholder": "Nazwa uzytkownika"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=25)], render_kw={"placeholder": "Hasło"})
    submit = SubmitField('Zaloguj się')

"""
Routy do danej strony- w przeglądarcie wpisujemy poprzez
http://127.0.0.1:5000/ *EVENTLIST*
"""
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Kiedy logowanie zostanie pomyslnie wykonane, sprawdzamy czy User jest w bazie danych
    sprawdzamy czy hasło wprowadzone i te z bazy danych jest identyczne
    logujemy usera i przekierowujemy go do strony głównej
    """
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Kiedy rejestracja zostanie pomyslnie wykonana, następuje zhaszowanie hasła,
    nie widzimy go podczas wpisywania, tworzymy potem nowego Usera,
    uzupełniamy bazę danych i przekierowujemy Usera do logowania
    """
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

@app.route('/kalkulator')
@login_required
def kalkulator():
    return render_template('kalkulator.html')

@app.route('/kolkokrzyzyk')
@login_required
def kolkokrzyzyk():

    return render_template('kolkokrzyzyk.html')

@app.route('/memory')
@login_required
def memory():
    return render_template('memory.html')

@app.route('/pietnastka')
@login_required
def pietnastka():
    return render_template('pietnastka.html')

@app.route('/pingpong')
@login_required
def pingpong():
    return render_template('pingpong.html')


if __name__ == "__main__":
    app.run(debug=True)