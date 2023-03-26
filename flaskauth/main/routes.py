from flask import Blueprint, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models import Customer
from flask_login import login_required, current_user, login_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.first_name)


@main.route('/register')
def register():
    return render_template('index.html')


@main.route('/register', methods=['POST'])
def register_post():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    customer = Customer.query.filter_by(email=email).first()
    if customer:
        flash('Email address already exists')
        return redirect(url_for('main.register'))
        

    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password, method='sha256')
    )

    db.session.add(new_customer)
    db.session.commit()

    return redirect(url_for('main.login'))


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')    
    customer = Customer.query.filter_by(email=email).first() 
    if not customer or not check_password_hash(customer.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('main.login'))
    login_user(customer)
    return redirect(url_for('main.profile'))
