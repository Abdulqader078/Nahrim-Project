from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)
DB = "Database/Nahrim_Database_final.db"

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/map')
def map_page(): 
    return render_template('map.html')

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


@app.route('/rainfall')
def rainfall():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT month, day, AVG(precipitation_mm)
                   FROM rainfall_Kedah_VISUALCROSSING
                   GROUP BY month, day
                   ORDER BY month, day """)
    kedah_data = cursor.fetchall()

    cursor.execute("""
                   SELECT month, day, AVG(precipitation_mm)
                   FROM rainfall_Selangor_VISUALCROSSING
                   GROUP BY month, day
                   ORDER BY month, day """)
    
    selangor_data = cursor.fetchall()
    conn.close()

    return jsonify({
        'kedah': [{'date': f"{row[0]}-{row[1]}", 'rainfall': row[2]} for row in kedah_data],
        'selangor': [{'date': f"{row[0]}-{row[1]}", 'rainfall': row[2]} for row in selangor_data]
    })    

@app.route('/rainfall/openmeteo')
def rainfall_openmeteo():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    cursor.execute(""" 
                    SELECT month, day, AVG(precipitation_mm)
                    FROM rainfall_Kedah_OPENMETEO
                    GROUP BY month, day 
                    ORDER BY month, day """)
    kedah_data = cursor.fetchall()

    cursor.execute("""
                SELECT month, day, AVG(precipitation_mm)
                FROM rainfall_Selangor_OPENMETEO
                GROUP BY month, day
                ORDER BY month, day """)                   
    selangor_data = cursor.fetchall()
    conn.close()

    return jsonify ({
    'kedah': [{'date': f"{row[0]}-{row[1]}", 'rainfall': row[2]} for row in kedah_data],
    'selangor': [{'date': f"{row[0]}-{row[1]}", 'rainfall': row[2]} for row in selangor_data]
    })

@app.route('/rainfall/nahrim')
def rainfall_nahrim():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    cursor.execute(""" 
                    SELECT Month, Day, AVG(Average_RCP)
                    FROM rainfall_Kedah_NAHRIM
                    GROUP BY Month, Day 
                    ORDER BY Month, Day """)
    kedah_data = cursor.fetchall()
    cursor.execute("""
                    SELECT Month, Day, AVG(Ave_RCP)
                    FROM rainfall_Selangor_NAHRIM
                    GROUP BY Month, Day 
                    ORDER BY Month, Day """)                   
    selangor_data = cursor.fetchall()
    conn.close()
    return jsonify ({
    'kedah': [{'date': f"{row[0]}-{row[1]}", 'avg': row[2]} for row in kedah_data],
    'selangor': [{'date': f"{row[0]}-{row[1]}", 'avg': row[2]} for row in selangor_data]
    })

@app.route('/heatmap')
def heatmap():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Latitude, Longitude, AVG(Average_RCP)
        FROM rainfall_Kedah_NAHRIM
        GROUP BY Latitude, Longitude """) 
    kedah_data = cursor.fetchall()

    cursor.execute("""
        SELECT Latitude, Longitude, AVG(Ave_RCP)
        FROM rainfall_Selangor_NAHRIM
        GROUP BY Latitude, Longitude """)
    selangor_data = cursor.fetchall()
    conn.close()

    all_values = [row[2] for row in kedah_data] + [row[2] for row in selangor_data]
    max_val = max(all_values) if all_values else 1

    return jsonify ({
        'kedah': [{'lat': row[0], 'lon': row[1], 'intensity': row[2] / max_val} for row in kedah_data],
        'selangor': [{'lat': row[0], 'lon': row[1], 'intensity': row[2] / max_val} for row in selangor_data],        
    })

if __name__ == '__main__':
    app.run(debug=True)