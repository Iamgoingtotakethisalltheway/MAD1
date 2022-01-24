from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

# print("Successfully imported")

app = Flask(__name__)
app