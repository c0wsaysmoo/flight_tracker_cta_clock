from datetime import datetime, timedelta
import requests as r
import pytz
import time
import json 

# Attempt to load config data
try:
    from config import TOMORROW_API_KEY
    from config import TEMPERATURE_UNITS
    from config import FORECAST_DAYS

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    TOMORROW_API_KEY = None
    TEMPERATURE_UNITS = "metric"
    FORECAST_DAYS = 3

if TEMPERATURE_UNITS != "metric" and TEMPERATURE_UNITS != "imperial":
    TEMPERATURE_UNITS = "metric"

from config import TEMPERATURE_LOCATION

# Weather API
TOMORROW_API_URL = "https://api.tomorrow.io/v4/"

def grab_temperature_and_humidity(delay=2):
    current_temp, humidity = None, None

    while True:
        try:
            request = r.get(
                f"{TOMORROW_API_URL}/weather/realtime",
                params={
                    "location": TEMPERATURE_LOCATION,
                    "units": TEMPERATURE_UNITS,
                    "apikey": TOMORROW_API_KEY
                }
            )
            request.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = request.json()["data"]["values"]
            current_temp, humidity = data["temperature"], data["humidity"]
            break  # If successful, exit the loop and return the temperature and humidity
        except r.exceptions.RequestException as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    return current_temp, humidity
    
def grab_rain(delay=2):
    while True:
        try:
            current_time = datetime.utcnow()
            
            resp = r.post(
                f"{TOMORROW_API_URL}/timelines",
                headers={
                    "Accept-Encoding": "gzip",
                    "accept": "application/json",
                    "content-type": "application/json"
                },
                params={"apikey": TOMORROW_API_KEY}, 
                json={
                    "location": TEMPERATURE_LOCATION,
                    "units": TEMPERATURE_UNITS,
                    "fields": [
                        "precipitationProbability"
                    ],
                    "timesteps": [
                        "1h"
                    ],
                    "startTime": current_time.isoformat(),
                    "endTime": (current_time + timedelta(hours=1)).isoformat()
                }
            )    
            resp.raise_for_status()
            
            # Return the intervals directly
            return resp.json()["data"]["timelines"][0].get("intervals", [])
        except (r.exceptions.RequestException, KeyError) as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

def grab_forecast(delay=2):
    while True:
        try:
            current_time = datetime.utcnow()
            dt = current_time + timedelta(hours=6)
            
            resp = r.post(
                f"{TOMORROW_API_URL}/timelines",
                headers={
                    "Accept-Encoding": "gzip",
                    "accept": "application/json",
                    "content-type": "application/json"
                },
                params={"apikey": TOMORROW_API_KEY}, 
                json={
                    "location": TEMPERATURE_LOCATION,
                    "units": TEMPERATURE_UNITS,
                    "fields": [
                        "sunriseTime",
                        "sunsetTime",
                        "moonPhase",
                        "precipitationProbability"
                    ],
                    "timesteps": [
                        "1d"
                    ],
                    "startTime": dt.isoformat(),
                    "endTime": (dt + timedelta(days=int(FORECAST_DAYS))).isoformat()
                }
            )    
            resp.raise_for_status()  # Fix the method name here
            
            # Print the raw JSON response for debugging
            #print("Raw JSON Response:")
            #print(json.dumps(resp.json(), indent=4))
            forecast = resp.json()["data"]["timelines"][0]["intervals"]
            return forecast
        except (r.exceptions.RequestException, KeyError) as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)