from flask import Flask

app = Flask(__name__)

@app.route("/<string:new>")
def index(new):
    return new

if __name__ == "__main__":
    app.run()
