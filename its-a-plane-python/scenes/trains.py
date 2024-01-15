from datetime import datetime, timedelta
from utilities.animator import Animator
from setup import colours, fonts, frames, screen
from rgbmatrix import graphics
from utilities import trainsdata
import time
from config import STOP_DISPLAY_NAME
from config import STOP_DISPLAY_NAME_2
import logging

# logging.basicConfig(filename='train_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Setup
TRAIN_COLOURS = colours.WHITE
TRAIN_COLOURS2 = colours.WHITE
TEXT_FONT = fonts.small
DISTANCE_FROM_TOP = 32
STATION_REFRESH_SECONDS = 30

class CTATrainScene(object):
    def __init__(self):
        super().__init__()
        self._cached_trains = None
        self._seconds_last_update = 0
        self._redraw_station = True
        self.TRAIN_COLOURS = colours.WHITE
        self.TRAIN_COLOURS2 = colours.WHITE
        self.TRAIN_COLOURS_1 = colours.WHITE  # You might need to initialize this based on your requirements
        self.TRAIN_COLOURS_2 = colours.WHITE
        self.TRAIN_COLOURS_3 = colours.WHITE
        self.TRAIN_COLOURS2_1 = colours.WHITE
        self.TRAIN_COLOURS2_1 = colours.WHITE
        self.TRAIN_COLOURS2_1 = colours.WHITE        

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def train(self, count):
        if len(self._data):
            self._redraw_station = True
            return

        # Ensure redraw when there's new data
        self._seconds_last_update += 1
        if self._seconds_last_update >= STATION_REFRESH_SECONDS or self._redraw_station:
            self._seconds_last_update = 0

            # Reset _redraw_forecast to True after regular refresh
            self._redraw_station = True

            # Use cached train data if available and redraw is requested
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
            ) = trainsdata.grab_trains()

            self._cached_trains = (
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
            self._redraw_station = False

            # Clear the current numbers by redrawing the square
            if self._cached_trains is not None:
                self.draw_square(
                    0,
                    18,  # Start from the bottom of the screen (32 - 20)
                    64,  # Width of the area
                    31,  # Height of the area
                    colours.TROPICAL_BLUE,
                )
            # Check if arrival times are available for trains to O'Hare
            if (next_train_1_arrival and
                next_train_2_arrival and
                next_train_3_arrival):
                # Calculate time difference between scheduled and actual arrival times for O'Hare trains
                arrival_time_1 = datetime.strptime(next_train_1_arrival, "%Y-%m-%dT%H:%M:%S")
                last_time_1 = datetime.strptime(next_train_1_last, "%Y-%m-%dT%H:%M:%S")

                if next_train_2_arrival and next_train_2_arrival != 'NA':
                    arrival_time_2 = datetime.strptime(next_train_2_arrival, "%Y-%m-%dT%H:%M:%S")
                else:
                    arrival_time_2 = None  # or set a default datetime if necessary
                if next_train_2_last:
                    last_time_2 = datetime.strptime(next_train_2_last, "%Y-%m-%dT%H:%M:%S")
                else:
                    last_time_2 = None  # or set a default datetime if necessary

                if next_train_3_arrival and next_train_3_arrival != 'NA':
                    arrival_time_3 = datetime.strptime(next_train_3_arrival, "%Y-%m-%dT%H:%M:%S")
                else:
                    arrival_time_3 = None  # or set a default datetime if necessary
                if next_train_3_last:
                    last_time_3 = datetime.strptime(next_train_3_last, "%Y-%m-%dT%H:%M:%S")
                else:
                    last_time_3 = None  # or set a default datetime if necessary

                time_difference_1 = arrival_time_1 - last_time_1
                if arrival_time_2 or last_time_2:
                    time_difference_2 = arrival_time_2 - last_time_2
                    Train_2 = str(int(time_difference_2.total_seconds() / 60)).zfill(2)
                else:
                    time_difference_2 = timedelta()
                    Train_2 = "NA"
                if arrival_time_3 or last_time_3:
                    time_difference_3 = arrival_time_3 - last_time_3
                    Train_3 = str(int(time_difference_3.total_seconds() / 60)).zfill(2)
                else:
                    time_difference_3 = timedelta()
                    Train_3 = "NA"

                # Convert the time differences to minutes and pad with leading zeros
                time_difference_1_minutes = int(time_difference_1.total_seconds() / 60)
                time_difference_2_minutes = int(time_difference_2.total_seconds() / 60)
                time_difference_3_minutes = int(time_difference_3.total_seconds() / 60)

                # Convert to strings and pad with leading zeros
                time_difference_1_str = str(time_difference_1_minutes).zfill(2)
                time_difference_2_str = str(time_difference_2_minutes).zfill(2)
                time_difference_3_str = str(time_difference_3_minutes).zfill(2)

                # Assign information for O'Hare trains with time differences
                Train_1 = time_difference_1_str
                Train_2 = time_difference_2_str
                Train_3 = time_difference_3_str
            else:
                # Set default values if there is no train information
                Train_1 = "NA"
                Train_2 = "NA"
                Train_3 = "NA"

            # Set text color to GREEN_LIGHT when the train is "Due"
            if next_train_1_is_app == "Due":
                Train_1 = time_difference_1_str
                self.TRAIN_COLOURS_1 = colours.GREEN_LIGHT
            # Set text color to RED_LIGHT when the arrival is estimated
            elif next_train_1_aoe == "Est":
                Train_1 = time_difference_1_str
                self.TRAIN_COLOURS_1 = colours.RED_LIGHT
            # Set text to "DL" when the train is delayed
            elif next_train_1_is_dly == "Delay":
                Train_1 = "DL"
                self.TRAIN_COLOURS_1 = colours.RED_LIGHT
            else:
                self.TRAIN_COLOURS_1 = colours.WHITE


            # Set text color to RED_LIGHT when the arrival is estimated
            if next_train_2_aoe == "Est":
                Train_2 = time_difference_2_str
                self.TRAIN_COLOURS_2 = colours.RED_LIGHT
            # Set text to "DL" when the train is delayed
            elif next_train_2_is_dly == "Delay":
                Train_2 = "DL"
                self.TRAIN_COLOURS_2 = colours.RED_LIGHT
            else:
                self.TRAIN_COLOURS_2 = colours.WHITE


            # Set text color to RED_LIGHT when the arrival is estimated
            if next_train_3_aoe == "Est":
                Train_3 = time_difference_3_str
                self.TRAIN_COLOURS_3 = colours.RED_LIGHT
            # Set text to "DL" when the train is delayed
            elif next_train_3_is_dly == "Delay":
                Train_3 = "DL"
                self.TRAIN_COLOURS_3 = colours.RED_LIGHT
            else:
                self.TRAIN_COLOURS_3 = colours.WHITE

            # Set O_Hare_1 to "N/A" if next_train_1_last is None
            if next_train_1_last is None:
                Train_1 = "NA"

            # Set O_Hare_2 to "N/A" if next_train_2_last is None
            if next_train_2_last is None:
                Train_2 = "NA"

            # Set O_Hare_3 to "N/A" if next_train_3_last is None
            if next_train_3_last is None:
                Train_3 = "NA"

            text_length = len(STOP_DISPLAY_NAME)
            available_space = 16  # the first 15 pixels
            character_width = 5  # width of each character

            # Calculate the starting position to center the text within the first 15 pixels
            start_position = (available_space - text_length * character_width) // 2

            # Draw the centered text
            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                start_position,
                25,
                TRAIN_COLOURS,
                STOP_DISPLAY_NAME
            )

            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                20,
                25,
                self.TRAIN_COLOURS_1,
                Train_1
            )

            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                35,
                25,
                self.TRAIN_COLOURS_2,
                Train_2
            )

            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                50,
                25,
                self.TRAIN_COLOURS_3,
                Train_3
            )

            # Check if arrival times are available for trains to Forest Park
            if (next_train2_1_arrival and
                next_train2_2_arrival and
                next_train2_3_arrival):
                # Calculate time difference between scheduled and actual arrival times for Forest Park trains
                arrival_time2_1 = datetime.strptime(next_train2_1_arrival, "%Y-%m-%dT%H:%M:%S")
                last_time2_1 = datetime.strptime(next_train2_1_last, "%Y-%m-%dT%H:%M:%S")

                if next_train2_2_arrival and next_train2_2_arrival != 'NA':
                    arrival_time2_2 = datetime.strptime(next_train2_2_arrival, "%Y-%m-%dT%H:%M:%S")
                else:
                    arrival_time2_2 = None  # or set a default datetime if necessary
                if next_train2_2_last:
                    last_time2_2 = datetime.strptime(next_train2_2_last, "%Y-%m-%dT%H:%M:%S")
                else:
                    last_time2_2 = None  # or set a default datetime if necessary

                if next_train2_3_arrival and next_train2_3_arrival != 'NA':
                    arrival_time2_3 = datetime.strptime(next_train2_3_arrival, "%Y-%m-%dT%H:%M:%S")
                else:
                    arrival_time2_3 = None  # or set a default datetime if necessary
                if next_train2_3_last:
                    last_time2_3 = datetime.strptime(next_train2_3_last, "%Y-%m-%dT%H:%M:%S")
                else:
                    last_time2_3 = None  # or set a default datetime if necessary


                time_difference2_1 = arrival_time2_1 - last_time2_1
                if arrival_time2_2 or last_time2_2:
                    time_difference2_2 = arrival_time2_2 - last_time2_2
                    Train2_2 = str(int(time_difference2_2.total_seconds() / 60)).zfill(2)
                else:
                    time_difference2_2 = timedelta()
                    Train2_2 = "NA"
                if arrival_time2_3 or last_time2_3:
                    time_difference2_3 = arrival_time2_3 - last_time2_3
                    Train2_3 = str(int(time_difference2_3.total_seconds() / 60)).zfill(2)
                else:
                    time_difference2_3 = timedelta()
                    Train2_3 = "NA"

                # Convert the time differences to minutes and pad with leading zeros
                time_difference2_1_minutes = int(time_difference2_1.total_seconds() / 60)
                time_difference2_2_minutes = int(time_difference2_2.total_seconds() / 60)
                time_difference2_3_minutes = int(time_difference2_3.total_seconds() / 60)

                # Convert to strings and pad with leading zeros
                time_difference2_1_str = str(time_difference2_1_minutes).zfill(2)
                time_difference2_2_str = str(time_difference2_2_minutes).zfill(2)
                time_difference2_3_str = str(time_difference2_3_minutes).zfill(2)

                # Assign information for Forest Park trains with time differences
                Train2_1 = time_difference2_1_str
                Train2_2 = time_difference2_2_str
                Train2_3 = time_difference2_3_str
            else:
                # Set default values if there is no train information
                Train2_1 = "NA"
                Train2_2 = "NA"
                Train2_3 = "NA"

            # Set text color to GREEN_LIGHT when the train is "Due"
            if next_train2_1_is_app == "Due":
                Train2_1 = time_difference2_1_str
                self.TRAIN_COLOURS2_1 = colours.GREEN_LIGHT
            # Set text color to RED_LIGHT when the arrival is estimated
            elif next_train2_1_aoe == "Est":
                Train2_1 = time_difference2_1_str
                self.TRAIN_COLOURS2_1 = colours.RED_LIGHT
            # Set text to "DL" when the train is delayed
            elif next_train2_1_is_dly == "Delay":
                Train2_1 = "DL"
                self.TRAIN_COLOURS2_1 = colours.RED_LIGHT
            else:
                self.TRAIN_COLOURS2_1 = colours.WHITE


            # Set text color to RED_LIGHT when the arrival is estimated
            if next_train2_2_aoe == "Est":
                Train2_2 = time_difference2_2_str
                self.TRAIN_COLOURS2_2 = colours.RED_LIGHT
            # Set text to "DL" when the train is delayed
            elif next_train2_2_is_dly == "Delay":
                Train2_2 = "DL"
                self.TRAIN_COLOURS2_2 = colours.RED_LIGHT
            else:
                self.TRAIN_COLOURS2_2 = colours.WHITE

            # Set text color to RED_LIGHT when the arrival is estimated
            if next_train2_3_aoe == "Est":
                Train2_3 = time_difference2_3_str
                self.TRAIN_COLOURS2_3 = colours.RED_LIGHT
            # Set text to "DL" when the train is delayed
            elif next_train2_3_is_dly == "Delay":
                Train2_3 = "DL"
                self.TRAIN_COLOURS2_3 = colours.RED_LIGHT
            else:
                self.TRAIN_COLOURS2_3 = colours.WHITE

            # Set ForestPark_1 to "N/A" if next_train2_1_last is None
            if next_train2_1_last is None:
                Train2_1 = "NA"

            # Set ForestPark_2 to "N/A" if next_train2_2_last is None
            if next_train2_2_last is None:
                Train2_2 = "NA"

            # Set ForestPark_3 to "N/A" if next_train2_3_last is None
            if next_train2_3_last is None:
                Train2_3 = "NA"

            text_length = len(STOP_DISPLAY_NAME_2)
            available_space = 16  # the first 15 pixels
            character_width = 5  # width of each character

            # Calculate the starting position to center the text within the first 15 pixels
            start_position = (available_space - text_length * character_width) // 2

            # Draw the centered text
            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                start_position,
                32,
                TRAIN_COLOURS,
                STOP_DISPLAY_NAME_2
            )

            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                20,
                32,  # Adjust the Y-coordinate to separate the two sets of train information
                self.TRAIN_COLOURS2_1,
                Train2_1
            )

            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                35,
                32,  # Adjust the Y-coordinate to separate the two sets of train information
                self.TRAIN_COLOURS2_2,
                Train2_2
            )

            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                50,
                32, #Adjust the Y-coordinate to separate the two sets of train information
                self.TRAIN_COLOURS2_3,
                Train2_3
            )