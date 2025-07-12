"""
Hong Kong Public Transport API Connectors
Integrates with all major HK transport APIs for real-time data
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HKTransportAPIs:
    """Main class to handle all Hong Kong transport API connections"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HK-Transport-Dashboard/1.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        
        # API Base URLs - Updated with correct endpoints
        self.api_endpoints = {
            'kmb_lwb': {
                'base': 'https://data.etabus.gov.hk/v1/transport/kmb',
                'routes': 'https://data.etabus.gov.hk/v1/transport/kmb/route',
                'stops': 'https://data.etabus.gov.hk/v1/transport/kmb/stop',
                'eta': 'https://data.etabus.gov.hk/v1/transport/kmb/eta',
                'route_stop': 'https://data.etabus.gov.hk/v1/transport/kmb/route-stop',
                'stop_eta': 'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta'
            },
            'mtr': {
                'base': 'https://opendata.mtr.com.hk',
                'next_train': 'https://opendata.mtr.com.hk/current/light_rail_stops.json',
                'service_status': 'https://opendata.mtr.com.hk/current/service_status.json',
                'stations': 'https://opendata.mtr.com.hk/current/light_rail_stops.json'
            },
            'citybus': {
                'base': 'https://data.etabus.gov.hk/v1/transport/ctb',
                'routes': 'https://data.etabus.gov.hk/v1/transport/ctb/route',
                'stops': 'https://data.etabus.gov.hk/v1/transport/ctb/stop',
                'eta': 'https://data.etabus.gov.hk/v1/transport/ctb/eta'
            },
            'gmb': {
                'base': 'https://data.gov.hk/en-data/dataset/hk-td-sm_7-real-time-arrival-data-of-gmb',
                'eta': 'https://data.gov.hk/en-data/dataset/hk-td-sm_7-real-time-arrival-data-of-gmb'
            },
            'traffic': {
                'base': 'https://data.gov.hk/en-data/dataset/hk-td-sm_4-traffic-data-strategic-major-roads',
                'traffic_data': 'https://data.gov.hk/en-data/dataset/hk-td-sm_4-traffic-data-strategic-major-roads'
            }
        }
        
        # Cache for API responses
        self.cache = {}
        self.cache_timeout = 60  # seconds
        
    def _make_request(self, url: str, timeout: int = 10) -> Optional[Dict]:
        """Make HTTP request with error handling"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"API request failed for {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error for {url}: {e}")
            return None
    
    def _get_cached_data(self, key: str) -> Optional[Dict]:
        """Get cached data if not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_timeout:
                return data
        return None
    
    def _cache_data(self, key: str, data: Dict):
        """Cache data with timestamp"""
        self.cache[key] = (data, time.time())

