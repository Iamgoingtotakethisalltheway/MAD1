from enum import unique
from application.database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)     # Password management is optional
    active = db.Column(db.Boolean())

    roles = db.relationship("Role", secondary="roles_users", backref=db.backref("user", lazy="dynamic"))
    trackers = db.relationship("Tracker", cascade="all,delete", backref="user")
    # trackers = db.relationship("Tracker", backref="user", passive_deletes=True)

    '''Can consider adding a user profile page where user can update/add details to his profile'''

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True, nullable=False)

class Tracker(db.Model):
    __tablename__ = "tracker"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_name = db.Column(db.String, nullable=False)
    tracker_type = db.Column(db.String, nullable=False)
    tracker_settings = db.Column(db.String)     # Problem with multiple choice
    tracker_desc = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    logs = db.relationship("Logs", cascade="all,delete", backref="tracker")
    # user = db.relationship("User", backref=backref("tracker", passive_deletes=True))

# class UserTrackers(db.Model):
#     __tablename__ = "user_trackers"
#     # ut_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
#     tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'), primary_key=True, nullable=False)

class Logs(db.Model):
    __tablename__ = "logs"
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer)             # Do we need this field?
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"))
    timestamp = db.Column(db.DateTime, nullable=False)
    # should be based on tracker type
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String)
