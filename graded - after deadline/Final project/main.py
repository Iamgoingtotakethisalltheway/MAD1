import os
from flask import Flask
from flask_restful import Resource, Api
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    # get and set environment: Local dev or production
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)                                                              # Needs flask_restful
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)     # Needs flask_security
    security = Security(app, user_datastore)                                    # Needs flask_security
    app.app_context().push()
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

# Import all the APIs and register the resources
from application.api import *
api.add_resource(UserAPI, "/v1/api/user", "/v1/api/user/<string:email>")
api.add_resource(User2API, "/v1/api/user2", "/v1/api/user2/<string:username>")
api.add_resource(TrackerAPI, "/v1/api/tracker", "/v1/api/tracker/<string:email>/<string:tracker_name>")
api.add_resource(TrackerListAPI, "/v1/api/trackerlist/<string:user_email>")
api.add_resource(LogsAPI, "/v1/api/log", "/v1/api/log/<string:log_id>")
api.add_resource(StatsAPI, "/v1/api/stats/<string:email>/<string:tracker_name>")

# Error handling

@app.errorhandler(404)
def page_not_found(e):
    # Note that we set the 404 status explicitly
    return render_template("404.html"), 404

@app.errorhandler(403)
def not_allowed(e):
    # Note that we set the 403 status explicitly
    return render_template("403.html"), 403

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)