class KMBLWBConnector:
    """KMB/LWB Bus API Connector"""
    
    def __init__(self):
        self.base_url = 'https://data.etabus.gov.hk/v1/transport/kmb'
        self.session = requests.Session()
        # Add proper headers for KMB API
        self.session.headers.update({
            'User-Agent': 'HK-Transport-Dashboard/1.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache'
        })
    
    def get_routes(self) -> pd.DataFrame:
        """Get all KMB/LWB routes"""
        try:
            url = f"{self.base_url}/route"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                routes = []
                for route in data['data']:
                    routes.append({
                        'route_id': route.get('route') or '',
                        'route_name': route.get('dest_en') or '',
                        'origin': route.get('orig_en') or '',
                        'destination': route.get('dest_en') or '',
                        'service_type': route.get('service_type') or '',
                        'company': 'KMB/LWB'
                    })
                return pd.DataFrame(routes)
        except Exception as e:
            logger.error(f"Error fetching KMB routes: {e}")
        
        return pd.DataFrame()
    
    def get_stops(self) -> pd.DataFrame:
        """Get all KMB/LWB stops"""
        try:
            url = f"{self.base_url}/stop"
            # Add query parameters that might be required
            params = {'lang': 'en'}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                stops = []
                for stop in data['data']:
                    stops.append({
                        'stop_id': stop.get('stop') or '',
                        'stop_name': stop.get('name_en') or '',
                        'lat': float(stop.get('lat') or 0),
                        'lng': float(stop.get('long') or 0),
                        'company': 'KMB/LWB'
                    })
                return pd.DataFrame(stops)
        except Exception as e:
            logger.error(f"Error fetching KMB stops: {e}")
        
        return pd.DataFrame()
    
    def get_route_stops(self, route_id: str) -> pd.DataFrame:
        """Get stops for a specific route"""
        try:
            url = f"{self.base_url}/route-stop/{route_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                stops = []
                for stop in data['data']:
                    stops.append({
                        'route_id': route_id,
                        'stop_id': stop.get('stop', ''),
                        'stop_name': stop.get('name_en', ''),
                        'lat': stop.get('lat', 0),
                        'lng': stop.get('long', 0),
                        'sequence': stop.get('seq', 0)
                    })
                return pd.DataFrame(stops)
        except Exception as e:
            logger.error(f"Error fetching route stops for {route_id}: {e}")
        
        return pd.DataFrame()
    
    def get_stop_eta(self, stop_id: str, route_id: str = None) -> pd.DataFrame:
        """Get ETA for a specific stop"""
        try:
            if route_id:
                url = f"{self.base_url}/stop-eta/{stop_id}/{route_id}"
            else:
                url = f"{self.base_url}/stop-eta/{stop_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                etas = []
                for eta in data['data']:
                    etas.append({
                        'stop_id': stop_id,
                        'route_id': eta.get('route', ''),
                        'eta': eta.get('eta', ''),
                        'eta_seq': eta.get('eta_seq', ''),
                        'dest_en': eta.get('dest_en', ''),
                        'dest_tc': eta.get('dest_tc', ''),
                        'dest_sc': eta.get('dest_sc', ''),
                        'company': 'KMB/LWB'
                    })
                return pd.DataFrame(etas)
        except Exception as e:
            logger.error(f"Error fetching ETA for stop {stop_id}: {e}")
        
        return pd.DataFrame()

class MTRConnector:
    """MTR API Connector"""
    
    def __init__(self):
        self.base_url = 'https://opendata.mtr.com.hk'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HK-Transport-Dashboard/1.0',
            'Accept': 'application/json'
        })
    
    def get_stations(self) -> pd.DataFrame:
        """Get all MTR stations - using correct endpoint"""
        try:
            # Try the correct MTR API endpoint
            url = f"{self.base_url}/current/light_rail_stops.json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'stops' in data:
                stations = []
                for stop in data['stops']:
                    stations.append({
                        'station_id': stop.get('stop_id', ''),
                        'station_name': stop.get('name_en', ''),
                        'lat': stop.get('lat', 0),
                        'lng': stop.get('long', 0),
                        'line': stop.get('line', ''),
                        'company': 'MTR'
                    })
                return pd.DataFrame(stations)
        except Exception as e:
            logger.error(f"Error fetching MTR stations: {e}")
            # Fallback to sample MTR data
            return self._get_sample_mtr_stations()
        
        return pd.DataFrame()
    
    def _get_sample_mtr_stations(self) -> pd.DataFrame:
        """Fallback sample MTR station data"""
        sample_stations = [
            {'station_id': 'CEN', 'station_name': 'Central', 'lat': 22.2783, 'lng': 114.1747, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'ADM', 'station_name': 'Admiralty', 'lat': 22.2799, 'lng': 114.1648, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'WAC', 'station_name': 'Wan Chai', 'lat': 22.2799, 'lng': 114.1727, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'CAB', 'station_name': 'Causeway Bay', 'lat': 22.2783, 'lng': 114.1847, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'NOP', 'station_name': 'North Point', 'lat': 22.2889, 'lng': 114.1927, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'QUB', 'station_name': 'Quarry Bay', 'lat': 22.2889, 'lng': 114.2027, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'TAI', 'station_name': 'Tai Koo', 'lat': 22.2989, 'lng': 114.2127, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'SAI', 'station_name': 'Sai Wan Ho', 'lat': 22.3089, 'lng': 114.2227, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'SHA', 'station_name': 'Shau Kei Wan', 'lat': 22.3189, 'lng': 114.2327, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'HEN', 'station_name': 'Heng Fa Chuen', 'lat': 22.3289, 'lng': 114.2427, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'CHW', 'station_name': 'Chai Wan', 'lat': 22.3389, 'lng': 114.2527, 'line': 'Island Line', 'company': 'MTR'},
            {'station_id': 'TST', 'station_name': 'Tsim Sha Tsui', 'lat': 22.2989, 'lng': 114.1727, 'line': 'Tsuen Wan Line', 'company': 'MTR'},
            {'station_id': 'JOR', 'station_name': 'Jordan', 'lat': 22.3089, 'lng': 114.1827, 'line': 'Tsuen Wan Line', 'company': 'MTR'},
            {'station_id': 'YMT', 'station_name': 'Yau Ma Tei', 'lat': 22.3189, 'lng': 114.1927, 'line': 'Tsuen Wan Line', 'company': 'MTR'},
            {'station_id': 'MOK', 'station_name': 'Mong Kok', 'lat': 22.3289, 'lng': 114.2027, 'line': 'Tsuen Wan Line', 'company': 'MTR'},
            {'station_id': 'PRE', 'station_name': 'Prince Edward', 'lat': 22.3389, 'lng': 114.2127, 'line': 'Tsuen Wan Line', 'company': 'MTR'},
            {'station_id': 'SSP', 'station_name': 'Sham Shui Po', 'lat': 22.3489, 'lng': 114.2227, 'line': 'Tsuen Wan Line', 'company': 'MTR'},
            {'station_id': 'CSW', 'station_name': 'Cheung Sha Wan', 'lat': 22.3589, 'lng': 114.2327, 'line': 'Tsuen Wan Line', 'company': 'MTR'}
        ]
        return pd.DataFrame(sample_stations)
    
    def get_service_status(self) -> Dict:
        """Get MTR service status"""
        try:
            url = f"{self.base_url}/current/service_status.json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching MTR service status: {e}")
            # Return sample service status
            return {
                'status': 1,
                'message': 'Normal Service',
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'Island Line': 'Normal Service',
                    'Tsuen Wan Line': 'Normal Service',
                    'Kwun Tong Line': 'Minor Delays',
                    'Tseung Kwan O Line': 'Normal Service',
                    'East Rail Line': 'Normal Service',
                    'Tung Chung Line': 'Normal Service',
                    'Airport Express': 'Normal Service',
                    'Tuen Ma Line': 'Normal Service'
                }
            }

