import pytest
import pandas as pd
import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hk_transport_enhanced import HKTransportData, create_hk_map, HK_CENTER, HK_BOUNDARY

class TestHKTransportData:
    """Test cases for HKTransportData class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.transport_data = HKTransportData()
    
    def test_init(self):
        """Test initialization of HKTransportData"""
        assert self.transport_data is not None
        assert hasattr(self.transport_data, 'base_urls')
        assert hasattr(self.transport_data, 'mtr_stations')
        assert hasattr(self.transport_data, 'bus_stops')
        assert hasattr(self.transport_data, 'minibus_routes')
    
    def test_get_mtr_data(self):
        """Test MTR data retrieval"""
        mtr_data = self.transport_data.get_mtr_data()
        assert isinstance(mtr_data, pd.DataFrame)
        assert not mtr_data.empty
        assert 'name' in mtr_data.columns
        assert 'lat' in mtr_data.columns
        assert 'lng' in mtr_data.columns
        assert 'line' in mtr_data.columns
    
    def test_get_bus_data(self):
        """Test bus data retrieval"""
        bus_data = self.transport_data.get_bus_data()
        assert isinstance(bus_data, pd.DataFrame)
        assert not bus_data.empty
        assert 'name' in bus_data.columns
        assert 'lat' in bus_data.columns
        assert 'lng' in bus_data.columns
        assert 'routes' in bus_data.columns
    
    def test_get_minibus_data(self):
        """Test minibus data retrieval"""
        minibus_data = self.transport_data.get_minibus_data()
        assert isinstance(minibus_data, pd.DataFrame)
        assert not minibus_data.empty
        assert 'name' in minibus_data.columns
        assert 'lat' in minibus_data.columns
        assert 'lng' in minibus_data.columns
        assert 'route' in minibus_data.columns
        assert 'fare' in minibus_data.columns
    
    def test_get_service_status(self):
        """Test service status retrieval"""
        status = self.transport_data.get_service_status()
        assert isinstance(status, dict)
        assert 'mtr' in status
        assert 'bus' in status
        assert 'minibus' in status
        
        # Check MTR lines
        mtr_lines = status['mtr']
        assert isinstance(mtr_lines, dict)
        assert len(mtr_lines) > 0
        
        # Check bus operators
        bus_operators = status['bus']
        assert isinstance(bus_operators, dict)
        assert len(bus_operators) > 0

class TestMapCreation:
    """Test cases for map creation functionality"""
    
    def test_create_hk_map(self):
        """Test map creation with sample data"""
        transport_data = HKTransportData()
        transport_data_dict = {
            'MTR': transport_data.get_mtr_data(),
            'Bus': transport_data.get_bus_data(),
            'Minibus': transport_data.get_minibus_data()
        }
        
        # Test with valid data
        map_obj = create_hk_map(transport_data_dict)
        assert map_obj is not None
        
        # Test with empty data
        empty_dict = {
            'MTR': pd.DataFrame(),
            'Bus': pd.DataFrame(),
            'Minibus': pd.DataFrame()
        }
        map_obj_empty = create_hk_map(empty_dict)
        assert map_obj_empty is not None

class TestConstants:
    """Test cases for application constants"""
    
    def test_hk_center(self):
        """Test Hong Kong center coordinates"""
        assert isinstance(HK_CENTER, list)
        assert len(HK_CENTER) == 2
        assert isinstance(HK_CENTER[0], (int, float))
        assert isinstance(HK_CENTER[1], (int, float))
        # Hong Kong should be around 22.3°N, 114.2°E
        assert 22.0 <= HK_CENTER[0] <= 23.0
        assert 113.0 <= HK_CENTER[1] <= 115.0
    
    def test_hk_boundary(self):
        """Test Hong Kong boundary coordinates"""
        assert isinstance(HK_BOUNDARY, list)
        assert len(HK_BOUNDARY) >= 3  # At least 3 points for a polygon
        for point in HK_BOUNDARY:
            assert isinstance(point, list)
            assert len(point) == 2
            assert isinstance(point[0], (int, float))
            assert isinstance(point[1], (int, float))

class TestDataValidation:
    """Test cases for data validation"""
    
    def test_mtr_data_validation(self):
        """Test MTR data validation"""
        transport_data = HKTransportData()
        mtr_data = transport_data.get_mtr_data()
        
        # Check for required columns
        required_columns = ['name', 'lat', 'lng', 'line']
        for col in required_columns:
            assert col in mtr_data.columns
        
        # Check data types
        assert mtr_data['lat'].dtype in ['float64', 'float32', 'int64', 'int32']
        assert mtr_data['lng'].dtype in ['float64', 'float32', 'int64', 'int32']
        assert mtr_data['name'].dtype == 'object'
        assert mtr_data['line'].dtype == 'object'
        
        # Check for valid coordinates
        assert mtr_data['lat'].min() >= 22.0
        assert mtr_data['lat'].max() <= 23.0
        assert mtr_data['lng'].min() >= 113.0
        assert mtr_data['lng'].max() <= 115.0
    
    def test_bus_data_validation(self):
        """Test bus data validation"""
        transport_data = HKTransportData()
        bus_data = transport_data.get_bus_data()
        
        # Check for required columns
        required_columns = ['name', 'lat', 'lng', 'routes']
        for col in required_columns:
            assert col in bus_data.columns
        
        # Check data types (allow object type for coordinates as they might be strings)
        assert bus_data['lat'].dtype in ['float64', 'float32', 'int64', 'int32', 'object']
        assert bus_data['lng'].dtype in ['float64', 'float32', 'int64', 'int32', 'object']
        assert bus_data['name'].dtype == 'object'
        assert bus_data['routes'].dtype == 'object'
        
        # Check that coordinates can be converted to numeric
        try:
            pd.to_numeric(bus_data['lat'])
            pd.to_numeric(bus_data['lng'])
        except:
            assert False, "Coordinates cannot be converted to numeric values"
    
    def test_minibus_data_validation(self):
        """Test minibus data validation"""
        transport_data = HKTransportData()
        minibus_data = transport_data.get_minibus_data()
        
        # Check for required columns
        required_columns = ['name', 'lat', 'lng', 'route', 'fare']
        for col in required_columns:
            assert col in minibus_data.columns
        
        # Check data types
        assert minibus_data['lat'].dtype in ['float64', 'float32', 'int64', 'int32']
        assert minibus_data['lng'].dtype in ['float64', 'float32', 'int64', 'int32']
        assert minibus_data['name'].dtype == 'object'
        assert minibus_data['route'].dtype == 'object'
        assert minibus_data['fare'].dtype == 'object'

if __name__ == "__main__":
    pytest.main([__file__]) 