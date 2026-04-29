import requests
import sqlite3
import time

conn = sqlite3.connect('../Database/Nahrim_Database_final.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT lat, lon FROM rainfall_selangor_visualcrossing")
locations = cursor.fetchall()

print(f"Adding April & May data for {len(locations)} locations...")

for lat, lon in locations:
    url = "https://climate-api.open-meteo.com/v1/climate"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2026-04-01",
        "end_date": "2026-05-31",
        "models": "best_match",
        "daily": "precipitation_sum"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "reason" in data:
            print(f" API Error for {lat}: {data['reason']}")
            continue

        if 'daily' in data and 'precipitation_sum' in data['daily']:
            for date_str, rain in zip(data['daily']['time'], data['daily']['precipitation_sum']):
                y, m, d = map(int, date_str.split('-'))
                r_val = rain if rain is not None else 0.0
                
                cursor.execute('''
                    INSERT INTO rainfall_openmeteo_selangor VALUES (?, ?, ?, ?, ?, ?)
                ''', (lat, lon, y, m, d, r_val))
            
            conn.commit()
            print(f" Saved April/May for: {lat}, {lon}")
        else:
            print(f" No daily data found in response for: {lat}")

        time.sleep(0.2)

    except Exception as e:
        print(f" Error at {lat}: {e}")
