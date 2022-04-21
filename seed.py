"""Seed file to make sample data for flask_feedback db"""

from models import User, db, Feedback
from app import app
from flask_bcrypt import Bcrypt

# crate all tables
db.drop_all()
db.create_all()

# if table isn't empty, empty it
User.query.delete()

# Add example user
user_info = {'username': "klobk23", 'password': "nocare23", "email": "someemail@gmail.com", "first_name": "Kain", "last_name": "Klob"}
user = User.register(user_info)

another_user = {'username': "otheruser", 'password': "badpass", "email": "someemail@gmail.com", "first_name": "Colton", "last_name": "Spahmer"}
user2 = User.register(another_user)

# Add Feedback example
feedback = Feedback(title="First title", content="This is some content for the feedback", username="klobk23")
feedback2 = Feedback(title="First title", content="This is some content for the feedback", username="otheruser")
feedback3 = Feedback(title="Second Title", content="This is some content for the feedback", username="klobk23")

db.session.add_all([feedback, feedback2, feedback3])
db.session.commit()