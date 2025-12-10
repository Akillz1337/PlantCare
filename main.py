from api import fetch_sensor_data
from plant_analyzer import analyze_plant_health
from weather import fetch_weather
from database import init_db, save_reading, get_recent_readings
from trend_analyzer import analyze_trends
from flask import Flask, render_template

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    data = fetch_sensor_data()
    weather = fetch_weather()
    
    if data:
        save_reading(data)

        recent_readings = get_recent_readings(limit=5)

        trends = analyze_trends(data, recent_readings)

        result = analyze_plant_health(data, weather)
        
        return render_template('index.html', 
                             data=data, 
                             result=result, 
                             weather=weather,
                             trends=trends)
    else:
        return "Error fetching sensor data"

if __name__ == "__main__":
    app.run(debug=True)
