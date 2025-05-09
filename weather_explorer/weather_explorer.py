"""
Weather Explorer - A Data-Centric Weather Application
Final Project for Programming II
"""

import requests
import json
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os
import sys

class WeatherExplorer:
    def __init__(self):
        """Initialize the Weather Explorer application"""
        self.locations = {}
        self.current_data = None
        self.forecast_data = None
        print("\n=== Welcome to Weather Explorer ===")
        print("Get accurate weather information for any US location!\n")

    def validate_coordinates(self, lat, lon):
        """Validate that coordinates are within the expected range"""
        try:
            lat_float = float(lat)
            lon_float = float(lon)
            
            # Check latitude range (-90 to 90)
            if lat_float < -90 or lat_float > 90:
                return False, "Latitude must be between -90 and 90 degrees."
            
            # Check longitude range (-180 to 180)
            if lon_float < -180 or lon_float > 180:
                return False, "Longitude must be between -180 and 180 degrees."
                
            return True, (lat_float, lon_float)
        except ValueError:
            return False, "Coordinates must be valid numbers."
            
    def get_location_input(self):
        """Get and validate location input from the user"""
        print("\n--- Enter Location Coordinates ---")
        print("(Example: 34.7465, -92.2896 for Little Rock, AR)")
        
        while True:
            try:
                latitude = input("Enter latitude: ")
                longitude = input("Enter longitude: ")
                
                valid, result = self.validate_coordinates(latitude, longitude)
                if valid:
                    return result
                else:
                    print(f"Error: {result}")
            except KeyboardInterrupt:
                print("\nExiting application...")
                sys.exit(0)
                
    def fetch_weather_data(self, lat, lon):
        """Fetch weather data from the NWS API"""
        print(f"\nFetching weather data for coordinates: {lat}, {lon}...")
        
        try:
            # First, get the forecast URL from the points endpoint
            points_url = f"https://api.weather.gov/points/{lat},{lon}"
            response = requests.get(points_url, headers={"User-Agent": "Weather Explorer Application (educational project)"})
            response.raise_for_status()
            
            # Extract metadata and forecast URLs
            data = response.json()
            location_name = f"{data['properties']['relativeLocation']['properties']['city']}, {data['properties']['relativeLocation']['properties']['state']}"
            forecast_url = data['properties']['forecast']
            hourly_forecast_url = data['properties']['forecastHourly']
            
            # Get the forecast data
            forecast_response = requests.get(forecast_url)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            print(f"Successfully retrieved weather data for {location_name}!")
            
            # Save the current location and data
            self.locations[f"{lat},{lon}"] = location_name
            self.forecast_data = forecast_data
            
            return location_name, forecast_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch weather data. {str(e)}")
            return None, None
            
    def display_forecast(self, location_name, forecast_data):
        """Display the weather forecast in a user-friendly format"""
        if not forecast_data:
            print("No forecast data available.")
            return
            
        print(f"\n=== Weather Forecast for {location_name} ===")
        
        # Get the periods from the forecast
        periods = forecast_data["properties"]["periods"]
        
        for i, period in enumerate(periods):
            # Create a clean, formatted output for each period
            print(f"\n--- {period['name']} ---")
            print(f"Temperature: {period['temperature']}°{period['temperatureUnit']}")
            print(f"Conditions: {period['shortForecast']}")
            print(f"Wind: {period['windSpeed']} {period['windDirection']}")
            print(f"Details: {period['detailedForecast']}")
            
            # Only show the first 7 periods (usually 3-4 days)
            if i >= 6:
                print("\n... More forecast data available ...")
                break
                
    def plot_temperature_trend(self):
        """Create a visualization of temperature trends using Matplotlib"""
        if not self.forecast_data:
            print("No forecast data available for visualization.")
            return
            
        periods = self.forecast_data["properties"]["periods"]
        
        # Extract data for plotting
        days = []
        temps = []
        
        for period in periods[:14]:  # Use the first 14 periods (7 days)
            # Use shortened day names for the x-axis
            day_name = period['name'].split()[0]  # Get just the day part
            if day_name not in days:  # Avoid duplicates
                days.append(day_name)
            temps.append(period['temperature'])
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(temps)), temps, marker='o', linestyle='-', color='#1f77b4')
        
        # Add labels and title
        plt.title('7-Day Temperature Forecast', fontsize=16)
        plt.xlabel('Time Period', fontsize=12)
        plt.ylabel('Temperature (°F)', fontsize=12)
        
        # Set x-axis ticks and labels
        plt.xticks(range(len(temps)), [period['name'] for period in periods[:14]], rotation=45)
        
        # Add grid lines for readability
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add value labels on the points
        for i, temp in enumerate(temps):
            plt.text(i, temp + 1, f"{temp}°F", ha='center')
        
        plt.tight_layout()
        
        # Show the plot
        print("\nGenerating temperature trend visualization...")
        plt.savefig('temperature_trend.png')
        print("Visualization saved as 'temperature_trend.png'")
        plt.show()
        
    def save_weather_data(self):
        """Save the current weather data to a CSV file"""
        if not self.forecast_data:
            print("No weather data available to save.")
            return
            
        try:
            # Get the location information
            location = list(self.locations.values())[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"weather_data_{location.replace(', ', '_')}_{timestamp}.csv"
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header row
                writer.writerow(['Period', 'Temperature (°F)', 'Wind', 'Short Forecast', 'Detailed Forecast'])
                
                # Write data rows
                for period in self.forecast_data["properties"]["periods"]:
                    writer.writerow([
                        period['name'],
                        period['temperature'],
                        f"{period['windSpeed']} {period['windDirection']}",
                        period['shortForecast'],
                        period['detailedForecast']
                    ])
                    
            print(f"\nWeather data saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving weather data: {str(e)}")
            return None
            
    def compare_locations(self):
        """Compare weather across multiple locations"""
        locations_data = []
        
        print("\n--- Compare Weather Across Locations ---")
        print("Enter coordinates for up to 3 locations (or press Enter to stop):")
        
        for i in range(3):
            print(f"\nLocation {i+1}:")
            try:
                lat_lon = self.get_location_input()
                location_name, forecast_data = self.fetch_weather_data(lat_lon[0], lat_lon[1])
                
                if location_name and forecast_data:
                    locations_data.append({
                        'name': location_name,
                        'forecast': forecast_data
                    })
                    
                    # Ask if they want to add another location
                    if i < 2:
                        add_another = input("\nAdd another location? (y/n): ").lower()
                        if add_another != 'y':
                            break
            except KeyboardInterrupt:
                print("\nCancelling location comparison...")
                return
                
        if len(locations_data) < 2:
            print("Need at least 2 locations to compare. Operation cancelled.")
            return
            
        # Create comparison visualization
        plt.figure(figsize=(12, 6))
        
        markers = ['o', 's', '^']  # Different markers for different locations
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Different colors
        
        for i, location in enumerate(locations_data):
            # Extract data for plotting
            periods = location['forecast']["properties"]["periods"][:8]  # First 4 days (day/night)
            temps = [period['temperature'] for period in periods]
            labels = [period['name'] for period in periods]
            
            # Plot this location's data
            plt.plot(
                range(len(temps)), 
                temps, 
                marker=markers[i], 
                linestyle='-', 
                color=colors[i], 
                label=location['name']
            )
            
        # Add labels and title
        plt.title('Temperature Comparison Across Locations', fontsize=16)
        plt.xlabel('Time Period', fontsize=12)
        plt.ylabel('Temperature (°F)', fontsize=12)
        
        # Set x-axis ticks and labels from the first location
        plt.xticks(
            range(len(locations_data[0]['forecast']["properties"]["periods"][:8])), 
            [period['name'] for period in locations_data[0]['forecast']["properties"]["periods"][:8]], 
            rotation=45
        )
        
        # Add grid and legend
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        plt.tight_layout()
        
        # Show the plot
        print("\nGenerating temperature comparison visualization...")
        plt.savefig('temperature_comparison.png')
        print("Visualization saved as 'temperature_comparison.png'")
        plt.show()
        
    def display_menu(self):
        """Display the main menu and handle user choices"""
        while True:
            print("\n=== Weather Explorer Menu ===")
            print("1. Get weather for a location")
            print("2. Visualize temperature trend")
            print("3. Save weather data to CSV")
            print("4. Compare multiple locations")
            print("5. Exit application")
            
            try:
                choice = input("\nEnter your choice (1-5): ")
                
                if choice == '1':
                    lat_lon = self.get_location_input()
                    location_name, forecast_data = self.fetch_weather_data(lat_lon[0], lat_lon[1])
                    if location_name and forecast_data:
                        self.display_forecast(location_name, forecast_data)
                
                elif choice == '2':
                    if self.forecast_data:
                        self.plot_temperature_trend()
                    else:
                        print("Please get weather data for a location first (Option 1).")
                
                elif choice == '3':
                    self.save_weather_data()
                
                elif choice == '4':
                    self.compare_locations()
                
                elif choice == '5':
                    print("\nThank you for using Weather Explorer. Goodbye!")
                    sys.exit(0)
                
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
                    
            except KeyboardInterrupt:
                print("\nExiting application...")
                sys.exit(0)
                
    def run(self):
        """Run the Weather Explorer application"""
        try:
            self.display_menu()
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("The application will now exit.")
            sys.exit(1)

# Run the application if this file is executed directly
if __name__ == "__main__":
    app = WeatherExplorer()
    app.run()
