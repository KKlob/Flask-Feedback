""" Models for flask-feedback"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                        nullable=False,
                        primary_key=True)
    password = db.Column(db.Text,
                        nullable=False)
    email = db.Column(db.String(50),
                        nullable=False)
    first_name = db.Column(db.String(30),
                        nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)
    feedback = db.relationship('Feedback', backref='users')

    @classmethod
    def collect_user_data(cls, form):
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user_info = {'username':username, 'password':password, 'email':email, 'first_name':first_name, 'last_name':last_name}
        return user_info


    @classmethod
    def register(cls, user_info):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(user_info['password']).decode('utf-8')
        user = cls(username=user_info['username'], password=hashed, email=user_info['email'], first_name=user_info['first_name'], last_name=user_info['last_name'])
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct
            Return User if valid; else return False
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    
class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                    nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String(),
                        db.ForeignKey('users.username', ondelete='CASCADE'))

    @classmethod
    def collect_form_info(cls, form):
        title = form.title.data
        content = form.content.data
        feedback_info = {'title': title, 'content': content}
        return feedback_info

    @classmethod
    def add_feedback(cls, feedback_info, username):
        feedback = Feedback(title=feedback_info['title'], content=feedback_info['content'], username=username)
        db.session.add(feedback)
        db.session.commit()
        return feedback

    @classmethod
    def update_feedback(cls, feedback_info, feedback):
        feedback.title = feedback_info['title']
        feedback.content = feedback_info['content']
        db.session.add(feedback)
        db.session.commit()
        return feedback