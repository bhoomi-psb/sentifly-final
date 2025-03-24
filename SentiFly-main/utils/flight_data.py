import pandas as pd
import numpy as np
import requests
import os
import json
from datetime import datetime, timedelta
import random  # For demo purposes when API is not available

def get_flights(airline=None, status=None, region=None, search_term=None):
    """
    Get flight data from FlightAware API or another flight data source.
    
    Parameters:
    airline (str): Filter by airline name
    status (str): Filter by flight status 
    region (str): Filter by geographic region
    search_term (str): Search for specific flight number or route
    
    Returns:
    DataFrame: Pandas DataFrame containing flight data
    """
    # Check if API key is available
    api_key = os.getenv("FLIGHTAWARE_API_KEY")
    
    if api_key:
        try:
            # Real API implementation would go here
            # This is a placeholder for actual API call to FlightAware or similar service
            headers = {
                "x-apikey": api_key
            }
            
            # Build API request parameters
            params = {}
            if airline:
                params["airline"] = airline
            if status:
                params["status"] = status
            if region:
                params["region"] = region
            if search_term:
                params["query"] = search_term
            
            # Example API call (URL would need to be updated to actual API endpoint)
            # response = requests.get(
            #     "https://aeroapi.flightaware.com/aeroapi/flights",
            #     headers=headers,
            #     params=params
            # )
            
            # if response.status_code == 200:
            #     data = response.json()
            #     # Process API response into DataFrame
            #     # ...
            
            # For now, we'll generate sample data
            flights_data = generate_sample_flights(airline, status, region, search_term)
            return flights_data
        
        except Exception as e:
            print(f"Error fetching flight data: {str(e)}")
            # Fall back to sample data
            return generate_sample_flights(airline, status, region, search_term)
    else:
        # No API key, use sample data for development
        return generate_sample_flights(airline, status, region, search_term)

def get_flight_details(flight_id):
    """
    Get detailed information for a specific flight.
    
    Parameters:
    flight_id (str): The unique identifier for the flight
    
    Returns:
    dict: Detailed flight information
    """
    # Check if API key is available
    api_key = os.getenv("FLIGHTAWARE_API_KEY")
    
    if api_key:
        try:
            # Real API implementation would go here
            # This is a placeholder for actual API call
            headers = {
                "x-apikey": api_key
            }
            
            # Example API call
            # response = requests.get(
            #     f"https://aeroapi.flightaware.com/aeroapi/flights/{flight_id}",
            #     headers=headers
            # )
            
            # if response.status_code == 200:
            #     return response.json()
            
            # For now, return sample data
            return generate_sample_flight_details(flight_id)
        
        except Exception as e:
            print(f"Error fetching flight details: {str(e)}")
            return generate_sample_flight_details(flight_id)
    else:
        # No API key, use sample data
        return generate_sample_flight_details(flight_id)

