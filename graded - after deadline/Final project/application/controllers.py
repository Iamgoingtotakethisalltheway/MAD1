from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import current_app as app
from flask_security import login_required, roles_required, roles_accepted
# from flask_login import login_required
from requests import get, put, post, delete
import json
import datetime
import os
from application.graphs import *
from application.validation import *


# # Testing
# @app.route("/testing/")
# # @login_required
# def testing():
#     return render_template("layouts/navbar.html")

# Home page - index.html
base_url = "http://127.0.0.1:8080"
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Dashboard
@app.route("/dashboard/", methods=["GET"])
@app.route("/dashboard/<string:user_email>", methods=["GET"])
@login_required
# @roles_accepted("user", "admin")
def dashboard(user_email=None):
    tracker_list = get(f"{base_url}" + f"/v1/api/trackerlist/{user_email}")
    status_code = tracker_list.status_code
    if status_code == 200:
        try:
            tracker_list = tracker_list.json()
        except:
            pass
        for tracker in tracker_list:
            tracker_name = tracker["tracker_name"]
            logs = get(f"{base_url}" + f"/v1/api/stats/{user_email}/{tracker_name}").json()
            if logs != []:
                last_log = logs[0]
                # print(last_log)
                log_dt = last_log["timestamp"][0:-9]
                log_dt = datetime.datetime.strptime(log_dt, '%a, %d %b %Y %H:%M')
                log_dt = log_dt.strftime("%d-%m-%Y at %H:%M")
                tracker["last_log"] = log_dt
                tracker["last_value"] = last_log["value"]
                # print(last_log["timestamp"])
            else:
                last_log = None
                tracker["last_log"] = None
                tracker["last_value"] = None
        return render_template("dashboard.html", tracker_list=tracker_list)
    else:
        api_json_response = tracker_list.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)


# Log an event
@app.route("/logevent/<string:user_email>/<string:tracker_name>", methods=["GET", "POST"])
@login_required
def logevent(user_email=None, tracker_name=None):
    if request.method == "GET":
        user = get(f"{base_url}" + f"/v1/api/user/{user_email}")
        if user.status_code == 200:
            user = user.json()
            tracker = get(f"{base_url}" + f"/v1/api/tracker/{user_email}/{tracker_name}")
            if tracker.status_code == 200:
                tracker = tracker.json()
                choices = []
                if tracker["tracker_settings"]:
                    choices = [choice.strip() for choice in tracker["tracker_settings"].split(",")]
                if user["first_name"] != None:
                    name = user["first_name"]
                else:
                    name = user_email.split("@")[0]
                dt = datetime.datetime.now()
                dt = dt.strftime("%d-%m-%Y %H:%M")
                return render_template("log_event_form.html", name=name, dt=dt, user_email=user_email, tracker=tracker, tracker_name=tracker_name, choices=choices)
            else:
                api_json_response = tracker.json()
                return render_template("error_page_generic.html", api_json_response=api_json_response)
        else:
            api_json_response = user.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)

    if request.method == "POST":
        form_data = request.form.to_dict()     # Will contain only timestamp, value, note
        # form_data = dict()
        # form_data["timetamp"] = request.form.get("timestamp")
        # form_data["value"] = request.form.get("value")
        # form_data["note"] = request.form.get("note")
        form_data["user_email"] = user_email
        form_data["tracker_name"] = tracker_name
        # print(form_data["timestamp"])
        response = post(f"{base_url}" + f"/v1/api/log", data=form_data)
        if response.status_code == 201:
            return redirect(url_for("dashboard", user_email=user_email))
        else:
            api_json_response = response.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)


# View tracker stats
@app.route("/trackerstats/<string:user_email>/<string:tracker_name>", methods=["GET", "POST"])
@login_required
def tracker_stats(user_email, tracker_name):
    tracker_stats = get(f"{base_url}" + f"/v1/api/stats/{user_email}/{tracker_name}")
    if tracker_stats.status_code == 200:
        tracker_stats = tracker_stats.json()
        if os.path.exists("./static/graph.png"):
            os.remove("./static/graph.png")
        if tracker_stats:
            try:
                line_plot(tracker_stats)        # Imported from application.graphs moddule. Saves an image named 'graph.png' in same folder.
            except:
                pie_chart(tracker_stats)
        return render_template("stats.html", tracker_stats=tracker_stats, user_email=user_email, tracker_name=tracker_name)
    else:
        api_json_response = tracker_stats.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)

# Select tracker type before actually creating a tracker
@app.route("/select/trackertype/<string:user_email>", methods=["GET", "POST"])
@login_required
def select_tracker_type(user_email):
    user = get(f"{base_url}" + f"/v1/api/user/{user_email}")
    if user.status_code == 200:
        user = user.json()
        if user["first_name"] != None:
            name = user["first_name"]
        else:
            name = user_email.split("@")[0]
    else:
        api_json_response = user.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)

    if request.method == "GET":
        tracker_types = ["Numerical", "Multiple Choice", "Time Duration", "Boolean"]
        return render_template("tracker_type.html", name=name, user_email=user_email, tracker_types=tracker_types)

    if request.method == "POST":
        form_data = request.form.to_dict()     # Will contain only timestamp, value, note
        if form_data == {}:
            return redirect(url_for("select_tracker_type", user_email=user_email))
        tracker_type = form_data["tracker_type"].lower()
        # return render_template("create_tracker_form.html", name=name, user_email=user_email, tracker_type=tracker_type)
        return redirect(url_for("create_tracker", user_email=user_email, tracker_type=tracker_type))


