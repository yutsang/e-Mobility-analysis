"""
Configuration file for Hong Kong Transportation Dashboard
"""

# Hong Kong Geographic Settings
HK_CENTER = [22.3193, 114.1694]  # Central Hong Kong coordinates
HK_BOUNDARY = [
    [22.15, 113.8], [22.15, 114.5],
    [22.6, 114.5], [22.6, 113.8]
]

# API Endpoints
API_ENDPOINTS = {
    'mtr': {
        'base_url': 'https://opendata.mtr.com.hk',
        'stations': 'https://opendata.mtr.com.hk/current/light_rail_stops.json',
        'service_status': 'https://opendata.mtr.com.hk/current/service_status.json'
    },
    'bus': {
        'base_url': 'https://data.etabus.gov.hk',
        'stops': 'https://data.etabus.gov.hk/v1/transport/kmb/stop',
        'routes': 'https://data.etabus.gov.hk/v1/transport/kmb/route'
    },
    'minibus': {
        'base_url': 'https://data.gov.hk',
        'routes': 'https://data.gov.hk/en-data/dataset/hk-td-tis_21-gmb'
    }
}

# Map Configuration
MAP_CONFIG = {
    'default_zoom': 11,
    'tile_layers': {
        'OpenStreetMap': 'OpenStreetMap',
        'CartoDB positron': 'CartoDB positron',
        'CartoDB dark_matter': 'CartoDB dark_matter',
        'Stamen Terrain': 'Stamen Terrain'
    },
    'marker_colors': {
        'MTR': 'red',
        'Bus': 'blue',
        'Minibus': 'green'
    },
    'marker_icons': {
        'MTR': 'train',
        'Bus': 'bus',
        'Minibus': 'car'
    }
}

# UI Configuration
UI_CONFIG = {
    'page_title': 'Hong Kong Public Transportation Dashboard',
    'page_icon': '🚇',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'refresh_interval': 300,  # seconds
    'max_markers': 1000  # maximum markers to display for performance
}

# Data Configuration
DATA_CONFIG = {
    'cache_timeout': 300,  # seconds
    'max_retries': 3,
    'timeout': 10,
    'use_sample_data': True  # fallback to sample data if APIs fail
}

# Sample Data (fallback when APIs are unavailable)
SAMPLE_MTR_STATIONS = [
    {'name': 'Central', 'lat': 22.2783, 'lng': 114.1747, 'line': 'Island Line'},
    {'name': 'Admiralty', 'lat': 22.2799, 'lng': 114.1648, 'line': 'Island Line'},
    {'name': 'Wan Chai', 'lat': 22.2799, 'lng': 114.1727, 'line': 'Island Line'},
    {'name': 'Causeway Bay', 'lat': 22.2783, 'lng': 114.1847, 'line': 'Island Line'},
    {'name': 'North Point', 'lat': 22.2889, 'lng': 114.1927, 'line': 'Island Line'},
    {'name': 'Quarry Bay', 'lat': 22.2889, 'lng': 114.2027, 'line': 'Island Line'},
    {'name': 'Tai Koo', 'lat': 22.2989, 'lng': 114.2127, 'line': 'Island Line'},
    {'name': 'Sai Wan Ho', 'lat': 22.3089, 'lng': 114.2227, 'line': 'Island Line'},
    {'name': 'Shau Kei Wan', 'lat': 22.3189, 'lng': 114.2327, 'line': 'Island Line'},
    {'name': 'Heng Fa Chuen', 'lat': 22.3289, 'lng': 114.2427, 'line': 'Island Line'},
    {'name': 'Chai Wan', 'lat': 22.3389, 'lng': 114.2527, 'line': 'Island Line'},
    {'name': 'Tsim Sha Tsui', 'lat': 22.2989, 'lng': 114.1727, 'line': 'Tsuen Wan Line'},
    {'name': 'Jordan', 'lat': 22.3089, 'lng': 114.1827, 'line': 'Tsuen Wan Line'},
    {'name': 'Yau Ma Tei', 'lat': 22.3189, 'lng': 114.1927, 'line': 'Tsuen Wan Line'},
    {'name': 'Mong Kok', 'lat': 22.3289, 'lng': 114.2027, 'line': 'Tsuen Wan Line'},
    {'name': 'Prince Edward', 'lat': 22.3389, 'lng': 114.2127, 'line': 'Tsuen Wan Line'},
    {'name': 'Sham Shui Po', 'lat': 22.3489, 'lng': 114.2227, 'line': 'Tsuen Wan Line'},
    {'name': 'Cheung Sha Wan', 'lat': 22.3589, 'lng': 114.2327, 'line': 'Tsuen Wan Line'},
    {'name': 'Lai Chi Kok', 'lat': 22.3689, 'lng': 114.2427, 'line': 'Tsuen Wan Line'},
    {'name': 'Mei Foo', 'lat': 22.3789, 'lng': 114.2527, 'line': 'Tsuen Wan Line'},
    {'name': 'Lai King', 'lat': 22.3889, 'lng': 114.2627, 'line': 'Tsuen Wan Line'},
    {'name': 'Kwai Fong', 'lat': 22.3989, 'lng': 114.2727, 'line': 'Tsuen Wan Line'},
    {'name': 'Kwai Hing', 'lat': 22.4089, 'lng': 114.2827, 'line': 'Tsuen Wan Line'},
    {'name': 'Tai Wo Hau', 'lat': 22.4189, 'lng': 114.2927, 'line': 'Tsuen Wan Line'},
    {'name': 'Tsuen Wan', 'lat': 22.4289, 'lng': 114.3027, 'line': 'Tsuen Wan Line'},
]

