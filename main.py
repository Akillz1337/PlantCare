from api import fetch_sensor_data
from plant_analyzer import analyze_plant_health
from weather import fetch_weather
from database import init_db, save_reading, get_recent_readings, get_user_setting, set_user_setting
from trend_analyzer import analyze_trends
from plant_profiles import list_available_plants
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

init_db()

def get_mock_data():
    return {
        'soil_moisture': 45,
        'soil_temp': 22.5,
        'soil_ph': 6.5,
        'light_hours': 8,
        'npk': {
            'nitrogen': 60,
            'phosphorus': 50,
            'potassium': 60
        }
    }

@app.route("/")
def index():
    data = fetch_sensor_data()
    weather = fetch_weather()
    
    plant_type = get_user_setting('current_plant_type', 'default')
    
    use_mock_data = False
    if not data:
        recent_readings = get_recent_readings(limit=1, plant_type=plant_type)
        if recent_readings:
            last_reading = recent_readings[0]
            data = {
                'soil_moisture': last_reading[1],
                'soil_temp': last_reading[2],
                'soil_ph': last_reading[3],
                'light_hours': last_reading[4],
                'npk': {
                    'nitrogen': 60,
                    'phosphorus': 50,
                    'potassium': 60
                }
            }
        else:
            data = get_mock_data()
            use_mock_data = True
    else:
        save_reading(data, plant_type)
    
    recent_readings = get_recent_readings(limit=5, plant_type=plant_type)
    
    result = analyze_plant_health(data, weather, plant_type, recent_readings)
    
    trends = analyze_trends(data, recent_readings)
    
    available_plants = list_available_plants()
    
    return render_template('index.html', 
                         data=data, 
                         result=result, 
                         weather=weather,
                         trends=trends,
                         plant_type=plant_type,
                         available_plants=available_plants,
                         use_mock_data=use_mock_data)

@app.route("/api/plants", methods=["GET"])
def get_plants():
    return jsonify(list_available_plants())

@app.route("/api/plant/select", methods=["POST"])
def select_plant():
    data = request.get_json()
    plant_type = data.get('plant_type', 'default')
    
    available_plants = list_available_plants()
    if plant_type not in available_plants:
        return jsonify({'error': 'Invalid plant type'}), 400
    
    set_user_setting('current_plant_type', plant_type)
    return jsonify({'success': True, 'plant_type': plant_type})

@app.route("/api/plant/current", methods=["GET"])
def get_current_plant():
    plant_type = get_user_setting('current_plant_type', 'default')
    return jsonify({'plant_type': plant_type})

if __name__ == "__main__":
    app.run(debug=True)
