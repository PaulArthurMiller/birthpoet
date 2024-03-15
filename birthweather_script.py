# An OpenAI Assistant which looks up the weather on an entered date (birthdate),
# then writes a heartwarming note from the person's mom about the weather that day.

import requests
import os
import math
from math import radians, cos, sin, sqrt, atan2
from datetime import datetime
import json
from log_config import logging


# Testing env variable
# test_var = os.getenv('NOAA_KEY_TOKEN')
# print(f"Test Variable: {test_var}")


# Get inputs of birthdate and birth city/location.

# std_birthdate = input("What is the birthdate (MM-DD-YYYY): ")
# std_birthloc = input("Where did the birth occur (city, state): ")

# def show_json(obj):
#     print(json.loads(obj.model_dump_json))

def get_birthweather(std_birthdate, std_birthloc):
    formatted_date = format_date_if_needed(std_birthdate)
    city, state = parse_location(std_birthloc)
    latitude, longitude = get_coordinates(city, state)
    north, west, south, east = calculate_bounding_box(latitude, longitude, distance=50)
    stations = find_stations(north, west, south, east)
    st_latitudes, st_longitudes, st_names, st_ids = get_station_info(stations)
    closest_name, closest_id = find_closest(latitude, longitude, st_latitudes, st_longitudes, st_names, st_ids)
    data = find_data(formatted_date, closest_id)
    weather_details = extract_weather_details(data)
    return weather_details

def format_date_if_needed(std_birthdate):
    try:
        # Attempt to parse the date with the expected format
        datetime.strptime(std_birthdate, "%Y-%m-%d")
        # If parsing succeeds, the date is already in the correct format
        return std_birthdate
    except ValueError:
        # If parsing fails (throws a ValueError), the date is not in the expected format
        # Here, you would apply your formatting logic to correct the date format
        # Assuming you have a function 'format_date' that reformats the date correctly
        return format_date(std_birthdate)

def format_date(std_birthdate):
    date_formats = [
    "%Y-%m-%d",  # YYYY-MM-DD
    "%Y/%m/%d",  # YYYY/MM/DD
    "%m-%d-%Y",  # MM-DD-YYYY
    "%m/%d/%Y",  # MM/DD/YYYY
    "%d-%m-%Y",  # DD-MM-YYYY
    "%d/%m/%Y",  # DD/MM/YYYY
    "%B %d, %Y",  # January 01, 2023
    "%b. %d, %Y",  # Jan. 01, 2023
    "%d %B %Y",  # 01 January 2023
    "%d %b. %Y"   # 01 Jan. 2023
]
    
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(std_birthdate, date_format)
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            return formatted_date 
        except ValueError:
            continue
    return None

def parse_location(std_birthloc):
    try: 
        city, state = std_birthloc.split(", ")
        return city, state
    except ValueError:
        logging.error("Tool Error: Please enter the location in the format 'City, State'.")
        return None, None

def get_coordinates(city, state):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&state={state}&format=json"
    response = requests.get(url)
    data = response.json() 
    
    if data:
        latitude = data[0]["lat"]
        longitude = data[0]["lon"]
        logging.info('Tool: Latitude, longitude found.')
        return latitude, longitude
    else:
        logging.error('Tool Error: No coordinate information found.')
        return None, None

def calculate_bounding_box(latitude, longitude, distance=50):
    lat = float(latitude)
    lon = float(longitude)

    lat_rad = math.radians(lat)
    
    delta_lat = distance / 69
    delta_lon = distance / (math.cos(lat_rad) * 69)
    
    north = lat + delta_lat
    south = lat - delta_lat
    east = lon + delta_lon
    west = lon - delta_lon

    north = round(north, 3)
    south = round(south, 3)
    east = round(east, 3)
    west = round(west, 3)
    
    return north, west, south, east

def find_stations(north, west, south, east):
    noaa_key_token = os.getenv('NOAA_KEY_TOKEN')
    if noaa_key_token is not None:
        logging.info("Tool: NOAA Key Token found!")
    else:
        logging.error("Tool: NOAA Key Token not found. Please set it as an environment variable.")
        
    headers = {
        'token' : noaa_key_token
        }
    url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/stations?extent={south},{west},{north},{east}&startdate=2023-12-31&enddate=1923-01-01"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        stations = response.json()
        logging.info('Tool: Found stations!')
        return stations
    else:
        logging.error(f"Tool: Failed to find stations: {response.text}")
        return None

# north, west, south, east = calculate_bounding_box(latitude, longitude)
# print(f'Bounding box coordinates: {north}, {west}, {south}, {east}')

