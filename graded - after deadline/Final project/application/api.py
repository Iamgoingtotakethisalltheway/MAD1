import datetime
import re
from time import time
from urllib import response
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse, request

from application.database import db
from application.models import *
from application.validation import *

# ====================================================================================================================

# ========
# UserAPI           # "/v1/api/user", "/v1/api/user/<string:email>"
# ========

user_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "username": fields.String,
    "email": fields.String,
    "active": fields.Boolean
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("first_name")
create_user_parser.add_argument("last_name")
create_user_parser.add_argument("email")
create_user_parser.add_argument("username")
create_user_parser.add_argument("password")


update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument("first_name")
update_user_parser.add_argument("last_name")
update_user_parser.add_argument("email")
update_user_parser.add_argument("username")
update_user_parser.add_argument("password")

class UserAPI(Resource):            # "/v1/api/user", "/v1/api/user/<string:email>"
    @email_validator
    @marshal_with(user_fields)
    def get(self, email=None):
        # 'email_validator' decorator above validates email before processing
        # Following happens after email validation
        user = db.session.query(User).filter(User.email==email).first()
        if user:
            return user, 200
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")

    @email_validator
    @marshal_with(user_fields)
    def put(self, email):
        args = update_user_parser.parse_args()
        first_name = args.get("first_name", None)
        last_name = args.get("last_name", None)
        # email = args.get("email", None)
        # username = args.get("username", None)
        # password = args.get("password", None)

        # # Check if email exists
        # user = db.session.query(User).filter(User.email==email).first()
        # if user:
        #     raise BusinessValidationError(status_code=400, error_code="BE1006", error_message="Duplicate email")
        
        # Check if email exists
        user = db.session.query(User).filter(User.email==email).first()
        if user in [None, '']:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")


        user.first_name = first_name
        user.last_name = last_name
        # user.email = email
        
        db.session.add(user)
        db.session.commit()

        return user, 201

    @email_validator
    def delete(self, email):
        user = db.session.query(User).filter(User.email==email).first()
        if user in [None, '']:
            raise NotFoundError(status_code=404)
        db.session.delete(user)
        db.session.commit()
        return "", 200

    # def post(self):               # POST method doesnt make sense with email based login system. To be looked at later.
    #     args = create_user_parser.parse_args()
    #     first_name = args.get("first_name", None)
    #     last_name = args.get("last_name", None)
    #     email = args.get("email", None)
    #     username = args.get("username", None)
    #     password = args.get("password", None)

    #     if username in [None, '']:
    #         raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="username is required")

    #     if email in [None, '']:
    #         raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="email is required")

    #     if "@" in email:
    #         pass
    #     else:
    #         raise BusinessValidationError(status_code=400, error_code="BE1003", error_message="invalid email")
        
    #     user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()
    #     if user:
    #         raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Duplicate user")

    #     new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
    #     db.session.add(new_user)
    #     db.session.commit()

    #     return "", 201


# ====================================================================================================================

# ==========
# User2API              # "/v1/api/user2", "/v1/api/user2/<string:username>"
# ==========

