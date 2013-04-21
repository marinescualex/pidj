import os
import re
import subprocess
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack, render_template, redirect, request#, session, g, url_for, abort, flash

DEBUG = True
SECRET_KEY = 'development key'
DATABASE = '/tmp/pidj.db'

app = Flask(__name__)
app.config.from_object(__name__)


path = os.path.expanduser(u'/media/usbstick') # Path where music is stored

#
# Creates the database tables
#

def init_db():

    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

        # Add music files to database

        make_tree(path)

#
# Opens a database connection if there isn't one yet
#

def get_db():

    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

#
# Used to check if mplayer is still running
#

def is_running(process):

    s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
    for x in s.stdout:

        if re.search(process, x):
            return True

    return False

#
#   Insert files in database
#

def make_tree(path):
    db = get_db()
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
                db.execute('insert into files (title, path) values (?, ?)', [name, path])
                db.commit()
    return tree

#
# Escape string for shell commands
#

def shellquotes(string):
    return "\\'".join("'" + p + "'" for p in string.split("'"))

#
# Closes the database connection
#

@app.teardown_appcontext
def close_db_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

# List all files
@app.route('/')
def index():
    db = get_db()
    sql = db.execute('select id, title, path from files order by id asc')
    files =  sql.fetchall()
    return render_template('index.html', files=files)

# Play a specific file or vote it up in the queue
@app.route('/play/<id>')
def play(id):

    db = get_db()

    if is_running("mplayer"):
        #os.system("pkill -9 mplayer");
        ip = request.remote_addr # Get visitor ip address
        sql = db.execute('insert into votes (file_id, ip) values(?, ?)', [id, ip])
        db.commit()
    else:
        sql = db.execute('select id, title, path from files where id = ?', id)
        file = sql.fetchone()
        full_path = file[2] + '/' + file[1]
        os.system("mplayer %s &" % shellquotes(full_path))

    return redirect("http://localhost:5000/")

if __name__ == '__main__':
    init_db()
    app.run()