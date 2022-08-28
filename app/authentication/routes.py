from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            ## ADD names here?
            #name = form.name.data
            #print(name) --> Name was showing as None when data entered
            email = form.email.data
            password = form.password.data
            print(email, password)

            # create User using class made from models.py
            user = User(email, password = password)

            # add new User to database
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created') # 'User-created' is used to talk to application
            return redirect(url_for('site.home')) # send user back to home page
        else:
            print("FAILURE")
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()  # take email data and check it against User class and query database, and pull back first one for that email
            # check to see if user is in database, and check to see if decrypted/unhashed password is correct
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in', 'auth-success') # 'auth-success' is used to talk to application
                return redirect(url_for('site.profile'))
            else:
                print("Wrong info")
                flash('You have entered in the incorrect information. Access denied.', 'auth-failed')
                return redirect(url_for('auth.signin')) ### missing from video
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))