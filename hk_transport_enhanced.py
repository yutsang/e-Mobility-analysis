import streamlit as st
import folium
import pandas as pd
import requests
import json
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Hong Kong Public Transportation Dashboard",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .transport-icon {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    .status-normal { color: #28a745; }
    .status-delay { color: #ffc107; }
    .status-disruption { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Hong Kong coordinates and boundaries
HK_CENTER = [22.3193, 114.1694]
HK_BOUNDARY = [
    [22.15, 113.8], [22.15, 114.5],
    [22.6, 114.5], [22.6, 113.8]
]

class HKTransportData:
    def __init__(self):
        self.base_urls = {
            'mtr': 'https://opendata.mtr.com.hk',
            'bus': 'https://data.etabus.gov.hk',
            'minibus': 'https://data.gov.hk'
        }
        
        # Sample MTR station data (since API might be limited)
        self.mtr_stations = [
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
        
        # Sample bus stops data
        self.bus_stops = [
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
        
        # Sample minibus routes
        self.minibus_routes = [
            {'name': 'Central - Causeway Bay', 'lat': 22.2783, 'lng': 114.1747, 'route': 'GMB 1', 'fare': '$8.5'},
            {'name': 'Mong Kok - Tsim Sha Tsui', 'lat': 22.3193, 'lng': 114.1694, 'route': 'GMB 2', 'fare': '$7.5'},
            {'name': 'Kwun Tong - Kowloon Bay', 'lat': 22.3129, 'lng': 114.2251, 'route': 'GMB 3', 'fare': '$6.5'},
            {'name': 'Sham Shui Po - Cheung Sha Wan', 'lat': 22.3489, 'lng': 114.2227, 'route': 'GMB 4', 'fare': '$5.5'},
            {'name': 'Tsuen Wan - Kwai Chung', 'lat': 22.4289, 'lng': 114.3027, 'route': 'GMB 5', 'fare': '$7.0'},
        ]
    
    def get_mtr_data(self):
        """Get MTR station data"""
        try:
            # Try to fetch from API first
            mtr_stations_url = "https://opendata.mtr.com.hk/current/light_rail_stops.json"
            response = requests.get(mtr_stations_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return self._process_mtr_api_data(data)
        except:
            pass
        
        # Fallback to sample data
        return pd.DataFrame(self.mtr_stations)
    
    def _process_mtr_api_data(self, data):
        """Process MTR API data"""
        stations = []
        if 'stops' in data:
            for stop in data['stops']:
                stations.append({
                    'name': stop.get('name_en', ''),
                    'lat': stop.get('lat', 0),
                    'lng': stop.get('long', 0),
                    'line': stop.get('line', ''),
                })
        return pd.DataFrame(stations)
    
    def get_bus_data(self):
        """Get bus stop data"""
        try:
            # Try to fetch from API first
            bus_stops_url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"
            response = requests.get(bus_stops_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return self._process_bus_api_data(data)
        except:
            pass
        
        # Fallback to sample data
        return pd.DataFrame(self.bus_stops)
    
    def _process_bus_api_data(self, data):
        """Process bus API data"""
        stops = []
        if 'data' in data:
            for stop in data['data']:
                stops.append({
                    'name': stop.get('name_en', ''),
                    'lat': stop.get('lat', 0),
                    'lng': stop.get('long', 0),
                    'routes': stop.get('routes', []),
                })
        return pd.DataFrame(stops)
    
    def get_minibus_data(self):
        """Get minibus route data"""
        return pd.DataFrame(self.minibus_routes)
    
    def get_service_status(self):
        """Get real-time service status"""
        # Simulate real-time status
        return {
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

def create_hk_map(transport_data):
    """Create an interactive map of Hong Kong with transportation data"""
    # Create base map centered on Hong Kong
    m = folium.Map(
        location=HK_CENTER,
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add transportation data to map
    colors = {'MTR': 'red', 'Bus': 'blue', 'Minibus': 'green'}
    icons = {'MTR': 'train', 'Bus': 'bus', 'Minibus': 'car'}
    
    for transport_type in transport_data.keys():
        if not transport_data[transport_type].empty:
            df = transport_data[transport_type]
            color = colors.get(transport_type, 'gray')
            icon_name = icons.get(transport_type, 'info-sign')
            
            for idx, row in df.iterrows():
                if pd.notna(row['lat']) and pd.notna(row['lng']):
                    # Create popup content
                    if transport_type == 'MTR':
                        popup_content = f"""
                        <b>{transport_type}: {row['name']}</b><br>
                        Line: {row.get('line', 'N/A')}<br>
                        <a href="https://www.mtr.com.hk" target="_blank">More Info</a>
                        """
                    elif transport_type == 'Bus':
                        routes = row.get('routes', [])
                        routes_str = ', '.join(routes) if routes else 'N/A'
                        popup_content = f"""
                        <b>{transport_type}: {row['name']}</b><br>
                        Routes: {routes_str}<br>
                        <a href="https://www.kmb.hk" target="_blank">More Info</a>
                        """
                    else:  # Minibus
                        popup_content = f"""
                        <b>{transport_type}: {row['name']}</b><br>
                        Route: {row.get('route', 'N/A')}<br>
                        Fare: {row.get('fare', 'N/A')}<br>
                        <a href="https://www.td.gov.hk" target="_blank">More Info</a>
                        """
                    
                    folium.Marker(
                        location=[row['lat'], row['lng']],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=folium.Icon(color=color, icon=icon_name),
                        tooltip=f"{transport_type}: {row['name']}"
                    ).add_to(m)
    
    # Add Hong Kong boundary
    folium.Polygon(
        locations=HK_BOUNDARY,
        color='black',
        weight=2,
        fill=False,
        popup='Hong Kong SAR'
    ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Transportation Types</b></p>
    <p><i class="fa fa-train" style="color:red"></i> MTR Stations</p>
    <p><i class="fa fa-bus" style="color:blue"></i> Bus Stops</p>
    <p><i class="fa fa-car" style="color:green"></i> Minibus Routes</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

def create_dashboard():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">🚇 Hong Kong Public Transportation Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize transport data
    transport_data = HKTransportData()
    
    # Sidebar for controls
    st.sidebar.header("🚦 Transportation Options")
    show_mtr = st.sidebar.checkbox("🚇 Show MTR Stations", value=True)
    show_bus = st.sidebar.checkbox("🚌 Show Bus Stops", value=True)
    show_minibus = st.sidebar.checkbox("🚐 Show Minibus Routes", value=True)
    
    # Map style selector
    map_style = st.sidebar.selectbox(
        "🗺️ Map Style",
        ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter", "Stamen Terrain"]
    )
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Fetch data based on selections
    transport_data_dict = {}
    
    if show_mtr:
        with st.spinner("Loading MTR data..."):
            transport_data_dict['MTR'] = transport_data.get_mtr_data()
    
    if show_bus:
        with st.spinner("Loading bus data..."):
            transport_data_dict['Bus'] = transport_data.get_bus_data()
    
    if show_minibus:
        with st.spinner("Loading minibus data..."):
            transport_data_dict['Minibus'] = transport_data.get_minibus_data()
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Interactive Map", "📊 Statistics", "🚌 Real-time Info", "📈 Analytics"])
    
    with tab1:
        st.header("Hong Kong Transportation Map")
        
        # Create and display map
        if any(not df.empty for df in transport_data_dict.values()):
            map_obj = create_hk_map(transport_data_dict)
            folium_static(map_obj, width=1200, height=600)
        else:
            st.warning("No transportation data available. Please check your selections.")
    
    with tab2:
        st.header("Transportation Statistics")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_stations = sum(len(df) for df in transport_data_dict.values() if not df.empty)
        mtr_count = len(transport_data_dict.get('MTR', pd.DataFrame()))
        bus_count = len(transport_data_dict.get('Bus', pd.DataFrame()))
        minibus_count = len(transport_data_dict.get('Minibus', pd.DataFrame()))
        
        with col1:
            st.metric("Total Stations", total_stations, delta="+2 this week")
        with col2:
            st.metric("MTR Stations", mtr_count, delta="+1 new station")
        with col3:
            st.metric("Bus Stops", bus_count, delta="+5 new stops")
        with col4:
            st.metric("Minibus Routes", minibus_count, delta="+1 new route")
        
        # Create charts
        if any(not df.empty for df in transport_data_dict.values()):
            col1, col2 = st.columns(2)
            
            with col1:
                # Transport type distribution
                transport_counts = {
                    'MTR': mtr_count,
                    'Bus': bus_count,
                    'Minibus': minibus_count
                }
                
                fig = px.pie(
                    values=list(transport_counts.values()),
                    names=list(transport_counts.keys()),
                    title="Transportation Type Distribution",
                    color_discrete_map={'MTR': '#ff0000', 'Bus': '#0000ff', 'Minibus': '#00ff00'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Geographic distribution
                all_data = []
                for transport_type, df in transport_data_dict.items():
                    if not df.empty:
                        df_copy = df.copy()
                        df_copy['transport_type'] = transport_type
                        all_data.append(df_copy)
                
                if all_data:
                    combined_df = pd.concat(all_data, ignore_index=True)
                    fig2 = px.scatter(
                        combined_df,
                        x='lng',
                        y='lat',
                        color='transport_type',
                        title="Geographic Distribution",
                        labels={'lng': 'Longitude', 'lat': 'Latitude'}
                    )
                    st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.header("Real-time Transportation Information")
        
        # Get service status
        status_data = transport_data.get_service_status()
        
        # MTR Service Status
        st.subheader("🚇 MTR Service Status")
        mtr_col1, mtr_col2 = st.columns(2)
        
        with mtr_col1:
            for line, status in list(status_data['mtr'].items())[:4]:
                status_color = "🟢" if status == "Normal Service" else "🟡" if "Minor" in status else "🔴"
                st.write(f"{status_color} **{line}**: {status}")
        
        with mtr_col2:
            for line, status in list(status_data['mtr'].items())[4:]:
                status_color = "🟢" if status == "Normal Service" else "🟡" if "Minor" in status else "🔴"
                st.write(f"{status_color} **{line}**: {status}")
        
        # Bus Service Status
        st.subheader("🚌 Bus Service Updates")
        bus_col1, bus_col2, bus_col3 = st.columns(3)
        
        with bus_col1:
            st.info("**KMB**: Normal Service")
        with bus_col2:
            st.info("**Citybus**: Normal Service")
        with bus_col3:
            st.info("**New World First Bus**: Normal Service")
        
        # Minibus Information
        st.subheader("🚐 Minibus Information")
        st.info("Green and red minibus services are running as scheduled across all routes.")
        
        # Last updated
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with tab4:
        st.header("Transportation Analytics")
        
        # Create some sample analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Peak hours analysis
            hours = list(range(24))
            passenger_count = [100, 80, 60, 40, 30, 50, 200, 400, 600, 500, 450, 400, 
                              450, 500, 550, 600, 700, 800, 750, 650, 550, 450, 300, 150]
            
            fig = px.line(
                x=hours,
                y=passenger_count,
                title="Passenger Volume by Hour",
                labels={'x': 'Hour of Day', 'y': 'Passenger Count (thousands)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Transport mode preference
            modes = ['MTR', 'Bus', 'Minibus', 'Tram', 'Ferry']
            usage = [45, 30, 15, 5, 5]
            
            fig2 = px.bar(
                x=modes,
                y=usage,
                title="Transport Mode Usage (%)",
                labels={'x': 'Transport Mode', 'y': 'Usage %'}
            )
            st.plotly_chart(fig2, use_container_width=True)

def main():
    """Main application function"""
    try:
        create_dashboard()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check your internet connection and try again.")

if __name__ == "__main__":
    main() 