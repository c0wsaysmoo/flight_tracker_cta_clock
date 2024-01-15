from datetime import datetime, timedelta
from utilities.animator import Animator
from setup import colours, fonts, frames, screen
from utilities.temperature import grab_forecast, grab_rain

from rgbmatrix import graphics

import logging

# Configure logging
#logging.basicConfig(filename='/home/flight/its-a-plane-python/rain.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setup
TEXT_FONT = fonts.extrasmall
DISTANCE_FROM_TOP = 11
RAIN_REFRESH = 600


class RainScene(object):
    def __init__(self):
        super().__init__()
        self._last_api_call_time = None
        self._cached_forecast = None
        self._cached_rain = None
        self._last_rain_str = None
        self._redraw_forecast = True  # Initialize to True for the first refresh
        
        
    def colour_gradient(self, colour_A, colour_B, ratio):
        return graphics.Color(
            colour_A.red + ((colour_B.red - colour_A.red) * ratio),
            colour_A.green + ((colour_B.green - colour_A.green) * ratio),
            colour_A.blue + ((colour_B.blue - colour_A.blue) * ratio),
        )

    @Animator.KeyFrame.add(frames.PER_SECOND)
    def rain(self, count):
        #logging.debug("Entering rain method.")
        if len(self._data):
            self._redraw_forecast = True
            return

        # Check if enough time has passed since the last API call
        seconds_since_update = (datetime.now() - self._last_api_call_time).seconds if self._last_api_call_time is not None else 0
        if self._redraw_forecast or seconds_since_update >= RAIN_REFRESH:
            # Undraw old precipitation probability
            if self._last_rain_str is not None:
                self.draw_square(40, 6, 64, 10, colours.BLACK)

            if self._cached_forecast is not None and self._redraw_forecast:
                pass
            else:
                #logging.debug("Making API call for new forecast and rain data...")
                self._cached_forecast = grab_rain()
                self._cached_rain = grab_forecast()
                self._last_api_call_time = datetime.now()
                            
            self._redraw_forecast = False


            # Extract forecast
            precipitation_probability = self._cached_forecast[0]['values']['precipitationProbability']
            rain_ratio = self._cached_rain[0]["values"]["precipitationProbability"] / 100.0

            # Format the string
            self._last_rain_str = f"{precipitation_probability * 0.01:.0%}"

            rain_colour = self.colour_gradient(colours.WHITE, colours.BLUE, rain_ratio)

            # Calculate the offset to center the text
            space_width = 4
            rain_width = len(self._last_rain_str) * space_width
            offset = (40 + 64) // 2 - rain_width // 2

            #logging.debug("Drawing precipitation probability.")
            # Draw precipitation probability for the current hour
            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                offset,
                DISTANCE_FROM_TOP,
                rain_colour,
                self._last_rain_str  # Add the text argument here
            )
        #logging.debug("Exiting rain method.")
