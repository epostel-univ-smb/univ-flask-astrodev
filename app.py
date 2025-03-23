from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'your_secret_key'

# Charger les utilisateurs à partir du fichier CSV
def load_users():
    try:
        users = pd.read_csv('users.csv')
        return users.set_index('email').to_dict('index')
    except FileNotFoundError:
        return {}

# Page d'accueil
@app.route('/')
def index():
    return render_template('base.html')

# Inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return "Les mots de passe ne correspondent pas", 400
        
        users = load_users()
        if email in users:
            return "Email déjà utilisé", 400
        
        new_user = pd.DataFrame({
            'email': [email],
            'name': [name],
            'password': [generate_password_hash(password)]
        })
        
        try:
            existing_users = pd.read_csv('users.csv')
            combined = pd.concat([existing_users, new_user])
            combined.to_csv('users.csv', index=False)
        except FileNotFoundError:
            new_user.to_csv('users.csv', index=False)
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        users = load_users()
        if email not in users:
            return "Email inconnu", 400
        
        user = users[email]
        if not check_password_hash(user['password'], password):
            return "Mot de passe incorrect", 400
        
        # Simuler une session pour cet exemple
        # Dans une application réelle, utilisez Flask-Login pour gérer les sessions
        return redirect(url_for('appareil_photo'))
    
    return render_template('login.html')

# Routes pour les catégories
@app.route('/appareil_photo')
def appareil_photo():
    return render_template('appareil_photo.html')

@app.route('/photographies')
def photographies():
    return render_template('photographies.html')

@app.route('/telescopes')
def telescopes():
    return render_template('telescopes.html')

if __name__ == '__main__':
    app.run(debug=True)
