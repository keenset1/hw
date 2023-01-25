from flask import render_template, request, redirect,url_for,flash
from flask_login import login_user,logout_user,current_user
from flask import User
from .form import signupform, loginform 
from .import authentification
from models import db



@authentification.route('/signup', methods = ['GET','POST'])
def signup():
    form = signupform()
    if form.validate_on_submit():
        User = User(first_name=form.first_name=data,
                    last_name=form.last_name=data,
                    email = form.email.data,
                    password = form.password.data
        )
        db.session.add(User)
        db.session.commit()
        return redirect(url_for('authentification.login'))
    return render_template('signup.html',form=form)



@authentification.route('/login', methods = ['GET','POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        User = User.query.filter_by(email=form.email.data).first() 
        if User and User.check_password(form.password.data):
            login_user(User)
            return redirect(url_for('main.home'))
       
    return render_template('login.html',form=form)


@authentification.route('/logout', methods = ['GET' 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))   


