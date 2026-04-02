import requests
import sqlite3
import time

# 1. Connect to your existing database
conn = sqlite3.connect('Nahrim_Database_final.db')
cursor = conn.cursor()

# 2. Create a table for the NEW data source (Open-Meteo)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rainfall_openmeteo_kedah (
        lat REAL, lon REAL, 
        year INTEGER, month INTEGER, day INTEGER, 
        precipitation_mm REAL
    )
''')

# 3. Get all UNIQUE coordinates from your PDF extraction
cursor.execute("SELECT DISTINCT lat, lon FROM rainfall_Kedah_visualcrossing")
locations = cursor.fetchall()

print(f"Found {len(locations)} unique coordinates. Starting API fetch...")

# 4. Loop through every coordinate and get Open-Meteo data
for lat, lon in locations:
    print(f"Fetching Open-Meteo for: {lat}, {lon}...")
    
    # We use the 'archive' for March and 'forecast' for April/May
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": "2026-03-01",
        "end_date": "2026-04-02", # Today's date
        "daily": "precipitation_sum",
        "timezone": "GMT"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        for date_str, rain in zip(data['daily']['time'], data['daily']['precipitation_sum']):
            y, m, d = map(int, date_str.split('-'))
            cursor.execute('INSERT INTO rainfall_openmeteo_kedah VALUES (?, ?, ?, ?, ?, ?)', 
                           (lat, lon, y, m, d, rain if rain else 0.0))
        
        conn.commit()
        time.sleep(0.1) # Be quick but safe
    except Exception as e:
        print(f"Error at {lat}: {e}")

conn.close()
print("Comparison data fetch complete!")
