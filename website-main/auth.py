#this module handles the routes login page(see views.py for other routes)
#Blueprint member allows for organizing the application into smaller re-usable parts
#blueprints need to be registered, see __init__.py
#request allows to input data from user, flash allows for "flashing" data to user
#for flashing data the base.html has to be updated

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__) 


@auth.route("login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfuly!", category = "success")
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again", category = "error")
        else:
            flash("Email does not exist.", category = "error")
    
    return render_template("login.html", user = current_user) 






@auth.route("logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))




@auth.route("sign-up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email = email).first()                  #could this be done easier if I used composite primary keys to include email?
        if user:
            flash("Email already exists.", category = "error")
            return render_template("sign_up.html", user = current_user)              #if user already exists return to sign up page

        #check for all errors in submission
        error_list = []       
        if len(email) < 4:
            error_list.append("Email must be greater than 3 characters.")
            
        if len(first_name) < 2:
            error_list.append("First name must be greater than 1 character.")
            
        if (password1 != password2) or (not password1):         #still want to print this if they entered no pw
            error_list.append("Passwords must match.")
            
        if len(password1) < 6:
            error_list.append("Password must be greater than 6 characters.")

        if len(error_list):
            for error in error_list:
                flash(error, category = "error")
        else:
            new_user = User(email = email, first_name = first_name, password =  generate_password_hash(password1, method = "scrypt"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash("Account created succesfully!", category = "success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user = current_user) 