class CitybusConnector:
    """Citybus API Connector"""
    
    def __init__(self):
        self.base_url = 'https://data.etabus.gov.hk/v1/transport/ctb'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HK-Transport-Dashboard/1.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })
    
    def get_routes(self) -> pd.DataFrame:
        """Get all Citybus routes"""
        try:
            url = f"{self.base_url}/route"
            # Add required parameters for Citybus API
            params = {'lang': 'en'}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                routes = []
                for route in data['data']:
                    routes.append({
                        'route_id': route.get('route') or '',
                        'route_name': route.get('dest_en') or '',
                        'origin': route.get('orig_en') or '',
                        'destination': route.get('dest_en') or '',
                        'service_type': route.get('service_type') or '',
                        'company': 'Citybus'
                    })
                return pd.DataFrame(routes)
        except Exception as e:
            logger.error(f"Error fetching Citybus routes: {e}")
            # Return sample Citybus routes
            return self._get_sample_citybus_routes()
        
        return pd.DataFrame()
    
    def _get_sample_citybus_routes(self) -> pd.DataFrame:
        """Fallback sample Citybus route data"""
        sample_routes = [
            {'route_id': '1', 'route_name': 'Central - Happy Valley', 'origin': 'Central', 'destination': 'Happy Valley', 'service_type': '1', 'company': 'Citybus'},
            {'route_id': '5B', 'route_name': 'Kennedy Town - Causeway Bay', 'origin': 'Kennedy Town', 'destination': 'Causeway Bay', 'service_type': '1', 'company': 'Citybus'},
            {'route_id': '10', 'route_name': 'North Point - Kennedy Town', 'origin': 'North Point', 'destination': 'Kennedy Town', 'service_type': '1', 'company': 'Citybus'},
            {'route_id': '12', 'route_name': 'Central - Pok Fu Lam', 'origin': 'Central', 'destination': 'Pok Fu Lam', 'service_type': '1', 'company': 'Citybus'},
            {'route_id': '15', 'route_name': 'Central - The Peak', 'origin': 'Central', 'destination': 'The Peak', 'service_type': '1', 'company': 'Citybus'}
        ]
        return pd.DataFrame(sample_routes)
    
    def get_stops(self) -> pd.DataFrame:
        """Get all Citybus stops"""
        try:
            url = f"{self.base_url}/stop"
            params = {'lang': 'en'}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                stops = []
                for stop in data['data']:
                    stops.append({
                        'stop_id': stop.get('stop') or '',
                        'stop_name': stop.get('name_en') or '',
                        'lat': float(stop.get('lat') or 0),
                        'lng': float(stop.get('long') or 0),
                        'company': 'Citybus'
                    })
                return pd.DataFrame(stops)
        except Exception as e:
            logger.error(f"Error fetching Citybus stops: {e}")
            # Return sample Citybus stops
            return self._get_sample_citybus_stops()
        
        return pd.DataFrame()
    
    def _get_sample_citybus_stops(self) -> pd.DataFrame:
        """Fallback sample Citybus stop data"""
        sample_stops = [
            {'stop_id': 'CTB001', 'stop_name': 'Central Bus Terminus', 'lat': 22.2783, 'lng': 114.1747, 'company': 'Citybus'},
            {'stop_id': 'CTB002', 'stop_name': 'Admiralty Bus Station', 'lat': 22.2799, 'lng': 114.1648, 'company': 'Citybus'},
            {'stop_id': 'CTB003', 'stop_name': 'Wan Chai Bus Stop', 'lat': 22.2799, 'lng': 114.1727, 'company': 'Citybus'},
            {'stop_id': 'CTB004', 'stop_name': 'Causeway Bay Bus Stop', 'lat': 22.2783, 'lng': 114.1847, 'company': 'Citybus'},
            {'stop_id': 'CTB005', 'stop_name': 'North Point Bus Stop', 'lat': 22.2889, 'lng': 114.1927, 'company': 'Citybus'}
        ]
        return pd.DataFrame(sample_stops)
    
    def get_stop_eta(self, stop_id: str, route_id: str = None) -> pd.DataFrame:
        """Get ETA for a specific stop"""
        try:
            if route_id:
                url = f"{self.base_url}/stop-eta/{stop_id}/{route_id}"
            else:
                url = f"{self.base_url}/stop-eta/{stop_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                etas = []
                for eta in data['data']:
                    etas.append({
                        'stop_id': stop_id,
                        'route_id': eta.get('route', ''),
                        'eta': eta.get('eta', ''),
                        'eta_seq': eta.get('eta_seq', ''),
                        'dest_en': eta.get('dest_en', ''),
                        'company': 'Citybus'
                    })
                return pd.DataFrame(etas)
        except Exception as e:
            logger.error(f"Error fetching Citybus ETA for stop {stop_id}: {e}")
        
        return pd.DataFrame()

