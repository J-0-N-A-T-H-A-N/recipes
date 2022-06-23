from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, URL, NumberRange


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Re-enter password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    search = StringField("Enter Search Keywords", validators=[DataRequired()])
    submit = SubmitField("Search")


class AddRecipe(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired()])
    servings = IntegerField("Number of Servings", validators=[DataRequired(), NumberRange(min=1)])
    course = SelectField("Course", choices=["", "Starter", "Main", "Dessert"])
    submit = SubmitField("Add")
