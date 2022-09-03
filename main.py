from flask import Flask, jsonify, request
import sqlite3
import pandas as pd

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


app.run(host='0.0.0.0', port=9090)
