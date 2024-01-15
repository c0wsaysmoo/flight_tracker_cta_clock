from datetime import datetime
import requests as r
import pytz
import time
import json
from config import CTA_API_KEY
from config import STATION_ID
from config import NUMBER_OF_TRAINS
from config import END_STOP
from config import END_STOP_2 

# CTA API
CTA_API_URL = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"

def grab_trains(delay=2):
    # Initialize variables with default values for the first 3 trains to O'Hare
    next_train_1_arrival = next_train_1_aoe = next_train_1_is_app = next_train_1_is_dly = next_train_1_last = None
    next_train_2_arrival = next_train_2_aoe = next_train_2_is_dly = next_train_2_last = None
    next_train_3_arrival = next_train_3_aoe = next_train_3_is_dly = next_train_3_last = None

    # Initialize variables with default values for the first 3 trains to Forest Park
    next_train2_1_arrival = next_train2_1_aoe = next_train2_1_is_app = next_train2_1_is_dly = next_train2_1_last = None
    next_train2_2_arrival = next_train2_2_aoe = next_train2_2_is_dly = next_train2_2_last = None
    next_train2_3_arrival = next_train2_3_aoe = next_train2_3_is_dly = next_train2_3_last = None

    while True:  # Infinite loop for continuous attempts
        try:
            request = r.get(
                CTA_API_URL,
                params={
                    "key": CTA_API_KEY,
                    "outputType": "json",
                    "mapid": STATION_ID,
                }
            )
            request.raise_for_status()
            data = request.json()["ctatt"]["eta"]

            # Filter trains 1
            next_train_1 = [train for train in data if train["destNm"] == END_STOP]

            # Extract arrival time, estimated arrival time, isApp, and isDly for the first 3 trains 1
            if len(next_train_1) >= NUMBER_OF_TRAINS:
                next_train_1_arrival = next_train_1[0]["arrT"]
                next_train_1_last = next_train_1[0]["prdt"]
                next_train_1_aoe = "Act" if next_train_1[0]["isSch"] == "0" else "Est"
                next_train_1_is_app = "Due" if next_train_1[0]["isApp"] == "1" else ""
                next_train_1_is_dly = "Delay" if next_train_1[0]["isDly"] == "1" else ""

                next_train_2_arrival = next_train_1[1]["arrT"]
                next_train_2_last = next_train_1[1]["prdt"]
                next_train_2_aoe = "Act" if next_train_1[1]["isSch"] == "0" else "Est"
                next_train_2_is_dly = "Delay" if next_train_1[1]["isDly"] == "1" else ""

                next_train_3_arrival = next_train_1[2]["arrT"]
                next_train_3_last = next_train_1[2]["prdt"]
                next_train_3_aoe = "Act" if next_train_1[2]["isSch"] == "0" else "Est"
                next_train_3_is_dly = "Delay" if next_train_1[2]["isDly"] == "1" else ""
            else:
                next_train_1_arrival = next_train_1_aoe = next_train_1_is_app = next_train_1_is_dly = None
                next_train_2_arrival = next_train_2_aoe = next_train_2_is_dly = None
                next_train_3_arrival = next_train_3_aoe = next_train_3_is_dly = None

            # Filter trains 2
            next_train2_1 = [train for train in data if train["destNm"] == END_STOP_2]

            # Extract arrival time, estimated arrival time, isApp, and isDly for the first 3 trains 2
            if len(next_train2_1) >= 1:
                next_train2_1_arrival = next_train2_1[0]["arrT"]
                next_train2_1_last = next_train2_1[0]["prdt"]
                next_train2_1_aoe = "Act" if next_train2_1[0]["isSch"] == "0" else "Est"
                next_train2_1_is_app = "Due" if next_train2_1[0]["isApp"] == "1" else ""
                next_train2_1_is_dly = "Delay" if next_train2_1[0]["isDly"] == "1" else ""
            else:
                next_train2_1_arrival = next_train2_1_aoe = next_train2_1_is_app = next_train2_1_is_dly = "NA"

            if len(next_train2_1) >= 2:
                next_train2_2_arrival = next_train2_1[1]["arrT"]
                next_train2_2_last = next_train2_1[1]["prdt"]
                next_train2_2_aoe = "Act" if next_train2_1[1]["isSch"] == "0" else "Est"
                next_train2_2_is_dly = "Delay" if next_train2_1[1]["isDly"] == "1" else ""
            else:
                next_train2_2_arrival = next_train2_2_aoe = next_train2_2_is_dly = "NA"

            if len(next_train2_1) >= 3:
                next_train2_3_arrival = next_train2_1[2]["arrT"]
                next_train2_3_last = next_train2_1[2]["prdt"]
                next_train2_3_aoe = "Act" if next_train2_1[2]["isSch"] == "0" else "Est"
                next_train2_3_is_dly = "Delay" if next_train2_1[2]["isDly"] == "1" else ""
            else:
                next_train2_3_arrival = next_train2_3_aoe = next_train2_3_is_dly = "NA"

            break  # If successful, exit the loop

        except r.exceptions.RequestException as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    return (
        next_train_1_arrival,
        next_train_1_last,
        next_train_1_aoe,
        next_train_1_is_app,
        next_train_1_is_dly,
        next_train_2_arrival,
        next_train_2_last,
        next_train_2_aoe,
        next_train_2_is_dly,
        next_train_3_arrival,
        next_train_3_last,
        next_train_3_aoe,
        next_train_3_is_dly,
        next_train2_1_arrival,
        next_train2_1_last,
        next_train2_1_aoe,
        next_train2_1_is_app,
        next_train2_1_is_dly,
        next_train2_2_arrival,
        next_train2_2_last,
        next_train2_2_aoe,
        next_train2_2_is_dly,
        next_train2_3_arrival,
        next_train2_3_last,
        next_train2_3_aoe,
        next_train2_3_is_dly
    )

