def analyze_plant_health(data):
    recommendations = []
    warnings = []

    # Soil Moisture Check
    moisture = data['soil_moisture']
    if moisture < 30:
        recommendations.append("Water your plant soon")
    elif moisture > 70:
        warnings.append("Possible overwatering - let soil dry out")

    # pH Check
    ph = float(data['soil_ph'])
    if ph < 6.0:
        warnings.append("Soil is too acidic")
    elif ph > 7.5:
        warnings.append("Soil is too alkaline")

    # Light Hours Check
    light = data['light_hours']
    if light < 6:
        recommendations.append("Move plant to brighter location")

    # NPK Check
    npk = data['npk']
    if npk['nitrogen'] < 50:
        recommendations.append("Consider nitrogen fertilizer")

    return {
        'recommendations': recommendations,
        'warnings': warnings,
        'status': 'healthy' if not warnings else 'needs attention'
    }
