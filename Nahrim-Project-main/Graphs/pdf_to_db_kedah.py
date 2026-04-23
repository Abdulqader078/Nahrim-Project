import pdfplumber
import sqlite3

conn = sqlite3.connect('../Database/Nahrim_Database_final.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS rainfall_Kedah_visualcrossing')
cursor.execute('''
    CREATE TABLE rainfall_Kedah_visualcrossing (
        lat REAL, lon REAL, 
        year INTEGER, month INTEGER, day INTEGER, 
        precipitation_mm REAL
    )
''')

pdf_path = "RF_Kedah_Mac_May_2026_AveRCP.pdf" 

print("Starting extraction...")

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        table = page.extract_table({
            "vertical_strategy": "text", 
            "horizontal_strategy": "text"
        })
        
        if table:
            print(f"Page {i+1}: Found {len(table)} rows. Processing...")
            for row in table:
                try:
                    y = int(row[0])
                    m = int(row[1])
                    d = int(row[2])
                    lat = float(row[3])
                    lon = float(row[4])
                    precip = float(row[5]) 

                    cursor.execute('INSERT INTO rainfall_Kedah_visualcrossing VALUES (?, ?, ?, ?, ?, ?)', 
                                   (lat, lon, y, m, d, precip))
                except:
                    continue

conn.commit()
cursor.execute("SELECT COUNT(*) FROM rainfall_Kedah_visualcrossing")
total = cursor.fetchone()[0]
conn.close()

print(f"\nDONE! Successfully extracted {total} data points.")
