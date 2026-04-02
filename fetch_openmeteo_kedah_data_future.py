import requests
import sqlite3
import time

# 1. Connect to your database
conn = sqlite3.connect('Nahrim_Database_final.db')
cursor = conn.cursor()

# 2. Get your unique coordinates from your existing table
cursor.execute("SELECT DISTINCT lat, lon FROM rainfall_Kedah_visualcrossing")
locations = cursor.fetchall()

print(f"Adding April & May data for {len(locations)} locations...")

# 3. Fetch from the CLIMATE API (Handles future dates up to May 31st)
for lat, lon in locations:
    url = "https://climate-api.open-meteo.com/v1/climate"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2026-04-01",
        "end_date": "2026-05-31",
        "models": "best_match", # Let the API pick the best model for May
        "daily": "precipitation_sum"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # DEBUG: Check if there's an error message from the server
        if "reason" in data:
            print(f" API Error for {lat}: {data['reason']}")
            continue

        if 'daily' in data and 'precipitation_sum' in data['daily']:
            for date_str, rain in zip(data['daily']['time'], data['daily']['precipitation_sum']):
                y, m, d = map(int, date_str.split('-'))
                r_val = rain if rain is not None else 0.0
                
                cursor.execute('''
                    INSERT INTO rainfall_openmeteo_kedah VALUES (?, ?, ?, ?, ?, ?)
                ''', (lat, lon, y, m, d, r_val))
            
            conn.commit()
            print(f" Saved April/May for: {lat}, {lon}")
        else:
            # If it still says no data, it will print the whole response so we can see why
            print(f" No daily data found in response for: {lat}")

        time.sleep(0.2)

    except Exception as e:
        print(f" Error at {lat}: {e}")