def generate_sample_flights(airline=None, status=None, region=None, search_term=None):
    """
    Generate sample flight data for development and testing.
    
    Returns:
    DataFrame: Pandas DataFrame containing sample flight data
    """
    # Generate a random number of flights
    num_flights = random.randint(50, 200)
    
    # Define sample airlines including Indian airlines
    airlines = ["Air India", "IndiGo", "SpiceJet", "GoAir", "Air Asia India", "Vistara",
                "American Airlines", "Delta Air Lines", "United Airlines", 
                "Southwest Airlines", "JetBlue", "Alaska Airlines"]
    
    # Filter by specified airline if provided
    if airline and airline != "All Airlines":
        filtered_airlines = [airline]
    else:
        filtered_airlines = airlines
    
    # Define sample airports by region
    airports_by_region = {
        "North America": ["JFK", "LAX", "ORD", "ATL", "DFW", "SFO", "MIA", "SEA", "YYZ", "MEX"],
        "Europe": ["LHR", "CDG", "FRA", "AMS", "MAD", "FCO", "IST", "ZRH", "VIE", "ARN"],
        "Asia": ["DEL", "BOM", "MAA", "BLR", "HYD", "CCU", "COK", "TRV", "AMD", "GOI", "HND", "PVG", "HKG", "ICN", "SIN", "BKK", "KUL", "TPE", "MNL"],
        "South America": ["GRU", "EZE", "BOG", "SCL", "LIM", "BSB", "MVD", "CCS", "UIO", "ASU"],
        "Australia": ["SYD", "MEL", "BNE", "PER", "ADL", "CNS", "AKL", "CHC", "WLG", "NAN"],
        "Africa": ["JNB", "CPT", "CAI", "LOS", "ADD", "NBO", "CMN", "ALG", "TUN", "DAR"]
    }
    
    # Filter by region if provided
    if region and region != "All Regions":
        airports = airports_by_region.get(region, [])
        # Include some airports from other regions for international flights
        for r in airports_by_region:
            if r != region:
                airports.extend(random.sample(airports_by_region[r], 2))
    else:
        airports = []
        for r in airports_by_region:
            airports.extend(airports_by_region[r])
    
    # Define sample flight statuses
    statuses = ["En Route", "Scheduled", "Landed", "Delayed", "Diverted", "Cancelled"]
    
    # Filter by status if provided
    if status and status != "All Statuses":
        filtered_statuses = [status]
    else:
        filtered_statuses = statuses
    
    # Generate flight data
    flight_data = []
    
    for i in range(num_flights):
        airline_name = random.choice(filtered_airlines)
        airline_code = ''.join(word[0] for word in airline_name.split())[:2]
        
        flight_number = f"{airline_code}{random.randint(100, 9999)}"
        departure_airport = random.choice(airports)
        
        # Ensure arrival airport is different from departure
        arrival_candidates = [a for a in airports if a != departure_airport]
        arrival_airport = random.choice(arrival_candidates)
        
        status = random.choice(filtered_statuses)
        
        # Generate realistic departure and arrival times
        now = datetime.now()
        if status == "Scheduled":
            departure_time = now + timedelta(hours=random.randint(1, 24))
            flight_duration = timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + flight_duration
        elif status == "En Route":
            departure_time = now - timedelta(hours=random.randint(1, 6))
            flight_duration = timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + flight_duration
        elif status == "Landed":
            arrival_time = now - timedelta(hours=random.randint(0, 12))
            flight_duration = timedelta(hours=random.randint(1, 12))
            departure_time = arrival_time - flight_duration
        elif status == "Delayed":
            original_departure = now - timedelta(hours=random.randint(0, 3))
            departure_time = original_departure + timedelta(hours=random.randint(1, 5))
            flight_duration = timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + flight_duration
        elif status == "Diverted":
            departure_time = now - timedelta(hours=random.randint(1, 8))
            flight_duration = timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + flight_duration
        else:  # Cancelled
            departure_time = now + timedelta(hours=random.randint(1, 24))
            arrival_time = departure_time + timedelta(hours=random.randint(1, 12))
        
        # Generate realistic coordinates based on flight status
        if status == "En Route":
            # Generate a position somewhere between departure and arrival
            progress = random.random()  # 0 to 1, how far along the flight path
            
            # Very simplified calculation - real implementation would use great circle calculations
            # This just does a simple linear interpolation for demonstration
            latitude = random.uniform(20, 50)  # Simplified to general US/Europe latitudes
            longitude = random.uniform(-130, -70)  # Simplified to general US longitudes
            
            altitude = random.randint(25000, 40000)  # Typical cruising altitudes in feet
            ground_speed = random.randint(400, 600)  # Typical cruising speeds in knots
        else:
            # For non-en-route flights, set coordinates to the departure or arrival airport
            # This would normally come from a lookup table of airport coordinates
            latitude = random.uniform(20, 50)
            longitude = random.uniform(-130, -70)
            
            altitude = 0 if status in ["Landed", "Scheduled", "Cancelled"] else random.randint(0, 10000)
            ground_speed = 0 if status in ["Landed", "Scheduled", "Cancelled"] else random.randint(150, 350)
        
        # Generate a flight ID
        flight_id = f"FL{i:06d}"
        
        # Create the flight data entry
        flight_entry = {
            'flight_id': flight_id,
            'flight_number': flight_number,
            'airline': airline_name,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'ground_speed': ground_speed,
            'status': status,
            'departure_time': departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            'arrival_time': arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            'anomaly': random.random() < 0.05  # 5% chance of being flagged as an anomaly
        }
        
        # Apply search filter if provided
        if search_term:
            search_term = search_term.lower()
            if (search_term in flight_number.lower() or 
                search_term in departure_airport.lower() or 
                search_term in arrival_airport.lower() or
                search_term in airline_name.lower()):
                flight_data.append(flight_entry)
        else:
            flight_data.append(flight_entry)
    
    # Convert to DataFrame
    df = pd.DataFrame(flight_data)
    
    return df