# Example usage:
(
    next_train_1_arrival,
    next_train_1_last,
    next_train_1_aoe,
    next_train_1_is_app,
    next_train_1_is_dly,
    next_train_2_arrival,
    next_train_2_last,
    next_train_2_aoe,
    next_train_2_is_dly,
    next_train_3_arrival,
    next_train_3_last,
    next_train_3_aoe,
    next_train_3_is_dly,
    next_train2_1_arrival,
    next_train2_1_last,
    next_train2_1_aoe,
    next_train2_1_is_app,
    next_train2_1_is_dly,
    next_train2_2_arrival,
    next_train2_2_last,
    next_train2_2_aoe,
    next_train2_2_is_dly,
    next_train2_3_arrival,
    next_train2_3_last,
    next_train2_3_aoe,
    next_train2_3_is_dly
) = grab_trains()

print(f"Next Train 1 Arrival Time: {next_train_1_arrival}, Last Train 1 {next_train_1_last}, WiFi or ETA: {next_train_1_aoe}, isApp: {next_train_1_is_app}, isDly: {next_train_1_is_dly}")
print(f"Next Train 2 Arrival Time: {next_train_2_arrival}, Last Train 2 {next_train_2_last}, WiFi or ETA: {next_train_2_aoe}, isDly: {next_train_2_is_dly}")
print(f"Next Train 3 Arrival Time: {next_train_3_arrival}, Last Train 3 {next_train_3_last}, WiFi or ETA: {next_train_3_aoe}, isDly: {next_train_3_is_dly}")
print(f"Next Train 1 Arrival Time: {next_train2_1_arrival}, Last Train 1 {next_train2_1_last}, WiFi or ETA: {next_train2_1_aoe}, isApp: {next_train2_1_is_app}, isDly: {next_train2_1_is_dly}")
print(f"Next Train 2 Arrival Time: {next_train2_2_arrival}, Last Train 2 {next_train2_2_last}, WiFi or ETA: {next_train2_2_aoe}, isDly: {next_train2_2_is_dly}")
print(f"Next Train 3 Arrival Time: {next_train2_3_arrival}, Last Train 3 {next_train2_3_last}, WiFi or ETA: {next_train2_3_aoe}, isDly: {next_train2_3_is_dly}")
