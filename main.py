
from flask import Flask, request, render_template
import sqlite3
import pandas as pd
from login_check import *
from find_closest import *
from db_checks import *
from flask_cors import CORS


app = Flask(__name__, static_folder="./client/velib-client/build/static", template_folder='./client/velib-client/build')
CORS(app)
connection = sqlite3.connect("db.sqlite") 
initVelibTable(connection)
df = pd.read_csv('ressources/velib-pos.csv', sep=";", low_memory=False)
df.to_sql("velib", connection, if_exists='append', index=False)
connection.commit()


@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/find/velib', methods=['GET'])
@login_required
def find_velib():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    cursor = sqlite3.connect("db.sqlite") .cursor()
    data = cursor.execute('''SELECT geo, "Nom de la station" FROM velib''')
    list = [] 
    for row in data:  
        list.append({'latitude': float(row[0].split(",")[0]), 'longitude': float(row[0].split(",")[1]),'name': row[1]})   
    
    return closest(list, {'latitude': float(latitude), 'longitude': float(longitude)})

app.run(use_reloader=True, port=9090, threaded=True)
