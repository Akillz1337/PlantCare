import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            soil_moisture INTEGER,
            soil_temp REAL,
            soil_ph REAL,
            light_hours INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def save_reading(data):
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO readings (timestamp, soil_moisture, soil_temp, soil_ph, light_hours)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        data['soil_moisture'],
        float(data['soil_temp']),
        float(data['soil_ph']),
        data['light_hours']
    ))
    
    conn.commit()
    conn.close()

def get_recent_readings(limit=10):
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, soil_moisture, soil_temp, soil_ph, light_hours
        FROM readings
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    
    readings = cursor.fetchall()
    conn.close()
    
    return readings
