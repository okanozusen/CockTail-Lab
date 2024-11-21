from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class CocktailForm(FlaskForm):
    name = StringField('Cocktail Name', validators=[DataRequired()])

    category = SelectField('Select Category', choices=[
        ('alcohol', 'Alcohol'),
        ('non_alcohol', 'Non-Alcohol')
    ], validators=[DataRequired()])

    ingredients = SelectMultipleField('Ingredients', choices=[], coerce=str, validators=[DataRequired()])

    ingredient_ounces = StringField('Ingredient Amounts (oz)', validators=[DataRequired()])
    instructions = StringField('Instructions', validators=[DataRequired()])
    color = StringField('Color', render_kw={'readonly': True})

    submit = SubmitField('Create Cocktail')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')