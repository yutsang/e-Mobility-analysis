# Hong Kong Public Transportation Dashboard

A comprehensive Streamlit-based dashboard for visualizing Hong Kong's public transportation system, including MTR, buses, and minibuses with real-time data integration.

## 🚇 Features

- **Interactive Map**: OpenStreetMap-based visualization of Hong Kong with transportation data
- **Real-time Data**: Integration with government transportation APIs
- **Multiple Transport Modes**: MTR, Bus, and Minibus data visualization
- **Service Status**: Real-time service updates and status information
- **Analytics Dashboard**: Passenger volume analysis and transport mode usage statistics
- **Responsive Design**: Modern UI with customizable map styles

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd e-Mobility-analysis
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run hk_transport_enhanced.py
   ```

## 🚀 Usage

### Basic Usage
1. Open your web browser and navigate to `http://localhost:8501`
2. Use the sidebar to toggle different transportation modes
3. Explore the interactive map and various dashboard tabs

### Features Overview

#### 🗺️ Interactive Map Tab
- View all transportation stations and routes on an interactive map
- Click on markers for detailed information
- Toggle different transport modes using sidebar controls
- Customize map style (OpenStreetMap, CartoDB, etc.)

#### 📊 Statistics Tab
- View key metrics and statistics
- Interactive charts showing transportation distribution
- Geographic distribution analysis
- Real-time data updates

#### 🚌 Real-time Info Tab
- Live service status for all MTR lines
- Bus service updates from major operators
- Minibus route information
- Last updated timestamps

#### 📈 Analytics Tab
- Passenger volume analysis by hour
- Transport mode usage statistics
- Historical data trends
- Performance metrics

## 🔧 Configuration

### API Endpoints
The application integrates with the following government data sources:

- **MTR Open Data**: `https://opendata.mtr.com.hk`
- **KMB Bus Data**: `https://data.etabus.gov.hk`
- **Government Data**: `https://data.gov.hk`

### Customization
You can modify the following in the code:
- Map center coordinates (`HK_CENTER`)
- Hong Kong boundary coordinates (`HK_BOUNDARY`)
- Transportation data sources
- UI styling and colors
- Chart configurations

## 📊 Data Sources

### MTR (Mass Transit Railway)
- Station locations and line information
- Service status updates
- Real-time arrival data (where available)

### Bus Services
- KMB (Kowloon Motor Bus) routes and stops
- Citybus and New World First Bus information
- Bus stop locations and route details

### Minibus Services
- Green minibus routes and fares
- Red minibus information
- Route coverage areas

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile devices
- **Custom Styling**: Modern gradient headers and card-based layout
- **Interactive Elements**: Hover effects, popups, and tooltips
- **Color-coded Transport**: Different colors for each transport mode
- **Real-time Updates**: Automatic data refresh capabilities

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

2. **Map Not Loading**
   - Check internet connection (required for OpenStreetMap tiles)
   - Verify firewall settings

3. **API Data Not Loading**
   - Government APIs may have rate limits
   - Application includes fallback sample data
   - Check API endpoint availability

4. **Performance Issues**
   - Reduce the number of displayed markers
   - Use map zoom controls for better performance
   - Refresh data less frequently

### Error Messages

- **"Could not fetch MTR data"**: API temporarily unavailable, using sample data
- **"No transportation data available"**: Check sidebar selections
- **"An error occurred"**: Check internet connection and try refreshing

## 📈 Future Enhancements

- [ ] Real-time arrival predictions
- [ ] Route planning functionality
- [ ] Fare calculation features
- [ ] Historical data analysis
- [ ] Mobile app version
- [ ] Multi-language support (English/Chinese)
- [ ] Weather integration
- [ ] Crowding level indicators

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hong Kong Government for providing open transportation data
- MTR Corporation for their open data initiative
- KMB and other bus operators for data access
- OpenStreetMap contributors for map data
- Streamlit community for the excellent framework

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the documentation

---

**Note**: This application uses sample data when government APIs are unavailable. For production use, ensure proper API access and rate limiting compliance. 