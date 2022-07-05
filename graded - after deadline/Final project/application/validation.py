from unittest import result
from werkzeug.exceptions import HTTPException
from flask import make_response
import json
import re

class NotFoundError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)

# Validators for User fields
def validate_email(email):
    if email == None or email.strip() == "":
        raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="User email is required")
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="User email is not valid")

# Validators for Tracker fields
def validate_tracker_name(tracker_name):
    if tracker_name == None or tracker_name.strip() == "":
        raise BusinessValidationError(status_code=400, error_code="BE2001", error_message="Tracker name is required")
    match = re.match("^[^0-9!@#$%^*()_+-=~`|\?>,.;:'\s]+$", tracker_name)
    if not match:
        raise BusinessValidationError(status_code=400, error_code="BE2002", error_message="Tracker name is not valid. Numbers and special characters not alowed in tracker name.")

def validate_tracker_type(tracker_type):
    if tracker_type == None or tracker_type.strip() == "":
        raise BusinessValidationError(status_code=400, error_code="BE2003", error_message="Tracker type is required")
    match = re.match("^[^0-9!@#$%^*()_+-=~`|\?>,.;:']+$", tracker_type)
    if not match:
        raise BusinessValidationError(status_code=400, error_code="BE2004", error_message="Tracker type is not valid. Numbers and special characters not alowed in tracker type.")
    if tracker_type.lower() not in ["numerical", "multiple choice", "boolean", "time duration"]:
        raise BusinessValidationError(status_code=400, error_code="BE2005", error_message=f"Tracker type is not valid. Tracker type can only be 'numerical', 'multipe choice', 'boolean' or 'time duration'.")

def validate_tracker_settings(tracker_settings):
    if tracker_settings == None or tracker_settings.strip() == "":
        raise BusinessValidationError(status_code=400, error_code="BE2007", error_message="Tracker settings required for tracker type 'multiple choice")
    match = re.match("^[^\s,]+(,[^\s,]+)+$", tracker_settings)
    if not match:
        raise BusinessValidationError(status_code=400, error_code="BE2008", error_message="Tracker settings is not valid. Comma separated values (without spaces) expected.")

# Validators for Log fields (This just checks if the given entry is a number, so can be used for any integer field)
def validate_integer_type(id):
    if id == None:
        raise BusinessValidationError(status_code=400, error_code="BE3001", error_message="ID is required")
    try :
        int(id)
    except ValueError:
        raise BusinessValidationError(status_code=400, error_code="BE3002", error_message="ID is not valid. ID should be an integer.")

    # match = re.match("^[0-9]+$", id)
    # if not match:
    #     raise BusinessValidationError(status_code=400, error_code="BE3002", error_message="ID is not valid. ID should be an integer.")

def validate_timestamp(timestamp):
    if timestamp == None or timestamp.strip() == "":
        raise BusinessValidationError(status_code=400, error_code="BE3003", error_message="Timestamp is required")
    match = re.match("^[0-3][0-9]-[0-1][0-9]-[0-9]{4} [0-9]{2}:[0-9]{2}$", timestamp)
    if not match:
        raise BusinessValidationError(status_code=400, error_code="BE3004", error_message="Timestamp is not valid. String of the format '%d-%m-%Y %H:%M' or 'dd-mm-yyyy hh:mm' is expected.")

def validate_log_value(value, tracker_type, tracker_settings):
    if tracker_type == "numerical" or tracker_type == "time duration":
        try :
            float(value)
        except ValueError:
            raise BusinessValidationError(status_code=400, error_code="BE3006", error_message="Log value is not valid for this tracker type.")
    if tracker_type == "multiple choice":
        tracker_settings = tracker_settings.split(",")
        if not value in tracker_settings:
            raise BusinessValidationError(status_code=400, error_code="BE3006", error_message="Log value is not valid for this tracker type.")
    if tracker_type == "boolean":
        if not value in ["yes", "no"]:
            raise BusinessValidationError(status_code=400, error_code="BE3006", error_message="Log value is not valid for this tracker type.")



# Decorators (Used for demonstration purposes in UserAPI GET and DELETE methods)
def email_validator(func):
    def wrapper(self, email=None):
        if email == None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="User email is required")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="User email is not valid")
        function = func(self, email)
        return function
    return wrapper