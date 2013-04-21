import os
from sqlite3 import dbapi2 as sqlite3

conn = sqlite3.connect('/tmp/pidj.db')
c = conn.cursor()

c.execute("SELECT files.id, files.title, files.path, file_id, ip, count(file_id) as num from VOTES JOIN FILES ON FILES.id = VOTES.file_id group by file_id order by num desc limit 0, 1")
top_voted = c.fetchone()

def shellquotes(string):
    return "\\'".join("'" + p + "'" for p in string.split("'"))

if top_voted:
    next_song = top_voted[2] + '/' + top_voted[1]
    os.system("mplayer %s &" % shellquotes(next_song))




