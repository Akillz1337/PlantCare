from plant_profiles import get_plant_profile

def analyze_plant_health(data, weather=None, plant_type='default', recent_readings=None):
    profile = get_plant_profile(plant_type)
    recommendations = []
    warnings = []
    contextual_insights = []
    
    moisture = data['soil_moisture']
    ph = float(data['soil_ph'])
    light = data['light_hours']
    soil_temp = float(data['soil_temp'])
    npk = data.get('npk', {})
    
    _check_moisture(moisture, profile, recommendations, warnings)
    _check_ph(ph, profile, recommendations, warnings)
    _check_light(light, profile, recommendations, warnings)
    _check_soil_temp(soil_temp, profile, recommendations, warnings)
    _check_npk(npk, profile, recommendations, warnings)
    
    contextual_insights.extend(_analyze_contextual_relationships(
        moisture, ph, light, soil_temp, weather, profile
    ))
    
    if recent_readings and len(recent_readings) > 1:
        contextual_insights.extend(_analyze_trend_context(
            data, recent_readings, profile
        ))
    
    status = _determine_status(warnings, recommendations, contextual_insights)
    
    return {
        'recommendations': recommendations,
        'warnings': warnings,
        'contextual_insights': contextual_insights,
        'status': status,
        'plant_name': profile['name']
    }

def _check_moisture(moisture, profile, recommendations, warnings):
    ideal = profile['moisture']['ideal']
    min_val = profile['moisture']['min']
    max_val = profile['moisture']['max']
    
    if moisture < min_val:
        recommendations.append(f"Soil moisture too low ({moisture}%), {profile['name']} needs watering")
    elif moisture > max_val:
        warnings.append(f"Soil moisture too high ({moisture}%), possible overwatering")
    elif moisture < ideal - 10:
        recommendations.append(f"Soil moisture low ({moisture}%), consider watering")

def _check_ph(ph, profile, recommendations, warnings):
    ideal = profile['ph']['ideal']
    min_val = profile['ph']['min']
    max_val = profile['ph']['max']
    
    if ph < min_val:
        warnings.append(f"Soil too acidic (pH {ph:.1f}), {profile['name']} may struggle to absorb nutrients")
    elif ph > max_val:
        warnings.append(f"Soil too alkaline (pH {ph:.1f}), {profile['name']} may struggle to absorb nutrients")
    elif abs(ph - ideal) > 0.5:
        recommendations.append(f"Soil pH ({ph:.1f}) deviates from ideal, consider adjustment")

def _check_light(light, profile, recommendations, warnings):
    ideal = profile['light_hours']['ideal']
    min_val = profile['light_hours']['min']
    max_val = profile['light_hours']['max']
    
    if light < min_val:
        recommendations.append(f"Insufficient light ({light} hours), {profile['name']} needs more sunlight")
    elif light > max_val:
        warnings.append(f"Too much light ({light} hours), may stress {profile['name']}")

def _check_soil_temp(soil_temp, profile, recommendations, warnings):
    ideal = profile['soil_temp']['ideal']
    min_val = profile['soil_temp']['min']
    max_val = profile['soil_temp']['max']
    
    if soil_temp < min_val:
        warnings.append(f"Soil temperature too low ({soil_temp}°C), {profile['name']} growth may be limited")
    elif soil_temp > max_val:
        warnings.append(f"Soil temperature too high ({soil_temp}°C), may affect {profile['name']} root health")

def _check_npk(npk, profile, recommendations, warnings):
    if not npk:
        return
    
    for nutrient in ['nitrogen', 'phosphorus', 'potassium']:
        if nutrient in npk and nutrient in profile['npk']:
            value = npk[nutrient]
            min_val = profile['npk'][nutrient]['min']
            ideal = profile['npk'][nutrient]['ideal']
            
            nutrient_name = {'nitrogen': 'Nitrogen', 'phosphorus': 'Phosphorus', 'potassium': 'Potassium'}[nutrient]
            
            if value < min_val:
                recommendations.append(f"{nutrient_name} low ({value}), consider adding {nutrient_name.lower()}-rich fertilizer")

def _analyze_contextual_relationships(moisture, ph, light, soil_temp, weather, profile):
    insights = []
    
    if weather:
        if weather['temperature'] > 25 and moisture < profile['moisture']['ideal']:
            insights.append("High temperature + Low soil moisture: Plant losing water faster, water immediately")
        
        if weather['temperature'] < 10 and moisture > profile['moisture']['ideal'] + 20:
            insights.append("Low temperature + High moisture: Increased root rot risk, reduce watering frequency")
        
        if weather['humidity'] < 30 and moisture < profile['moisture']['min']:
            insights.append("Dry environment + Low soil moisture: Plant facing severe dehydration, urgent watering needed")
    
    if light > profile['light_hours']['max'] and moisture < profile['moisture']['ideal']:
        insights.append("High light + Low moisture: Plant may experience light stress, consider shading or increasing humidity")
    
    if soil_temp > profile['soil_temp']['max'] and ph > profile['ph']['ideal'] + 0.5:
        insights.append("High temperature + High pH: Nutrient absorption efficiency reduced, consider cooling or pH adjustment")
    
    if light < profile['light_hours']['min'] and moisture > profile['moisture']['max']:
        insights.append("Low light + High moisture: Increased risk of mold and fungal infection, improve ventilation")
    
    ideal_count = 0
    if profile['moisture']['min'] <= moisture <= profile['moisture']['max']:
        ideal_count += 1
    if profile['ph']['min'] <= ph <= profile['ph']['max']:
        ideal_count += 1
    if profile['light_hours']['min'] <= light <= profile['light_hours']['max']:
        ideal_count += 1
    if profile['soil_temp']['min'] <= soil_temp <= profile['soil_temp']['max']:
        ideal_count += 1
    
    if ideal_count >= 3:
        insights.append("Multiple parameters in ideal range, plant growing conditions are good")
    
    return insights

def _analyze_trend_context(current_data, recent_readings, profile):
    insights = []
    
    if len(recent_readings) < 2:
        return insights
    
    prev_moisture = recent_readings[1][1] if isinstance(recent_readings[1], tuple) else recent_readings[1].get('soil_moisture', 0)
    current_moisture = current_data['soil_moisture']
    moisture_trend = current_moisture - prev_moisture
    
    if moisture_trend < -10 and current_moisture < profile['moisture']['min']:
        insights.append("Rapid moisture decline and below minimum threshold: Take immediate action")
    
    if len(recent_readings) >= 3:
        low_count = sum(1 for r in recent_readings[:3] 
                       if (r[1] if isinstance(r, tuple) else r.get('soil_moisture', 0)) 
                           < profile['moisture']['min'])
        if low_count >= 2 and current_moisture < profile['moisture']['min']:
            insights.append("Moisture consistently low: Need to adjust watering strategy")
    
    return insights

def _determine_status(warnings, recommendations, contextual_insights):
    if warnings:
        return 'needs attention'
    elif any('High temperature' in insight or 'Rapid moisture' in insight for insight in contextual_insights):
        return 'needs attention'
    elif recommendations:
        return 'healthy but could improve'
    else:
        return 'healthy'
