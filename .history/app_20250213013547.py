import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import login_user, login_required, logout_user, current_user
from models import Cocktail
from models import User as UsersCocktail
from extensions import db, login_manager, migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_debugtoolbar import DebugToolbarExtension
import requests
from ingredients import get_ingredient_rating
from forms import RegistrationForm, LoginForm
from sqlalchemy.sql import text
import re

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$"


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
uri = os.getenv('DATABASE_URL', 'postgresql://gaming_lab_psql_user:BpVA4tBlRHtP2njTyIxlmLSITAj34dsl@dpg-culvbrqn91rc739o61a0-a.oregon-postgres.render.com/gaming_lab_psql')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate.init_app(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_cocktail', methods=['GET', 'POST'])
@login_required
def create_cocktail():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data submitted"}), 400

            name = data.get('name', 'Unnamed Cocktail')
            cup = data.get('cup')
            capacity = data.get('capacity')
            ingredients = data.get('ingredients', [])
            color = data.get('color', '#FFFFFF')
            sweetness = data.get('sweetness', 0)
            bitterness = data.get('bitterness', 0)
            smoothness = data.get('smoothness', 0)
            strength = data.get('strength', 0)
            freshness = data.get('freshness', 0)
            enjoyment_rating = data.get('enjoyment_rating', 0)
            final_strength = data.get('final_strength', 0)

            if not cup or not capacity or not ingredients:
                return jsonify({"error": "Required fields are missing"}), 400

            new_cocktail = Cocktail(
                name=name,
                cup=cup,
                capacity=capacity,
                ingredients=ingredients,
                color=color,
                sweetness=sweetness,
                bitterness=bitterness,
                smoothness=smoothness,
                strength=strength,
                freshness=freshness,
                enjoyment_rating=enjoyment_rating,
                final_strength=final_strength,
                user_id=current_user.id
            )
            db.session.add(new_cocktail)
            db.session.commit()

            return redirect(url_for('cocktail_detail'))

    except Exception as e:
        app.logger.error(f"Error creating cocktail: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    ingredient_response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list')
    ingredients = []
    if ingredient_response.status_code == 200:
        ingredients = ingredient_response.json().get('drinks', [])
        ingredient_names = [ingredient['strIngredient1'] for ingredient in ingredients]

    return render_template('create_cocktail.html', ingredients=ingredient_names)

@app.route('/cocktail_detail/<int:cocktail_id>', methods=['GET'])
@login_required
def cocktail_detail_by_id(cocktail_id):
    cocktail = Cocktail.query.filter_by(id=cocktail_id, user_id=current_user.id).first()
    if not cocktail:
        flash("Cocktail not found or you are not authorized to view it.", "danger")
        return redirect(url_for('index'))

    return render_template('cocktail_detail.html', cocktails=[cocktail])



@app.route('/delete_cocktail/<int:cocktail_id>', methods=['POST'])
@login_required
def delete_cocktail(cocktail_id):
    cocktail = Cocktail.query.filter_by(id=cocktail_id, user_id=current_user.id).first()
    if not cocktail:
        return jsonify({"error": "Cocktail not found or you are not authorized to delete it."}), 404

    try:
        db.session.delete(cocktail)
        db.session.commit()
        return jsonify({"success": True, "message": "Cocktail deleted successfully."}), 200
    except Exception as e:
        app.logger.error(f"Error deleting cocktail: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500



def calculate_color_based_on_ingredients(ingredients, ounces):
    color_map = {
        "Light rum": "Transparent",
        "Bourbon": "Amber",
        "Vodka": "Transparent",
        "Gin": "Transparent",
         "Blended whiskey": "#7A5C3C",
    "Tequila": "#FFD700",
    "Sweet Vermouth": "#9B1C1C",
    "Apricot brandy": "#FFD700",
    "Triple sec": "#E5D97E",
    "Southern Comfort": "#7A5C3C",
    "Orange bitters": "#FFA500",
    "Brandy": "#7A5C3C",
    "Lemon vodka": "#F1E5AC",
    "Dry Vermouth": "#F1E5AC",
    "Dark rum": "#3E1F1A",
    "Amaretto": "#7A5C3C",
    "Tea": "#6B4F34",
    "Applejack": "#FFD700",
    "Champagne": "#FFFAE3",
    "Scotch": "#7A5C3C",
    "Coffee liqueur": "#3E1F1A",
    "Añejo rum": "#7A5C3C",
    "Bitters": "#6B4F34",
    "Kahlua": "#3E1F1A",
    "Dubonnet Rouge": "#9B1C1C",
    "Irish whiskey": "#7A5C3C",
    "Apple brandy": "#FFD700",
    "Carbonated water": "#D1D1D1",
    "Cherry brandy": "#9B1C1C",
    "Creme de Cacao": "#3E1F1A",
    "Port": "#9B1C1C",
    "Coffee brandy": "#6B4F34",
    "Red wine": "#9B1C1C",
    "Rum": "#F1E5AC",
    "Ricard": "#E5D97E",
    "Sherry": "#7A5C3C",
    "Cognac": "#7A5C3C",
    "Sloe gin": "#8B3B8C",
    "Strawberry schnapps": "#FF0000",
    "Apple cider": "#7A5C3C",
    "Lime juice": "#00FF00",
    "Lemon juice": "#FFFF00",
    "Cranberry juice": "#D32F2F",
    "Orange": "#FFA500",
    "Sugar": "#FFFFFF",
    "Milk": "#FFFFFF",
    "Lemonade": "#FFFF00",
    "Grapefruit juice": "#FF6347",
    "Apple juice": "#FFEB3B",
    "Pineapple juice": "#FFEB3B",
    "Ginger": "#DDB67D",
    "Strawberries": "#FF0000",
    "Cantaloupe": "#FFA500",
    "Berries": "#8A2BE2",
    "Grapes": "#8B0000",
    "Coconut milk": "#FFFACD",
    "Papaya": "#FF6347",
    "Agave syrup": "#D3B09C",
    "Almond milk": "#FFF5F3",
    "Honey": "#FFB900",
    "Pomegranate": "#800000",
    "Mango": "#FFB300",
    "Blueberry": "#0000FF",
    "Blue Curacao (non-alcoholic)": "#1E90FF",
    "Blue Raspberry Syrup": "#00BFFF",
    "Butterfly Pea Flower": "#6A5ACD",
    "Ginger Ale": "#D1E8E2",
    "Mint Syrup": "#98FB98",
    "Pineapple": "#FFE135",
    "Cucumber": "#7FFFD4",
    "Kiwi": "#8FBC8F"
    }

    final_color = "clear"
    ingredient_colors = []

    total_ounces = sum(float(oz) for oz in ounces)

    for ingredient, ounce in zip(ingredients, ounces):
        ingredient_color = color_map.get(ingredient, 'clear')
        ingredient_ratio = float(ounce) / total_ounces  

        if ingredient_color != 'clear':
            ingredient_colors.append((ingredient_color, ingredient_ratio))

    if ingredient_colors:
        final_color = max(set([color for color, _ in ingredient_colors]), key=lambda x: [color for color, _ in ingredient_colors].count)

    return final_color


def calculate_ratings(ingredients, ounces):
    final_ratings = {
        'Bitterness': 0,
        'Smoothness': 0,
        'Strength': 0
    }

    total_ounces = sum(float(oz) for oz in ounces)

    for ingredient, ounce in zip(ingredients, ounces):
        ratings = get_ingredient_rating(ingredient)
        if ratings:
            ingredient_ratio = float(ounce) / total_ounces  
            final_ratings['Bitterness'] += ratings['Bitterness'] * ingredient_ratio
            final_ratings['Smoothness'] += ratings['Smoothness'] * ingredient_ratio
            final_ratings['Strength'] += ratings['Strength'] * ingredient_ratio

    return final_ratings




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # ✅ Validate password format before checking credentials
        if not re.match(PASSWORD_REGEX, form.password.data):
            flash('❌ Invalid password format. Ensure it meets security requirements.', 'danger')
            return redirect(url_for('login'))

        # ✅ Check if user exists and password matches
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('✅ Welcome back, our bartender apprentice! Time to shake things up!', 'success')
            return redirect(url_for('index'))
        else:
            flash('❌ Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route('/cocktails', methods=['GET'])
@login_required
def cocktail_detail():
    """
    Displays a list of all the cocktails created by the logged-in user.
    """
    cocktails = Cocktail.query.filter_by(user_id=current_user.id).all()
    if not cocktails:
        flash("You have not created any cocktails yet.", "info")
    return render_template('cocktail_detail.html', cocktails=cocktails)

from sqlalchemy.sql import text

@app.route('/test-db')
def test_db():
    try:
        from models import db
        db.session.execute(text('SELECT 1'))  # Explicitly declare SQL as text
        return "Database connection is successful!"
    except Exception as e:
        return f"Database connection failed: {e}"




if __name__ == '__main__':
    app.run(debug=True)
# 🔹 Description:
# This Flask application serves as the backend for the Cocktail Lab web application,
# allowing users to register, log in, create and manage cocktails, and interact with the database.
#
# 🔹 Features:
# - User authentication (Registration, Login, Logout)
# - Password validation with strict security rules
# - Cocktail creation, deletion, and retrieval
# - Database connectivity and error handling
# - API endpoints for testing application health
#
# =============================================
# 🛠️ CONFIGURATION
# =============================================
#
# 1️⃣ **Environment Variables**
# - `SECRET_KEY`: Used for session security.
# - `DATABASE_URL`: PostgreSQL database connection URL.
# - `DEBUG_TB_INTERCEPT_REDIRECTS`: Prevents redirect interception by Flask Debug Toolbar.
#
# 2️⃣ **Libraries Used**
# - `Flask` → Web framework
# - `Flask-WTF` → Form validation
# - `Flask-Login` → User authentication
# - `SQLAlchemy` → ORM for database management
# - `Werkzeug` → Password hashing
# - `Requests` → API integration
# - `Flask-DebugToolbar` → Debugging support
#
# =============================================
# 🔗 ROUTES OVERVIEW
# =============================================
#
# 📌 **1. User Authentication**
# - `GET /register` → Displays registration form
# - `POST /register` → Creates a new user (Requires a strong password)
# - `GET /login` → Displays login form
# - `POST /login` → Logs in a user (Validates credentials)
# - `GET /logout` → Logs out the current user
#
# 📌 **2. Cocktail Management**
# - `GET /create_cocktail` → Displays the cocktail creation form
# - `POST /create_cocktail` → Creates a new cocktail
# - `GET /cocktail_detail/<int:cocktail_id>` → Shows details of a cocktail
# - `POST /delete_cocktail/<int:cocktail_id>` → Deletes a cocktail
#
# 📌 **3. Testing & Debugging**
# - `GET /test` → Checks if the Flask server is running
# - `GET /test-db` → Verifies the database connection
#
# =============================================
# 🔐 PASSWORD VALIDATION
# =============================================
# ✅ Password must be at least **10 characters long**
# ✅ Must contain **one uppercase letter**
# ✅ Must contain **one lowercase letter**
# ✅ Must contain **one number**
# ✅ Must contain **one special character** (@, $, !, %, *, ?, &)
#
# Regex Rule: 
# `r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$"`