from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, UserMixin

auth = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, email):
        self.id = email 
        self.email = email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        from .models import Admin
        admin = Admin.query.first()

        if admin and admin.email == email and password == '1234567':
            login_user(admin, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Please check your email and password.', category='error')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))