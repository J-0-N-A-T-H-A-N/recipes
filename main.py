from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, SearchForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@db01:5432/website"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ############### #
# DATABASE TABLES #
# ############### #

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    pw_hash = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, name, email, pw_hash, role):
        self.name = name
        self.email = email
        self.pw_hash = pw_hash
        self.role = role

class Recipe(db.Model):
    __tablename__ = "recipes"
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(250), nullable=False)
    owner = db.Column(db.String(250), nullable=False)

    def __init__(self, recipe_name, owner):
        self.recipe_name = recipe_name
        self.owner = owner


# Uncomment to create tables
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("Email already exists. Login instead.")
            return redirect(url_for("login", logged_in=current_user.is_authenticated))
        else:
            new_user = User(
                name=form.name.data,
                email=form.email.data,
                pw_hash=generate_password_hash(form.password1.data, method='pbkdf2:sha256', salt_length=8),
                role="user"
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home", logged_in=current_user.is_authenticated))

    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/login', methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.pw_hash, password):
                login_user(user)
                print(user)
                print(current_user.name)
                print(current_user.id)
                return redirect(url_for("home", logged_in=current_user.is_authenticated))
            else:
                flash("Email not found or password incorrect, try again.")
        else:
            flash("Email not found or password incorrect, try again.")

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home', logged_in=current_user.is_authenticated))

@app.route('/search/')
def search():
    form = SearchForm()
    return render_template("search.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/myrecipes/')
def myrecipes():
    form = SearchForm()
    recipe_list = []
    my_recipes = db.session.query(Recipe).filter_by(owner=current_user.id).all()
    for recipe in my_recipes:
        recipe_list.append(recipe)
    print(recipe_list)
    return render_template("myrecipes.html", form=form, logged_in=current_user.is_authenticated, recipes=recipe_list)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
