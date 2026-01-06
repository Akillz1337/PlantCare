def analyze_trends(current_data, recent_readings):
    trends = []
    
    if len(recent_readings) < 2:
        return trends

    prev_moisture = recent_readings[1][1]
    prev_temp = recent_readings[1][2]

    current_moisture = current_data['soil_moisture']
    current_temp = float(current_data['soil_temp'])
    
    moisture_change = current_moisture - prev_moisture
    temp_change = current_temp - prev_temp

    if moisture_change <= -5:
        trends.append(f"Soil moisture dropped {abs(moisture_change)}% since last reading")
    elif moisture_change >= 5:
        trends.append(f"Soil moisture increased {moisture_change}% since last reading")

    if temp_change >= 3:
        trends.append(f"Soil temperature rising (+ {temp_change}°C) - monitor moisture closely")
    elif temp_change <= -3:
        trends.append(f"Soil temperature dropping (- {abs(temp_change)}C)")
    
    if len(recent_readings) >= 3:
        last_moisture = [r[1] for r in recent_readings[:3]]
        if all(m < 30 for m in last_moisture) and current_moisture < 30:
            trends.append("Moisture has been low for multiple readings - water now")
    
    return trends
