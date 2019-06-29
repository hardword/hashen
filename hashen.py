# hashen/hashen.py
from flask import Flask, request, jsonify
from flask_api import status
from os import kill, path, remove
import time, base64, hashlib
import sqlite3

application = Flask(__name__)

DATABASE = 'database.db'
DATABASE_JOURNAL = 'database.db-journal'
SHUTDOWN_FLAG = 'shutdown.flag'
# You can change SLEEP value to change wait time(seconds)
SLEEP = 5

# DB over hashmap(Python:dictionary) to support multiple worker processes 
def connect_db():
    return sqlite3.connect(DATABASE)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stat(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password VARCHAR(128),
        time REAL(32)
        )''')
    conn.commit()
    conn.close()

def get_total():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT count(*) FROM stat')
    total = cur.fetchone()
    conn.commit()
    conn.close()
    return total[0]

def get_average_time():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT avg(time) FROM stat')
    average = cur.fetchone()
    conn.commit()
    conn.close()
    return average[0]

def insert_stat_data(password, time):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO stat (password, time) VALUES (?,?)', (password, time))
    conn.commit()
    conn.close()

# base64 of sha-512
def genhashen(pwd):
    if isinstance(pwd, basestring):
        return base64.b64encode(hashlib.sha512(pwd).hexdigest().decode('hex'))

# gunicorn support gracefully shutdown natively with TERM signal
def shutdown_server():
    pid = int(open('gunicorn.pid','ro').read().strip())
    kill(pid, 15)

# Initialization
if path.exists(SHUTDOWN_FLAG):
	remove(SHUTDOWN_FLAG)
# You can comment out below 4 lines w.r.t Database to keep old statistics
if path.exists(DATABASE):
	remove(DATABASE)
if path.exists(DATABASE_JOURNAL):
	remove(DATABASE_JOURNAL)
create_tables()

@application.route('/hash', methods=['POST'])
def hashen():
    error = 'Something went wrong.... Check your request data'
    if path.exists(SHUTDOWN_FLAG):
        return 'Server is shutting down.... we can not handle your request.', status.HTTP_400_BAD_REQUEST
    elif request.form.get('password'):
        start = time.time()
        pwd = request.form.get('password')	    
        time.sleep(SLEEP)
        resp = genhashen(pwd)
        if resp:
            finish = time.time()
            insert_stat_data(resp, finish-start)
            return resp  
        else:
            return error, status.HTTP_400_BAD_REQUEST      
    else:
        return error, status.HTTP_400_BAD_REQUEST

@application.route('/shutdown', methods=['GET'])
def shutdown():
    f = open(SHUTDOWN_FLAG,'w+')
    f.close()
    shutdown_server()
    return 'Server shutting down...'

@application.route('/stats', methods=['GET'])
def stats():
    total = get_total()
    average = get_average_time()
    statA = {'total':total,'average':average}
    return jsonify(statA)

if __name__ == '__main__':
    application.run(threaded=True,debug=False,host='0.0.0.0')
