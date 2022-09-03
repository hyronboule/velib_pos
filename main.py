from flask import Flask, jsonify, request
import sqlite3
import pandas as pd
from math import cos, asin, sqrt
from json import JSONEncoder

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

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    return jsonify(data)   


@app.route('/find/velib', methods=['GET'])
def find_velib():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    cursor = sqlite3.connect("db.sqlite") .cursor()
    data = cursor.execute('''SELECT geo, "Nom de la station" FROM velib''')
    list = [] 
    for row in data:  
        tmp = {'latitude': float(row[0].split(",")[0]), 'longitude': float(row[0].split(",")[1]),'name': row[1]}
        list.append(tmp)   
    
    return closest(list, {'latitude': float(latitude or 0), 'longitude': float(longitude or 0)})
 



def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(data, v):
    return min(data, key=lambda p: distance(v['latitude'],v['longitude'],p['latitude'],p['longitude']))
 
 

app.run(host='0.0.0.0', port=9090)
