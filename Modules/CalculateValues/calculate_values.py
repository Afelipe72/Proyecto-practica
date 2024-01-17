import math
import Modules
from Modules.Values.constants import GSD, frames_per_second


def get_center_bounding_box(coordinates_in_detection) -> list:
    x_center = (coordinates_in_detection[0] + coordinates_in_detection[2]) / 2
    y_center = (coordinates_in_detection[1] + coordinates_in_detection[3]) / 2
    bounding_box_center = [x_center, y_center]
    return bounding_box_center


def calculate_speed(previous_frame_coordinates, current_frame_coordinates) -> dict:
    c_speeds = {}
    for key in current_frame_coordinates:
        if key in previous_frame_coordinates:
            prev_x, prev_y = previous_frame_coordinates[key]
            current_x, current_y = current_frame_coordinates[key]
            x_change = (current_x - prev_x) * Modules.Values.constants.GSD / frames_per_second
            y_change = (current_y - prev_y) * Modules.Values.constants.GSD / frames_per_second
            speed_vehicle = math.sqrt(x_change ** 2 + y_change ** 2)
            c_speeds[key] = (x_change, y_change, speed_vehicle)
        else:
            c_speeds[key] = (0, 0, 0)
    return c_speeds


def calculate_acceleration(speed_x_y_total_previous_frame, speed_x_y_total_current_frame) -> dict:
    acceleration = {}
    for key in speed_x_y_total_current_frame:
        if key in speed_x_y_total_previous_frame:
            x_value_previous, y_value_previous, total_val_previous = speed_x_y_total_previous_frame[key]
            x_value_current, y_value_current, total_val_current = speed_x_y_total_current_frame[key]
            x_change = ((x_value_current - x_value_previous) / frames_per_second)*0.1
            y_change = ((y_value_current - y_value_previous) / frames_per_second)*0.1
            acceleration_vehicle = math.sqrt(x_change ** 2 + y_change ** 2)
            acceleration[key] = (x_change, y_change, acceleration_vehicle)
        else:
            acceleration[key] = (0, 0, 0)
    return acceleration

