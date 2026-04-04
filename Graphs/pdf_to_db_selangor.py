import pdfplumber
import sqlite3

# 1. Setup Database
conn = sqlite3.connect('Nahrim_Database_final.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS rainfall_selangor_visualcrossing')
cursor.execute('''
    CREATE TABLE rainfall_selangor_visualcrossing (
        lat REAL, lon REAL, 
        year INTEGER, month INTEGER, day INTEGER, 
        precipitation_mm REAL
    )
''')

pdf_path = "RF_Slgr_Wlyh_Mac_May_2026_AveRCP.pdf" # Make sure this matches your file name!

print("Starting extraction...")

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        # Using a more robust table extraction setting
        table = page.extract_table({
            "vertical_strategy": "text", 
            "horizontal_strategy": "text"
        })
        
        if table:
            print(f"Page {i+1}: Found {len(table)} rows. Processing...")
            for row in table:
                # This helps us see if we are hitting headers or data
                try:
                    # Based on your image: Year(0), Month(1), Day(2), Lat(3), Lon(4), Rain(5)
                    y = int(row[0])
                    m = int(row[1])
                    d = int(row[2])
                    lat = float(row[3])
                    lon = float(row[4])
                    precip = float(row[5]) 

                    cursor.execute('INSERT INTO rainfall_selangor_visualcrossing VALUES (?, ?, ?, ?, ?, ?)', 
                                   (lat, lon, y, m, d, precip))
                except:
                    continue # Skip headers/empty lines

conn.commit()
cursor.execute("SELECT COUNT(*) FROM rainfall_selangor_visualcrossing")
total = cursor.fetchone()[0]
conn.close()

print(f"\nDONE! Successfully extracted {total} data points.")
