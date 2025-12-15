import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            plant_type TEXT DEFAULT 'default',
            soil_moisture INTEGER,
            soil_temp REAL,
            soil_ph REAL,
            light_hours INTEGER
        )
    ''')
    
    try:
        cursor.execute('ALTER TABLE readings ADD COLUMN plant_type TEXT DEFAULT "default"')
    except sqlite3.OperationalError:
        pass
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE,
            setting_value TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO user_settings (setting_key, setting_value)
        VALUES ('current_plant_type', 'default')
    ''')
    
    conn.commit()
    conn.close()

def save_reading(data, plant_type='default'):
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO readings (timestamp, plant_type, soil_moisture, soil_temp, soil_ph, light_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        plant_type,
        data['soil_moisture'],
        float(data['soil_temp']),
        float(data['soil_ph']),
        data['light_hours']
    ))
    
    conn.commit()
    conn.close()

def get_recent_readings(limit=10, plant_type=None):
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    
    if plant_type:
        cursor.execute('''
            SELECT timestamp, soil_moisture, soil_temp, soil_ph, light_hours
            FROM readings
            WHERE plant_type = ?
            ORDER BY id DESC
            LIMIT ?
        ''', (plant_type, limit))
    else:
        cursor.execute('''
            SELECT timestamp, soil_moisture, soil_temp, soil_ph, light_hours
            FROM readings
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
    
    readings = cursor.fetchall()
    conn.close()
    
    return readings

def get_user_setting(key, default=None):
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT setting_value FROM user_settings WHERE setting_key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else default

def set_user_setting(key, value):
    conn = sqlite3.connect('plant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_settings (setting_key, setting_value)
        VALUES (?, ?)
    ''', (key, value))
    conn.commit()
    conn.close()
