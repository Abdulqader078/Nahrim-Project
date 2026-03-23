from flask import Flask, render_template, jsonify
import sqlite3 

app = Flask(__name__)
DB = "Database/Nahrim_Database.db"

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/map')
def map_page(): 
    return render_template('map.html')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/hospitals')
def hostpitals():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT Hospital_Name, Address, Hospital_Type, Latitude, Longitude FROM Hospitals")
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            'name': row[0],
            'address': row[1],
            'type': row[2],
            'lat': row[3],
            'lng': row[4]
        })
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)