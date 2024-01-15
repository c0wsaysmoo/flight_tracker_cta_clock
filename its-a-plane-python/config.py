ZONE_HOME = {
    "tl_y": xx.xxxxx, # Top-Left Latitude (deg) After finding your address make your own "box" around it. I usually go ~3.5 miles in each direction but depends how many planes you want to see and where you live
    "tl_x": xx.xxxxx, # Top-Left Longitude (deg)
    "br_y": xx.xxxxx, # Bottom-Right Latitude (deg)
    "br_x": xx.xxxxx # Bottom-Right Longitude (deg)
}
LOCATION_HOME = [
    xx.xxxxx, # Latitude (deg) #use your address here https://www.latlong.net/
    xx.xxxxx # Longitude (deg)
]
TEMPERATURE_LOCATION = "xx.xxxxxxx,xx.xxxxxx" #usually the same as location_home
TOMORROW_API_KEY = "xxxxx" # Get an API key from https://tomorrow.io
TEMPERATURE_UNITS = "imperial" #can also use "metric" if you'd like
DISTANCE_UNITS = "imperial" #can also use "metric" if you'd like
CLOCK_FORMAT = "12hr" #use 12hr or 24hr
MIN_ALTITUDE = 2600 #feet
BRIGHTNESS = 100
GPIO_SLOWDOWN = 1
JOURNEY_CODE_SELECTED = "ORD" #use your local airport
JOURNEY_BLANK_FILLER = " ? "
HAT_PWM_ENABLED = True
FORECAST_DAYS = 1 
CTA_API_KEY = "xxxxx" # go here https://www.transitchicago.com/developers/traintrackerapply/ to apply for a api key
STATION_ID = 40380 #can be found here https://www.transitchicago.com/developers/ttdocs/
END_STOP = "O'Hare" #Top train end of the line stop must be spelled as listed
END_STOP_2 = "Forest Park" #Other direction end of the line stop must be spelled as listed
STOP_DISPLAY_NAME = "ORD" #what it actually shows up as on display max digits 3
STOP_DISPLAY_NAME_2 = "FP" #what it actually shows up as on display max digits 3