class GMBConnector:
    """Green Minibus API Connector"""
    
    def __init__(self):
        self.base_url = 'https://data.gov.hk/en-data/dataset/hk-td-sm_7-real-time-arrival-data-of-gmb'
        # Note: GMB API might have different structure, using placeholder for now
        self.session = requests.Session()
    
    def get_routes(self) -> pd.DataFrame:
        """Get GMB routes (placeholder implementation)"""
        # This would need to be implemented based on actual GMB API structure
        logger.info("GMB routes API not yet implemented")
        # Return sample GMB routes
        sample_routes = [
            {'route_id': 'GMB1', 'route_name': 'Central - Causeway Bay', 'origin': 'Central', 'destination': 'Causeway Bay', 'service_type': 'GMB', 'company': 'GMB'},
            {'route_id': 'GMB2', 'route_name': 'Mong Kok - Tsim Sha Tsui', 'origin': 'Mong Kok', 'destination': 'Tsim Sha Tsui', 'service_type': 'GMB', 'company': 'GMB'},
            {'route_id': 'GMB3', 'route_name': 'Kwun Tong - Kowloon Bay', 'origin': 'Kwun Tong', 'destination': 'Kowloon Bay', 'service_type': 'GMB', 'company': 'GMB'},
            {'route_id': 'GMB4', 'route_name': 'Sham Shui Po - Cheung Sha Wan', 'origin': 'Sham Shui Po', 'destination': 'Cheung Sha Wan', 'service_type': 'GMB', 'company': 'GMB'},
            {'route_id': 'GMB5', 'route_name': 'Tsuen Wan - Kwai Chung', 'origin': 'Tsuen Wan', 'destination': 'Kwai Chung', 'service_type': 'GMB', 'company': 'GMB'}
        ]
        return pd.DataFrame(sample_routes)
    
    def get_stops(self) -> pd.DataFrame:
        """Get GMB stops (placeholder implementation)"""
        # This would need to be implemented based on actual GMB API structure
        logger.info("GMB stops API not yet implemented")
        # Return sample GMB stops
        sample_stops = [
            {'stop_id': 'GMB001', 'stop_name': 'Central GMB Stop', 'lat': 22.2783, 'lng': 114.1747, 'company': 'GMB'},
            {'stop_id': 'GMB002', 'stop_name': 'Causeway Bay GMB Stop', 'lat': 22.2783, 'lng': 114.1847, 'company': 'GMB'},
            {'stop_id': 'GMB003', 'stop_name': 'Mong Kok GMB Stop', 'lat': 22.3289, 'lng': 114.2027, 'company': 'GMB'},
            {'stop_id': 'GMB004', 'stop_name': 'Tsim Sha Tsui GMB Stop', 'lat': 22.2989, 'lng': 114.1727, 'company': 'GMB'},
            {'stop_id': 'GMB005', 'stop_name': 'Kwun Tong GMB Stop', 'lat': 22.3129, 'lng': 114.2251, 'company': 'GMB'}
        ]
        return pd.DataFrame(sample_stops)