def generate_sample_flight_details(flight_id):
    """
    Generate detailed information for a sample flight.
    
    Parameters:
    flight_id (str): The flight ID
    
    Returns:
    dict: Detailed flight information
    """
    # Generate airline information including Indian airlines
    airlines = ["Air India", "IndiGo", "SpiceJet", "GoAir", "Air Asia India", "Vistara",
                "American Airlines", "Delta Air Lines", "United Airlines", 
                "Southwest Airlines", "JetBlue", "Alaska Airlines"]
    airline = random.choice(airlines)
    airline_code = ''.join(word[0] for word in airline.split())[:2]
    
    # Generate flight number
    flight_number = f"{airline_code}{random.randint(100, 9999)}"
    
    # Generate airports including Indian airports
    airports = ["DEL", "BOM", "MAA", "BLR", "HYD", "CCU", "COK", "TRV", "AMD", "GOI", 
                "JFK", "LAX", "ORD", "ATL", "DFW", "SFO", "LHR", "CDG", "FRA", "AMS"]
    departure_airport = random.choice(airports)
    arrival_candidates = [a for a in airports if a != departure_airport]
    arrival_airport = random.choice(arrival_candidates)
    
    # Generate aircraft information
    aircraft_types = ["Boeing 737-800", "Boeing 787-9", "Airbus A320", "Airbus A321neo", "Boeing 777-300ER", "Airbus A350-900"]
    aircraft_type = random.choice(aircraft_types)
    registration = f"N{random.randint(100, 999)}{airline_code}"
    
    # Generate times
    now = datetime.now()
    departure_time = now - timedelta(hours=random.randint(1, 3))
    arrival_time = departure_time + timedelta(hours=random.randint(2, 10))
    
    # Generate status
    status = random.choice(["En Route", "Scheduled", "Landed", "Delayed", "Diverted", "Cancelled"])
    
    # Generate flight path
    num_waypoints = random.randint(5, 15)
    flight_path = []
    
    start_lat, start_lon = 35.0 + random.uniform(-5, 5), -100.0 + random.uniform(-20, 20)
    end_lat, end_lon = 40.0 + random.uniform(-5, 5), -80.0 + random.uniform(-20, 20)
    
    for i in range(num_waypoints):
        progress = i / (num_waypoints - 1)
        # Simple linear interpolation
        lat = start_lat + progress * (end_lat - start_lat) + random.uniform(-1, 1)
        lon = start_lon + progress * (end_lon - start_lon) + random.uniform(-1, 1)
        alt = random.randint(30000, 38000) if 0.1 < progress < 0.9 else random.randint(10000, 25000)
        spd = random.randint(450, 550) if 0.1 < progress < 0.9 else random.randint(250, 400)
        
        timestamp = departure_time + (arrival_time - departure_time) * progress
        
        flight_path.append({
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "latitude": lat,
            "longitude": lon,
            "altitude": alt,
            "ground_speed": spd
        })
    
    # Generate weather conditions
    weather = {
        "departure": {
            "temperature": random.randint(50, 85),
            "conditions": random.choice(["Clear", "Partly Cloudy", "Cloudy", "Rain", "Snow"]),
            "wind_speed": random.randint(0, 25),
            "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        },
        "arrival": {
            "temperature": random.randint(50, 85),
            "conditions": random.choice(["Clear", "Partly Cloudy", "Cloudy", "Rain", "Snow"]),
            "wind_speed": random.randint(0, 25),
            "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        },
        "en_route": [
            {
                "position": "Mid-flight",
                "conditions": random.choice(["Clear", "Cloudy", "Turbulence", "Storms Nearby"])
            }
        ]
    }
    
    # Generate flight details
    flight_details = {
        "flight_id": flight_id,
        "flight_number": flight_number,
        "airline": airline,
        "status": status,
        "aircraft": {
            "type": aircraft_type,
            "registration": registration,
            "age": random.randint(1, 15)
        },
        "departure": {
            "airport": departure_airport,
            "terminal": random.choice(["A", "B", "C", "D", "E"]),
            "gate": f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 30)}",
            "scheduled_time": (departure_time - timedelta(minutes=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            "actual_time": departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            "delay_minutes": random.randint(0, 60)
        },
        "arrival": {
            "airport": arrival_airport,
            "terminal": random.choice(["1", "2", "3", "4", "5"]),
            "gate": f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 30)}",
            "scheduled_time": (arrival_time - timedelta(minutes=random.randint(-30, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            "estimated_time": arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            "delay_minutes": random.randint(-15, 60)
        },
        "flight_path": flight_path,
        "weather": weather,
        "additional_info": {
            "meal_service": random.choice(["Yes", "No", "Premium Cabins Only"]),
            "wifi_available": random.choice(["Yes", "No", "Limited"]),
            "codeshare_with": random.choice([None, "BA", "LH", "AF", "DL", "UA"]),
            "on_time_performance": f"{random.randint(70, 98)}%"
        }
    }
    
    return flight_details
