from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #Ensure passwords are not stored as plain text. Uses a hash function.
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')

        user = User.query.filter_by(userName=userName).first()  #filter all of the users with a certain UserID.
        print('USER: ', user)
        
        if user:  #If we found an user.
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember = True)
                return redirect(url_for('views.home')) #When a user is logged in redirects to homepage.
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.',category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        userName = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')
        elif len(email) < 4:
            flash('email must be greater than 3 characters.', category='error')
        elif len(userName) < 2:
            flash('userName must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be atleast 6 characters long', category='error')
        else:
            new_user = User(email=email, userName=userName, password=generate_password_hash(password1,method='sha256'))  # sha256 hashing algorithm used for the hash func, for the password
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) #When a user is created redirect the user to the home page.
            

    return render_template("sign_up.html", user=current_user)

