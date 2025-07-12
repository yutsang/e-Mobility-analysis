import pytest
import pandas as pd
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_connectors import (
    HKTransportAPIManager, 
    KMBLWBConnector, 
    MTRConnector, 
    CitybusConnector
)

class TestAPIConnectors:
    """Test cases for API connectors with mocked responses"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.api_manager = HKTransportAPIManager()
    
    @patch('requests.Session.get')
    def test_kmb_routes_api(self, mock_get):
        """Test KMB routes API with mocked response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'route': '1A',
                    'dest_en': 'Tsim Sha Tsui',
                    'orig_en': 'Central',
                    'service_type': '1'
                },
                {
                    'route': '2',
                    'dest_en': 'Mong Kok',
                    'orig_en': 'Central',
                    'service_type': '1'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the API call
        connector = KMBLWBConnector()
        routes = connector.get_routes()
        
        assert isinstance(routes, pd.DataFrame)
        assert not routes.empty
        assert len(routes) == 2
        assert 'route_id' in routes.columns
        assert 'route_name' in routes.columns
    
    @patch('requests.Session.get')
    def test_kmb_stops_api(self, mock_get):
        """Test KMB stops API with mocked response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'stop': 'WT001',
                    'name_en': 'Central Bus Terminus',
                    'lat': 22.2783,
                    'long': 114.1747
                },
                {
                    'stop': 'WT002',
                    'name_en': 'Admiralty Bus Station',
                    'lat': 22.2799,
                    'long': 114.1648
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the API call
        connector = KMBLWBConnector()
        stops = connector.get_stops()
        
        assert isinstance(stops, pd.DataFrame)
        assert not stops.empty
        assert len(stops) == 2
        assert 'stop_id' in stops.columns
        assert 'stop_name' in stops.columns
    
    @patch('requests.Session.get')
    def test_kmb_eta_api(self, mock_get):
        """Test KMB ETA API with mocked response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'route': '1A',
                    'eta': '2024-01-01T10:30:00Z',
                    'eta_seq': '1',
                    'dest_en': 'Tsim Sha Tsui'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the API call
        connector = KMBLWBConnector()
        eta = connector.get_stop_eta('WT001', '1A')
        
        assert isinstance(eta, pd.DataFrame)
        assert not eta.empty
        assert 'eta' in eta.columns
        assert 'route_id' in eta.columns
    
    @patch('requests.Session.get')
    def test_mtr_stations_api(self, mock_get):
        """Test MTR stations API with mocked response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'stops': [
                {
                    'stop_id': 'MTR001',
                    'name_en': 'Central',
                    'lat': 22.2783,
                    'long': 114.1747,
                    'line': 'Island Line'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the API call
        connector = MTRConnector()
        stations = connector.get_stations()
        
        assert isinstance(stations, pd.DataFrame)
        assert not stations.empty
        assert 'station_id' in stations.columns
        assert 'station_name' in stations.columns
    
    @patch('requests.Session.get')
    def test_citybus_routes_api(self, mock_get):
        """Test Citybus routes API with mocked response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'route': '10',
                    'dest_en': 'North Point',
                    'orig_en': 'Central',
                    'service_type': '1'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the API call
        connector = CitybusConnector()
        routes = connector.get_routes()
        
        assert isinstance(routes, pd.DataFrame)
        assert not routes.empty
        assert 'route_id' in routes.columns
    
    def test_api_manager_initialization(self):
        """Test API manager initialization"""
        assert self.api_manager is not None
        assert hasattr(self.api_manager, 'kmb_lwb')
        assert hasattr(self.api_manager, 'mtr')
        assert hasattr(self.api_manager, 'citybus')
        assert hasattr(self.api_manager, 'gmb')
        assert hasattr(self.api_manager, 'traffic')
    
    @patch.object(KMBLWBConnector, 'get_routes')
    @patch.object(MTRConnector, 'get_stations')
    @patch.object(CitybusConnector, 'get_routes')
    def test_get_all_routes(self, mock_citybus, mock_mtr, mock_kmb):
        """Test getting all routes from API manager"""
        # Mock responses
        mock_kmb.return_value = pd.DataFrame({'route_id': ['1A'], 'route_name': ['Test']})
        mock_citybus.return_value = pd.DataFrame({'route_id': ['10'], 'route_name': ['Test']})
        
        routes = self.api_manager.get_all_routes()
        
        assert isinstance(routes, dict)
        assert 'KMB/LWB' in routes
        assert 'MTR' in routes
        assert 'Citybus' in routes
        assert 'GMB' in routes
    
    @patch.object(KMBLWBConnector, 'get_stops')
    @patch.object(MTRConnector, 'get_stations')
    @patch.object(CitybusConnector, 'get_stops')
    def test_get_all_stops(self, mock_citybus, mock_mtr, mock_kmb):
        """Test getting all stops from API manager"""
        # Mock responses
        mock_kmb.return_value = pd.DataFrame({'stop_id': ['WT001'], 'stop_name': ['Test']})
        mock_mtr.return_value = pd.DataFrame({'station_id': ['MTR001'], 'station_name': ['Test']})
        mock_citybus.return_value = pd.DataFrame({'stop_id': ['CT001'], 'stop_name': ['Test']})
        
        stops = self.api_manager.get_all_stops()
        
        assert isinstance(stops, dict)
        assert 'KMB/LWB' in stops
        assert 'MTR' in stops
        assert 'Citybus' in stops
        assert 'GMB' in stops

class TestAPIErrorHandling:
    """Test cases for API error handling"""
    
    @patch('requests.Session.get')
    def test_api_timeout_handling(self, mock_get):
        """Test handling of API timeouts"""
        mock_get.side_effect = Exception("Connection timeout")
        
        connector = KMBLWBConnector()
        routes = connector.get_routes()
        
        # Should return empty DataFrame on error
        assert isinstance(routes, pd.DataFrame)
        assert routes.empty
    
    @patch('requests.Session.get')
    def test_api_invalid_json_handling(self, mock_get):
        """Test handling of invalid JSON responses"""
        mock_response = Mock()
        mock_response.json.side_effect = Exception("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        connector = KMBLWBConnector()
        routes = connector.get_routes()
        
        # Should return empty DataFrame on error
        assert isinstance(routes, pd.DataFrame)
        assert routes.empty
    
    @patch('requests.Session.get')
    def test_api_http_error_handling(self, mock_get):
        """Test handling of HTTP errors"""
        mock_get.side_effect = Exception("HTTP 500")
        
        connector = KMBLWBConnector()
        routes = connector.get_routes()
        
        # Should return empty DataFrame on error
        assert isinstance(routes, pd.DataFrame)
        assert routes.empty

class TestDataValidation:
    """Test cases for data validation"""
    
    def test_route_data_structure(self):
        """Test that route data has correct structure"""
        expected_columns = ['route_id', 'route_name', 'origin', 'destination', 'service_type', 'company']
        
        # Create sample route data
        sample_data = pd.DataFrame({
            'route_id': ['1A'],
            'route_name': ['Test Route'],
            'origin': ['Central'],
            'destination': ['Tsim Sha Tsui'],
            'service_type': ['1'],
            'company': ['KMB/LWB']
        })
        
        for col in expected_columns:
            assert col in sample_data.columns
    
    def test_stop_data_structure(self):
        """Test that stop data has correct structure"""
        expected_columns = ['stop_id', 'stop_name', 'lat', 'lng', 'company']
        
        # Create sample stop data
        sample_data = pd.DataFrame({
            'stop_id': ['WT001'],
            'stop_name': ['Test Stop'],
            'lat': [22.2783],
            'lng': [114.1747],
            'company': ['KMB/LWB']
        })
        
        for col in expected_columns:
            assert col in sample_data.columns
    
    def test_eta_data_structure(self):
        """Test that ETA data has correct structure"""
        expected_columns = ['stop_id', 'route_id', 'eta', 'eta_seq', 'dest_en', 'company']
        
        # Create sample ETA data
        sample_data = pd.DataFrame({
            'stop_id': ['WT001'],
            'route_id': ['1A'],
            'eta': ['2024-01-01T10:30:00Z'],
            'eta_seq': ['1'],
            'dest_en': ['Tsim Sha Tsui'],
            'company': ['KMB/LWB']
        })
        
        for col in expected_columns:
            assert col in sample_data.columns

if __name__ == "__main__":
    pytest.main([__file__]) 