# stations = find_stations(north, west, south, east)
# print(json.dumps(stations, indent=4))

def get_station_info(stations):
    station_info = stations['results']
    st_latitudes = []
    st_longitudes = []
    st_names = []
    st_ids = []

    for info in station_info :
        st_latitude = info.get('latitude')
        st_longitude = info.get('longitude')
        st_name = info.get('name')
        st_id = info.get('id')

        st_latitudes.append(st_latitude)
        st_longitudes.append(st_longitude)
        st_names.append(st_name)
        st_ids.append(st_id)

    return st_latitudes, st_longitudes, st_names, st_ids

def find_closest(latitude, longitude, st_latitudes, st_longitudes, st_names, st_ids):
    st_distances = []
    for st_latitude, st_longitude in zip(st_latitudes, st_longitudes):
        lat2 = st_latitude
        lon2 = st_longitude
        st_distance = calculate_distance(latitude, longitude, lat2, lon2)
        st_distances.append(st_distance)
    closest_index = st_distances.index(min(st_distances))
    closest_name, closest_id = st_names[closest_index], st_ids[closest_index]
    return closest_name, closest_id


def calculate_distance(latitude, longitude, lat2, lon2):
    R = 6371.0

    lat1 = float(latitude)
    lon1 = float(longitude)
    lat2 = float(lat2)
    lon2 = float(lon2)

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def find_data(formatted_date, closest_id):
    start_date = formatted_date#'1998-01-25'
    end_date = formatted_date#'1998-12-27'

    noaa_key_token = os.getenv('NOAA_KEY_TOKEN')
    if noaa_key_token is not None:
        logging.info("Tool data step: NOAA Key Token found!")
    else:
        logging.error("Tool data step: NOAA Key Token not found. Please set it as an environment variable.")
        
    headers = {
        'token' : noaa_key_token
        }
    url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid={closest_id}&startdate={start_date}&enddate={end_date}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        logging.info('Tool: Found data!')
        return data
    else:
        logging.error(f"Tool: Failed to find data: {response.text}")
        return None

def extract_weather_details(data):
    weather_details = {
        "high_temp": None,
        "low_temp": None,
        "precipitation_amount": None,
        "snow_amount": None,
        "precipitation_type": None,
    }

    for result in data["results"]:
        datatype = result["datatype"]
        value = result["value"]
        
        if datatype == "TMAX":
            weather_details["high_temp"] = (value / 10.0) * (9/5) + 32
        elif datatype == "TMIN":
            weather_details["low_temp"] = (value / 10.0) * (9/5) + 32
        elif datatype == "PRCP":
            weather_details["precipitation_amount"] = (value / 10.0)/ 25.4
        elif datatype == "SNOW":
            weather_details["snow_amount"] = (value / 10.0)/ 25.4

    if weather_details["snow_amount"] and weather_details["snow_amount"] > 0:
        weather_details["precipitation_type"] = "Snow"
    elif weather_details["precipitation_amount"] and weather_details["precipitation_amount"] > 0:
        weather_details["precipitation_type"] = "Rain"
    else:
        weather_details["precipitation_type"] = "None"
        
    return weather_details

    # noaa_key_token = os.getenv('NOAA_KEY_TOKEN')
    # if noaa_key_token is not None:
    #     print("NOAA Key Token found!")
    # else:
    #     print("NOAA Key Token not found. Please set it as an environment variable.")
        
    # headers = {
    #     'X-API-KEY' : noaa_key_token
    #     }

    # url = f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations={closest_id}&startDate={start_date}&endDate={end_date}&format=json&includeStationName=true'

    # response = requests.get(url, headers=headers)
    # return response
# north, west, south, east = calculate_bounding_box(latitude, longitude)
# print(f'Bounding box coordinates: {north}, {west}, {south}, {east}')
# closest_name, closest_id = find_closest(st_latitudes, st_longitudes, st_names, st_ids)
# print(f'Closest station is {closest_name}, with ID {closest_id}')
# data = find_data(formatted_date, closest_id)

# print(json.dumps(data, indent=4))


# def get_birth_weather(data_id):
#     pass




# First NOAA connection: search for correct NOAA dataID based on date and location.
# Parse JSON and extract dataID.
# May need a connection to Google Maps to identify nearest weather reporting station
# to the location input.

# Second connection: get specifics for the day's weather, including temps, precip,
# cloudcover, winds, storm events, etc. Parse JSON and extract, place in string.

# Structure inputs and weather data as a prompt for OpenAI model.

