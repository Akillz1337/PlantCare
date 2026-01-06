PLANT_PROFILES = {
    'tomato': {
        'name': 'Tomato',
        'moisture': {'min': 50, 'max': 80, 'ideal': 65},
        'ph': {'min': 6.0, 'max': 6.8, 'ideal': 6.5},
        'light_hours': {'min': 8, 'max': 12, 'ideal': 10},
        'soil_temp': {'min': 18, 'max': 25, 'ideal': 22},
        'npk': {
            'nitrogen': {'min': 50, 'ideal': 70},
            'phosphorus': {'min': 40, 'ideal': 60},
            'potassium': {'min': 50, 'ideal': 70}
        },
        'description': 'Tomatoes need plenty of sunlight and water, prefer warm conditions'
    },
    'lettuce': {
        'name': 'Lettuce',
        'moisture': {'min': 40, 'max': 70, 'ideal': 55},
        'ph': {'min': 6.0, 'max': 7.0, 'ideal': 6.5},
        'light_hours': {'min': 6, 'max': 10, 'ideal': 8},
        'soil_temp': {'min': 15, 'max': 22, 'ideal': 18},
        'npk': {
            'nitrogen': {'min': 40, 'ideal': 60},
            'phosphorus': {'min': 30, 'ideal': 50},
            'potassium': {'min': 40, 'ideal': 60}
        },
        'description': 'Lettuce prefers cooler conditions and doesn\'t need too much sunlight'
    },
    'basil': {
        'name': 'Basil',
        'moisture': {'min': 40, 'max': 70, 'ideal': 55},
        'ph': {'min': 6.0, 'max': 7.5, 'ideal': 6.5},
        'light_hours': {'min': 6, 'max': 10, 'ideal': 8},
        'soil_temp': {'min': 18, 'max': 25, 'ideal': 22},
        'npk': {
            'nitrogen': {'min': 45, 'ideal': 65},
            'phosphorus': {'min': 35, 'ideal': 55},
            'potassium': {'min': 45, 'ideal': 65}
        },
        'description': 'Basil is a common herb that needs moderate water and sunlight'
    },
    'default': {
        'name': 'General Plant',
        'moisture': {'min': 30, 'max': 70, 'ideal': 50},
        'ph': {'min': 6.0, 'max': 7.5, 'ideal': 6.5},
        'light_hours': {'min': 6, 'max': 10, 'ideal': 8},
        'soil_temp': {'min': 18, 'max': 25, 'ideal': 22},
        'npk': {
            'nitrogen': {'min': 50, 'ideal': 70},
            'phosphorus': {'min': 40, 'ideal': 60},
            'potassium': {'min': 50, 'ideal': 70}
        },
        'description': 'General plant configuration for most indoor plants'
    }
}

def get_plant_profile(plant_type='default'):
    return PLANT_PROFILES.get(plant_type, PLANT_PROFILES['default'])

def list_available_plants():
    return {key: profile['name'] for key, profile in PLANT_PROFILES.items()}
