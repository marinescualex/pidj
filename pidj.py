import os
import re
import subprocess
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)


path = os.path.expanduser(u'~/music') # Path where music is stored


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
#   Get files from music path
#

def make_tree(path):
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
    return tree

# List all files
@app.route('/')
def index():
    return render_template('index.html', tree=make_tree(path))

# Play a specific file or vote it up in the queue
@app.route('/play/<file>')
def play(file):
    if is_running("mplayer"):
        os.system("pkill mplayer");
    os.system("mplayer ~/music/%s &" % file)
    return render_template('index.html', tree=make_tree(path))

if __name__ == '__main__':
    #init_db()
    app.run()