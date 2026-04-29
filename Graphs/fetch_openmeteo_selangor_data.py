import requests
import sqlite3
import time

conn = sqlite3.connect('../Database/Nahrim_Database_final.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS rainfall_openmeteo_selangor (
        lat REAL, lon REAL, 
        year INTEGER, month INTEGER, day INTEGER, 
        precipitation_mm REAL
    )
''')

cursor.execute("SELECT DISTINCT lat, lon FROM rainfall_selangor_visualcrossing")
locations = cursor.fetchall()

print(f"Found {len(locations)} unique coordinates. Starting API fetch...")

for lat, lon in locations:
    print(f"Fetching Open-Meteo for: {lat}, {lon}...")
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": "2026-03-01",
        "end_date": "2026-04-02", 
        "daily": "precipitation_sum",
        "timezone": "GMT"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        for date_str, rain in zip(data['daily']['time'], data['daily']['precipitation_sum']):
            y, m, d = map(int, date_str.split('-'))
            cursor.execute('INSERT INTO rainfall_openmeteo_selangor VALUES (?, ?, ?, ?, ?, ?)', 
                           (lat, lon, y, m, d, rain if rain else 0.0))
        
        conn.commit()
        time.sleep(0.1)
    except Exception as e:
        print(f"Error at {lat}: {e}")

conn.close()
print("Comparison data fetch complete!")
