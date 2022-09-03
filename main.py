from functools import wraps
from flask import Flask, jsonify, request, Response
import sqlite3
import pandas as pd
from math import cos, asin, sqrt
import base64

def check(authorization_header):
    username = "toto"
    password = "titi"
    encoded_uname_pass = authorization_header.split()[-1]
    str  = username + ":" + password
    if encoded_uname_pass == base64.b64encode(str.encode("utf-8")).decode('utf-8'):
        return True

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        return f(*args, **kwargs)
    return decorated            


def initVelibTable(conn):
    """
    Delete all rows in the data in table
    """
    try:
        sql = 'DROP TABLE IF EXISTS velib;'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()    
    except:
        sql = 'CREATE TABLE velib'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        

app = Flask(__name__)

connection = sqlite3.connect("db.sqlite") # change to 'sqlite:///your_filename.db'

 
initVelibTable(connection)


df = pd.read_csv('ressources/velib-pos.csv', sep=";", low_memory=False)
df.to_sql("velib", connection, if_exists='append', index=False)
connection.commit()


@app.route('/find/velib', methods=['GET'])
@login_required
def find_velib():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    cursor = sqlite3.connect("db.sqlite") .cursor()
    data = cursor.execute('''SELECT geo, "Nom de la station" FROM velib''')
    list = [] 
    for row in data:  
        tmp = {'latitude': float(row[0].split(",")[0]), 'longitude': float(row[0].split(",")[1]),'name': row[1]}
        list.append(tmp)   
    
    return closest(list, {'latitude': float(latitude), 'longitude': float(longitude)})
 


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(data, v):
    return min(data, key=lambda p: distance(v['latitude'],v['longitude'],p['latitude'],p['longitude']))
 

app.run(host='0.0.0.0', port=9090)
