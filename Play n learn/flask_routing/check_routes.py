from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to home page!</h1>"

@app.route("/user")
def user():
    return "<h1>I am a new user!</h1>"

@app.route("/admin/")
def admin():
    return "<h1>I am the admin for this site!</h1>"

if __name__ == "__main__":
    app.run()