# Create a tracker (after selecting tracker type in previous page)
@app.route("/create/tracker/<string:user_email>", methods=["GET", "POST"])
@login_required
def create_tracker(user_email):
    tracker_type = request.args.get("tracker_type")
    user = get(f"{base_url}" + f"/v1/api/user/{user_email}")
    if user.status_code == 200:
        user = user.json()
        if user["first_name"] != None:
            name = user["first_name"]
        else:
            name = user_email.split("@")[0]
    else:
        api_json_response = user.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)

    if request.method == "GET":
        return render_template("create_tracker_form.html", name=name, user_email=user_email, tracker_type=tracker_type)

    if request.method == "POST":
        form_data = request.form.to_dict()
        form_data["tracker_type"] = tracker_type
        user_id = user["id"]
        form_data["user_id"] = user_id
        if "tracker_settings" not in form_data.keys():
            form_data["tracker_settings"] = ""
        # print(form_data)
        response = post(f"{base_url}" + f"/v1/api/tracker", data=form_data)
        if response.status_code == 201:
            return redirect(url_for("dashboard", user_email=user_email))
        else:
            api_json_response = response.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)



# Edit/update a tracker
@app.route("/update/tracker/<string:user_email>/<string:tracker_name>", methods=["GET", "POST"])
@login_required
def update_tracker(user_email, tracker_name):
    user = get(f"{base_url}" + f"/v1/api/user/{user_email}")
    if user.status_code == 200:
        user = user.json()
        if user["first_name"] != None:
            name = user["first_name"]
        else:
            name = user_email.split("@")[0]
    else:
        api_json_response = user.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)

    if request.method == "GET":
        tracker = get(f"{base_url}" + f"/v1/api/tracker/{user_email}/{tracker_name}")
        if tracker.status_code == 200:
            tracker = tracker.json()
            return render_template("update_tracker_form.html", name=name, tracker=tracker, user_email=user_email, tracker_name=tracker_name)
        else:
            api_json_response = tracker.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)

    if request.method == "POST":
        form_data = request.form.to_dict()
        response = put(f"{base_url}"+ f"/v1/api/tracker/{user_email}/{tracker_name}", data=form_data)
        if response.status_code == 201:
            return redirect(url_for("dashboard", user_email=user_email))
        else:
            api_json_response = response.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)


# Delete a tracker
@app.route("/delete/tracker/<string:user_email>/<string:tracker_name>", methods=["GET"])
@login_required
def delete_tracker(user_email, tracker_name):
    response = delete(f"{base_url}"+ f"/v1/api/tracker/{user_email}/{tracker_name}")
    if response.status_code == 200:
        return redirect(url_for("dashboard", user_email=user_email))
    else:
        api_json_response = response.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)



# Edit/update a log
@app.route("/update/log/<string:user_email>/<int:log_id>/<string:tracker_name>", methods=["GET", "POST"])
@login_required
def update_log(user_email, log_id, tracker_name):
    # tracker_name = request.args.get("tracker_name")
    user = get(f"{base_url}" + f"/v1/api/user/{user_email}")
    if user.status_code == 200:
        user = user.json()
        if user["first_name"] != None:
            name = user["first_name"]
        else:
            name = user_email.split("@")[0]
    else:
        api_json_response = user.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)

    if request.method == "GET":
        log = get(f"{base_url}" + f"/v1/api/log/{log_id}")
        if log.status_code == 200:
            log = log.json()
            tracker = get(f"{base_url}" + f"/v1/api/tracker/{user_email}/{tracker_name}")
            if tracker.status_code == 200:
                tracker = tracker.json()
                choices = []
                if tracker["tracker_settings"]:
                    choices = [choice.strip() for choice in tracker["tracker_settings"].split(",")]
                dt = log["timestamp"][0:-9]
                dt = datetime.datetime.strptime(dt, '%a, %d %b %Y %H:%M')
                dt = dt.strftime("%d-%m-%Y %H:%M")
                # Need tracker details for using appropriate validation in update_log_form. See Create log controller for how tracker is passed.
                return render_template("update_log_form.html", name=name, dt=dt, log=log, user_email=user_email, tracker_name=tracker_name, tracker=tracker, choices=choices)
            else:
                api_json_response = tracker.json()
                return render_template("error_page_generic.html", api_json_response=api_json_response)
        else:
            api_json_response = log.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        # print(form_data)
        response = put(f"{base_url}"+ f"/v1/api/log/{log_id}", data=form_data)
        if response.status_code == 201:
            return redirect(url_for("tracker_stats", user_email=user_email, tracker_name=tracker_name))
        else:
            api_json_response = response.json()
            return render_template("error_page_generic.html", api_json_response=api_json_response)

# Delete a log
@app.route("/delete/log/<string:user_email>/<int:log_id>/<string:tracker_name>", methods=["GET"])
@login_required
def delete_log(user_email, log_id, tracker_name):
    response = delete(f"{base_url}" + f"/v1/api/log/{log_id}")
    if response.status_code == 200:
        return redirect(url_for("tracker_stats", user_email=user_email, tracker_name=tracker_name))
    else:
        api_json_response = response.json()
        return render_template("error_page_generic.html", api_json_response=api_json_response)



# EXTRA CODE

# To interact with database, use API endpoints (Example)
@app.route("/profile/<string:username>", methods=["GET"])
@login_required
def user_profile(username):
    user_profile = get(f"{base_url}" + f"/v1/api/user/{username}")
    try:
        user_profile = user_profile.json()
    except:
        pass
    return render_template("user_profile.html", profile=user_profile, username=username)