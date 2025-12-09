from api import fetch_sensor_data
from plant_analyzer import analyze_plant_health
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    data = fetch_sensor_data()
    if data:
        result = analyze_plant_health(data)
        return render_template('index.html', data=data, result=result)
    else:
        return "Error fetching sensor data"

if __name__ == "__main__":
    app.run(debug=True)