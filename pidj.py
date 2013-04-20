from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    #init_db()
    app.run()