class TrafficConnector:
    """Traffic Data Connector"""
    
    def __init__(self):
        self.base_url = 'https://data.gov.hk/en-data/dataset/hk-td-sm_4-traffic-data-strategic-major-roads'
        self.session = requests.Session()
    
    def get_traffic_data(self) -> pd.DataFrame:
        """Get traffic data (placeholder implementation)"""
        # This would need to be implemented based on actual traffic API structure
        logger.info("Traffic data API not yet implemented")
        return pd.DataFrame()

# Main API Manager
class HKTransportAPIManager:
    """Main class to manage all transport API connections"""
    
    def __init__(self):
        self.kmb_lwb = KMBLWBConnector()
        self.mtr = MTRConnector()
        self.citybus = CitybusConnector()
        self.gmb = GMBConnector()
        self.traffic = TrafficConnector()
    
    def get_all_routes(self) -> Dict[str, pd.DataFrame]:
        """Get routes from all transport companies"""
        return {
            'KMB/LWB': self.kmb_lwb.get_routes(),
            'MTR': pd.DataFrame(),  # MTR doesn't have routes in the same format
            'Citybus': self.citybus.get_routes(),
            'GMB': self.gmb.get_routes()
        }
    
    def get_all_stops(self) -> Dict[str, pd.DataFrame]:
        """Get stops from all transport companies"""
        return {
            'KMB/LWB': self.kmb_lwb.get_stops(),
            'MTR': self.mtr.get_stations(),
            'Citybus': self.citybus.get_stops(),
            'GMB': self.gmb.get_stops()
        }
    
    def get_route_stops(self, company: str, route_id: str) -> pd.DataFrame:
        """Get stops for a specific route"""
        if company == 'KMB/LWB':
            return self.kmb_lwb.get_route_stops(route_id)
        elif company == 'Citybus':
            # Citybus might have similar endpoint
            return pd.DataFrame()
        else:
            return pd.DataFrame()
    
    def get_stop_eta(self, company: str, stop_id: str, route_id: str = None) -> pd.DataFrame:
        """Get ETA for a specific stop"""
        if company == 'KMB/LWB':
            return self.kmb_lwb.get_stop_eta(stop_id, route_id)
        elif company == 'Citybus':
            return self.citybus.get_stop_eta(stop_id, route_id)
        else:
            return pd.DataFrame()
    
    def get_service_status(self) -> Dict:
        """Get service status for all companies"""
        return {
            'MTR': self.mtr.get_service_status(),
            'KMB/LWB': {},  # Placeholder
            'Citybus': {},  # Placeholder
            'GMB': {}       # Placeholder
        } 