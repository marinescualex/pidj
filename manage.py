from flask import Flask, current_app
from flask.ext.script import Manager

app = Flask(__name__)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()