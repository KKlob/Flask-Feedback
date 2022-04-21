"""flask-feedback application"""

from flask import Flask, request, render_template, redirect, flash, session, get_flashed_messages
from models import db, connect_db, User, Feedback
from secrets import database, app_secret_key
from forms import AddUserForm, LoginUserForm, AddFeedbackForm


# Config app stuff
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = app_secret_key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# connect db to app and create all tables
connect_db(app)

# all routes below

@app.route('/')
def redirect_to_register_page():
    """Simply redirects to register page"""
    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user_page():
    """User Add form, handle adding"""

    if session.get('user'):
        flash("You're already logged in!")
        return redirect(f'/users/{session.get("user")}')

    form = AddUserForm()
    msgs = get_flashed_messages()

    if form.validate_on_submit():
        user_info = User.collect_user_data(form)
        user = User.register(user_info)
        session['user'] = user.username
        flash(f'Success: User {user.username} logged in')
        return redirect(f'/users/{user.username}')
    else:
        return render_template('register_user_form.html', form=form, msgs=msgs, type_page="register")

@app.route('/login', methods=["GET", "POST"])
def login_user_page():
    """User login page, handle authentication"""

    if session.get('user'):
        flash("You're already logged in!")
        return redirect(f'/users/{session.get("user")}')

    form = LoginUserForm()
    msgs = get_flashed_messages()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['user'] = user.username
            flash(f'Success: User {user.username} logged in')
            return redirect(f'/users/{user.username}')
        else:
            flash(f'Error: Incorect credentials. Please try again')
            return redirect('/login')
    else:
        return render_template('register_user_form.html', form=form, type_page="login", msgs=msgs)


@app.route('/users/<username>')
def user_info_page(username):
    """User info page"""

    msgs = get_flashed_messages()

    if session.get('user'):
        if session.get('user') == username:
            user = User.query.filter_by(username=username).first()
            return render_template('user_info_page.html', user=user, msgs=msgs)
        else:
            flash(f'Error: You can only access your own user page!')
            return redirect(f'/users/{session.get("user")}')
    else:
        flash(f'Error: You must be logged in to view that page!')
        return redirect('/register')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_user_feedback(username):
    """Add feedback for user; handles submitted feedback form"""

    msgs = get_flashed_messages()
    form = AddFeedbackForm()

    if session.get('user'):
        if session.get('user') == username:
            if form.validate_on_submit():
                feedback_info = Feedback.collect_form_info(form)
                feedback = Feedback.add_feedback(feedback_info, username)
                flash(f'Success: Feedback "{feedback.title}" was added!')
                return redirect(f'/users/{username}')
            else:
                return render_template('feedback_form.html', msgs=msgs, form=form, type_page="add")
        else:
            flash(f'Error: You can only add feedback for your own user!')
            return redirect(f'/users/{session.get("user")}')
    else:
        flash(f'Error: You must be logged in to view that!')
        return redirect(f'/register')
        
@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Update feedback form; handles form submit to update feedback"""

    msgs = get_flashed_messages()
    feedback = Feedback.query.get(feedback_id)
    form = AddFeedbackForm(obj=feedback)

    if session.get('user'):
        if session.get('user') == feedback.username:
            if form.validate_on_submit():
                feedback_info = Feedback.collect_form_info(form)
                updated_feedback = Feedback.update_feedback(feedback_info, feedback)
                flash(f'Success: Feedback "{updated_feedback.title}" has been updated!')
                return redirect(f'/users/{updated_feedback.username}')
            else:
                return render_template('feedback_form.html', msgs=msgs, form=form, type_page="edit")
        else:
            flash(f'Error: You can only edit feedback for your own user!')
            return redirect(f'/users/{session.get("user")}')
    else:
        flash(f'Error: You must be logged in to view that!')
        return redirect('/register')

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback"""

    feedback = Feedback.query.get(feedback_id)

    if session.get('user'):
        if session.get('user') == feedback.username:
            db.session.delete(feedback)
            db.session.commit()
            flash(f'Success: Feedback "{feedback.title}" has been deleted.')
            return redirect(f'/users/{session.get("user")}')
        else:
            flash(f'Error: You can only delete your own feedback!')
            return redirect(f'/users/{session.get("user")}')
    else:
        flash(f'Error: You must be logged in to access that!')
        return redirect('/register')

@app.route('/logout')
def logout():
    """Log user out and redirect"""
    user = session.get('user')
    session.clear()
    flash(f'Success: User {user} has been logged out')
    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete user"""

    if session.get('user'):
        if session.get('user') == username:
            user = User.query.filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
            session.clear()
            flash(f'Success: User {user.username} has been deleted')
            return redirect('/register')
        else:
            flash(f'Error: You can only delete your own user!')
            return redirect(f'/users/{session.get("user")}')
    else:
        flash(f'Error: You must be logged in to access that!')
        return redirect('/register')