SAMPLE_BUS_STOPS = [
    {'name': 'Central Bus Terminus', 'lat': 22.2783, 'lng': 114.1747, 'routes': ['1', '2', '5B', '10']},
    {'name': 'Admiralty Bus Station', 'lat': 22.2799, 'lng': 114.1648, 'routes': ['6', '6A', '6X', '15']},
    {'name': 'Wan Chai Bus Terminus', 'lat': 22.2799, 'lng': 114.1727, 'routes': ['2A', '8', '8P', '25A']},
    {'name': 'Causeway Bay Bus Station', 'lat': 22.2783, 'lng': 114.1847, 'routes': ['5B', '10', '23', '25']},
    {'name': 'North Point Bus Terminus', 'lat': 22.2889, 'lng': 114.1927, 'routes': ['2', '2A', '8', '8P']},
    {'name': 'Quarry Bay Bus Station', 'lat': 22.2889, 'lng': 114.2027, 'routes': ['2', '2A', '8', '8P']},
    {'name': 'Tai Koo Bus Terminus', 'lat': 22.2989, 'lng': 114.2127, 'routes': ['2', '2A', '8', '8P']},
    {'name': 'Sai Wan Ho Bus Station', 'lat': 22.3089, 'lng': 114.2227, 'routes': ['2', '2A', '8', '8P']},
    {'name': 'Shau Kei Wan Bus Terminus', 'lat': 22.3189, 'lng': 114.2327, 'routes': ['2', '2A', '8', '8P']},
    {'name': 'Heng Fa Chuen Bus Station', 'lat': 22.3289, 'lng': 114.2427, 'routes': ['2', '2A', '8', '8P']},
    {'name': 'Chai Wan Bus Terminus', 'lat': 22.3389, 'lng': 114.2527, 'routes': ['2', '2A', '8', '8P']},
]

SAMPLE_MINIBUS_ROUTES = [
    {'name': 'Central - Causeway Bay', 'lat': 22.2783, 'lng': 114.1747, 'route': 'GMB 1', 'fare': '$8.5'},
    {'name': 'Mong Kok - Tsim Sha Tsui', 'lat': 22.3193, 'lng': 114.1694, 'route': 'GMB 2', 'fare': '$7.5'},
    {'name': 'Kwun Tong - Kowloon Bay', 'lat': 22.3129, 'lng': 114.2251, 'route': 'GMB 3', 'fare': '$6.5'},
    {'name': 'Sham Shui Po - Cheung Sha Wan', 'lat': 22.3489, 'lng': 114.2227, 'route': 'GMB 4', 'fare': '$5.5'},
    {'name': 'Tsuen Wan - Kwai Chung', 'lat': 22.4289, 'lng': 114.3027, 'route': 'GMB 5', 'fare': '$7.0'},
]

# Service Status Configuration
SERVICE_STATUS = {
    'mtr': {
        'Island Line': 'Normal Service',
        'Tsuen Wan Line': 'Normal Service',
        'Kwun Tong Line': 'Minor Delays',
        'Tseung Kwan O Line': 'Normal Service',
        'East Rail Line': 'Normal Service',
        'Tung Chung Line': 'Normal Service',
        'Airport Express': 'Normal Service',
        'Tuen Ma Line': 'Normal Service',
    },
    'bus': {
        'KMB': 'Normal Service',
        'Citybus': 'Normal Service',
        'New World First Bus': 'Normal Service',
    },
    'minibus': {
        'Green Minibus': 'Normal Service',
        'Red Minibus': 'Normal Service',
    }
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'peak_hours': {
        'morning': [7, 8, 9],
        'evening': [17, 18, 19]
    },
    'transport_modes': ['MTR', 'Bus', 'Minibus', 'Tram', 'Ferry'],
    'usage_percentages': [45, 30, 15, 5, 5]
} 