class User2API(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        # user = User.query.filter_by(username=username).first()
        user = db.session.query(User).filter(User.username==username).first()
        if user:
            return user, 200
        else:
            raise NotFoundError(status_code=404)

# ====================================================================================================================

# ==========
# TrackerAPI            # "/v1/api/tracker", "/v1/api/tracker/<string:email>/<string:tracker_name>"
# ==========

# class Tracker(db.Model):
#     __tablename__ = "tracker"
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     tracker_name = db.Column(db.String, unique=True, nullable=False)
#     tracker_type = db.Column(db.String, nullable=False)
#     tracker_settings = db.Column(db.String)     # Problem with multiple choice
#     tracker_desc = db.Column(db.String)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

tracker_fields = {
    "id": fields.Integer,
    "tracker_name": fields.String,
    "tracker_type": fields.String,
    "tracker_settings": fields.String,
    "tracker_desc": fields.String,
    "user_id": fields.Integer
}

create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument("tracker_name")
create_tracker_parser.add_argument("tracker_type")
create_tracker_parser.add_argument("tracker_settings")
create_tracker_parser.add_argument("tracker_desc")
create_tracker_parser.add_argument("user_id", type=int)


update_tracker_parser = reqparse.RequestParser()
update_tracker_parser.add_argument("tracker_name")
# update_tracker_parser.add_argument("tracker_type")
# update_tracker_parser.add_argument("tracker_settings")
update_tracker_parser.add_argument("tracker_desc")
update_tracker_parser.add_argument("user_id", type=int)


class TrackerAPI(Resource):             # "/v1/api/tracker", "/v1/api/tracker/<string:email>/<string:tracker_name>"
    @marshal_with(tracker_fields)
    def get(self, email=None, tracker_name=None):
        # parser = reqparse.RequestParser()     # This reqparse method can also can be used
        # parser.add_argument('user_id')
        # args = parser.parse_args()
        # user_id = args.get('user_id', None)
        # user_id = request.args.get('user_id')

        # Validation before querying db (These funcions are defined in validation.py file)
        validate_email(email)
        validate_tracker_name(tracker_name)

        # db queries after validation
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            user_id = user.id
            tracker = db.session.query(Tracker).filter((Tracker.tracker_name == tracker_name) & (Tracker.user_id == user_id)).first()
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")
        if tracker:
            return tracker, 200
        else:
            raise NotFoundError(status_code=404, error_code="NF1002", error_message=f"No such tracker name associated with this user in the database.")


    @marshal_with(tracker_fields)
    def put(self, email=None, tracker_name=None):
        '''Only tracker name and description can be edited/updated.'''
        # Parse form data 
        args = update_tracker_parser.parse_args()
        new_tracker_name = args.get("tracker_name", None).lower()
        # tracker_type = args.get("tracker_type", None)
        # tracker_settings = args.get("tracker_settings", None)
        tracker_desc = args.get("tracker_desc", None).lower()
        # user_id = args.get("user_id", None)

        # Validate email, tracker name and parsed form data before db queries
        validate_email(email)
        validate_tracker_name(tracker_name)
        validate_tracker_name(new_tracker_name)

        # get user object from db to get user_id
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            user_id = user.id
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")

        # get tracker object from db
        tracker = db.session.query(Tracker).filter((Tracker.tracker_name == tracker_name) & (Tracker.user_id == user_id)).first()
        # if tacker exists, modify and commit
        if tracker in [None, '']:
            raise NotFoundError(status_code=404, error_code="NF1002", error_message=f"No such tracker name associated with this user in the database.")

        # If tracker_name is same as new tracker_name, 


        # Before update check if another tracker exists with the new tracker name 
        if tracker_name != new_tracker_name:
            tracker_nameclash = db.session.query(Tracker).filter((Tracker.tracker_name == new_tracker_name) & (Tracker.user_id == user_id)).first()
            if tracker_nameclash:
                raise BusinessValidationError(status_code=400, error_code="BE2006", error_message=f"Duplicate tracker. User has another tracker named '{new_tracker_name}'. Please choose a different name.")
            else:
                # Update tracker details and commit
                tracker.tracker_name = new_tracker_name.lower()
                tracker.tracker_desc = tracker_desc

                db.session.add(tracker)
                db.session.commit()

        return tracker, 201


    def delete(self, email=None, tracker_name=None):
        # user_id = request.args.get('user_id')

        # Validation before querying db (These funcions are defined in validation.py file)
        validate_email(email)
        validate_tracker_name(tracker_name)

        # db queries after validation
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            user_id = user.id
            tracker = db.session.query(Tracker).filter((Tracker.tracker_name == tracker_name) & (Tracker.user_id == user_id)).first()
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")

        if tracker in [None, '']:
            raise NotFoundError(status_code=404, error_code="NF1002", error_message=f"No such tracker name associated with this user in the database.")

        db.session.delete(tracker)
        db.session.commit()
        return "", 200

    def post(self):
        # Parse form data
        args = create_tracker_parser.parse_args()
        tracker_name = args.get("tracker_name", None).lower()
        tracker_type = args.get("tracker_type", None).lower()
        tracker_settings = args.get("tracker_settings", None).lower()
        tracker_desc = args.get("tracker_desc", None).lower()
        user_id = args.get("user_id", None)

        # Validate parsed data before db queries
        validate_tracker_name(tracker_name)
        validate_tracker_type(tracker_type)

        if tracker_type == "multiple choice":
            validate_tracker_settings(tracker_settings)

        # db queries after validation is successful
        tracker = db.session.query(Tracker).filter((Tracker.tracker_name == tracker_name.lower()) & (Tracker.user_id == user_id)).first()
        if tracker:
            raise BusinessValidationError(status_code=400, error_code="BE2006", error_message="Duplicate tracker")
        
        new_tracker = Tracker(tracker_name=tracker_name, tracker_type=tracker_type, tracker_settings=tracker_settings, tracker_desc=tracker_desc, user_id=user_id)
        db.session.add(new_tracker)
        db.session.commit()
        return "", 201

# ====================================================================================================================

# ==============
# TrackerListAPI            # "/v1/api/trackerlist/<string:user_email>"
# ==============

class TrackerListAPI(Resource):         # /v1/api/trackerlist/<string:user_email>
    @marshal_with(tracker_fields)
    def get(self, user_email):
        # Validate user_email before db queries
        validate_email(user_email)

        # db queries after validation is successful
        user = db.session.query(User).filter(User.email == user_email).first()
        if user:
            tracker_list = db.session.query(Tracker).filter(Tracker.user_id == user.id).all()
            return tracker_list, 200
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")

# ====================================================================================================================

# =======
# LogsAPI               # "/v1/api/log", "/v1/api/log/<string:log_id>"
# =======

# class Logs(db.Model):
#     __tablename__ = "logs"
#     log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)             # Do we need this field?
#     tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id", ondelete="CASCADE"))
#     timestamp = db.Column(db.DateTime, nullable=False)
#     # should be based on tracker type
#     value = db.Column(db.String, nullable=False)
#     note = db.Column(db.String)

log_fields = {
    "log_id": fields.Integer,
    "user_id": fields.Integer,
    "tracker_id": fields.Integer,
    "timestamp": fields.DateTime,
    "value": fields.String,
    "note": fields.String
}

create_log_parser = reqparse.RequestParser()
create_log_parser.add_argument("user_email")
create_log_parser.add_argument("tracker_name")
create_log_parser.add_argument("timestamp")
create_log_parser.add_argument("value")
create_log_parser.add_argument("note")

update_log_parser = reqparse.RequestParser()
update_log_parser.add_argument("user_email")
update_log_parser.add_argument("tracker_name")
update_log_parser.add_argument("timestamp")
update_log_parser.add_argument("value")
update_log_parser.add_argument("note")


class LogsAPI(Resource):            # "/v1/api/log", "/v1/api/log/<string:log_id>"
    @marshal_with(log_fields)
    def get(self, log_id=None):
        # Validate log_id before db queries - validate_integer_type function is defined in validation.py file.
        validate_integer_type(log_id)
        
        # db queries after validation is successful
        log = db.session.query(Logs).filter(Logs.log_id == log_id).first()
        # user_id = log.user_id
        # tracker_id = log.tracker_id
        # username = db.session.query(User).filter(User.id == user_id).first()
        # tracker_name = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
        if log:
            return log, 200
        else:
            raise NotFoundError(status_code=404, error_code="NF1003", error_message="ID not found in database")

    @marshal_with(log_fields)
    def put(self, log_id):          
        args = update_log_parser.parse_args()
        # user_email = args.get("user_email", None)
        # tracker_name = args.get("tracker_name", None)
        timestamp = args.get("timestamp", None)
        value = args.get("value", None)
        note = args.get("note", None)

        # Get the log by log ID after validating log id
        validate_integer_type(log_id)
        log = db.session.query(Logs).filter(Logs.log_id == log_id).first()

        # If log does not exist, throw an error
        if log in [None, '']:
            raise NotFoundError(status_code=404, error_code="NF1003", error_message="ID not found in database")

        # validate parsed form data before further db queries
        validate_timestamp(timestamp)
        
        # Check if value given is appropriate for the type of tracker
            # Get the tracker first
        tracker_id = log.tracker_id
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
            # Get tracker details to verify if value given is appropriate for the type of tracker
        tracker_type = tracker.tracker_type
        tracker_settings = tracker.tracker_settings
        validate_log_value(value, tracker_type, tracker_settings)

        # Convert timestamp string to datetime object
        timestamp = datetime.datetime.strptime(timestamp, "%d-%m-%Y %H:%M")

        # what if there is another log for same tracker 
        user_id = log.user_id
        all_logs = db.session.query(Logs).filter((Logs.user_id == user_id) & (Logs.tracker_id == tracker_id)).all()
        all_timestamps = [item.timestamp for item in all_logs]
        
        if timestamp == log.timestamp:
            log.value = value
            log.note = note
            db.session.add(log)
            db.session.commit()
            return log, 201
        else:  
            if timestamp in all_timestamps:
                raise BusinessValidationError(status_code=400, error_code="BE3005", error_message="Duplicate log")
            else:
                log.timestamp = timestamp
                log.value = value
                log.note = note
                db.session.add(log)
                db.session.commit()
            return log, 201


    def delete(self, log_id=None):
        # Validate log_id before db queries - validate_integer_type function is defined in validation.py file.
        validate_integer_type(log_id)
        
        # db queries after validation is successful
        log = db.session.query(Logs).filter(Logs.log_id == log_id).first()
        if log in [None, '']:
            raise NotFoundError(status_code=404, error_code="NF1003", error_message="ID not found in database")
        db.session.delete(log)
        db.session.commit()
        return "", 200

    def post(self):
        args = create_log_parser.parse_args()
        user_email = args.get("user_email", None).lower()
        tracker_name = args.get("tracker_name", None).lower()
        timestamp = args.get("timestamp", None).lower()
        value = args.get("value", None).lower()
        note = args.get("note", None).lower()

        # validate parsed form data before making db queries
        validate_email(user_email)
        validate_tracker_name(tracker_name)
        validate_timestamp(timestamp)

        # db queries after all validations are successful
        user = db.session.query(User).filter(User.email == user_email).first()
        if user:
            user_id = user.id
            tracker = db.session.query(Tracker).filter((Tracker.tracker_name == tracker_name) & (Tracker.user_id == user_id)).first()
            if tracker:
                tracker_id = tracker.id
            else:
                raise NotFoundError(status_code=404, error_code="NF1002", error_message=f"No such tracker name associated with this user in the database.")
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")

        # Convert timestamp string to datetime object
        timestamp = datetime.datetime.strptime(timestamp, "%d-%m-%Y %H:%M")

        # Check if there is another log with the same timestamp
        log = db.session.query(Logs).filter((Logs.user_id == user_id) & (Logs.tracker_id == tracker_id) & (Logs.timestamp == timestamp)).first()
        if log:
            raise BusinessValidationError(status_code=400, error_code="BE3005", error_message="Duplicate log")
        
        # Check if value given is appropriate for the type of tracker
        tracker_type = tracker.tracker_type
        tracker_settings = tracker.tracker_settings
        validate_log_value(value, tracker_type, tracker_settings)

        new_log = Logs(user_id=user_id, tracker_id=tracker_id, timestamp=timestamp, value=value, note=note)
        db.session.add(new_log)
        db.session.commit()
        return "", 201


# =================================================================================================================================================

# ========
# statsAPI                  # "/v1/api/stats/<string:email>/<string:tracker_name>"
# ========

class StatsAPI(Resource):               # "/v1/api/stats/<string:email>/<string:tracker_name>"
    @marshal_with(log_fields)
    def get(self, email=None, tracker_name=None):

        # Validate before making db queries
        validate_email(email)
        validate_tracker_name(tracker_name)

        # db queries after validation is successful
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            user_id = user.id
        else:
            raise NotFoundError(status_code=404, error_code="NF1001", error_message="User not found in database")

        try:    
            tracker = db.session.query(Tracker).filter((Tracker.tracker_name == tracker_name) & (Tracker.user_id == user_id)).first()
            tracker_id = tracker.id
            stats = db.session.query(Logs).filter((Logs.user_id == user_id) & (Logs.tracker_id == tracker_id)).order_by(Logs.timestamp.desc()).all()
            return stats, 200
        except:
            raise NotFoundError(status_code=404, error_code="NF1002", error_message=f"No such tracker name associated with this user in the database.")

# ======================================================================================================================================================