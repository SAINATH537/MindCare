# src/app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from database.db_helper import DBHelper
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'e5b0b6ce3b7b2b3e8f2c9c5c4b6a7d9a2e3c4e5f6a7b8c9d'  # Replace with a strong secret key

def get_db():
    if 'db' not in g:
        g.db = DBHelper()
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.create_connection().close()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_db().get_user(username, password)
        if user:
            session['user_id'] = user[0]  # Store user ID in session
            session['username'] = user[1]  # Store username in session
            flash(f"User {username} logged in successfully.", 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        education = request.form['education']
        dob = request.form['dob']
        try:
            get_db().create_user(username, password, name, age, gender, education, dob)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = get_db().get_user_by_id(session['user_id'])
    if user is None:
        flash('User not found', 'error')
        return redirect(url_for('login'))

    user_data = {
        'username': user[1],
        'name': user[3],
        'age': user[4],
        'gender': user[5],
        'education': user[6],
        'dob': user[7]
    }
    return render_template('profile.html', user=user_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/mood-tracker', methods=['GET', 'POST'])
def mood_tracker():
    if request.method == 'POST':
        mood = request.form['mood']
        note = request.form['note']
        get_db().insert_mood(mood, note)
        flash('Mood saved successfully!', 'success')
        return redirect(url_for('mood_tracker'))
    return render_template('mood_tracker.html')

@app.route('/visualization')
def visualization():
    mood_data = get_db().get_mood_data()
    return render_template('visualization.html', mood_data=mood_data)

@app.route('/mindfulness')
def mindfulness():
    return render_template('mindfulness.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    app.run(debug=True)