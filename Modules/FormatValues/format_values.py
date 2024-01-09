# Method: format_csv_values
import Modules
from Modules.CalculateValues.calculate_values import get_center_bounding_box, calculate_speed, calculate_acceleration
from Modules.Values.variables import coordinates, previous_frame_bounding_box, previous_speeds_to_acceleration, current_frame, format_time_elapsed, vx, vy, vt, ax, ay, at
from Modules.Values.constants import GSD
# Method: format_report_values
from Modules.WriteValuesOnFiles.write_values_on_files import write_excel_file


def format_csv_values(tracker_id, bounding_box_anchors, class_id, confidence_value) -> list:
    car_id = tracker_id
    bounding_box_center = get_center_bounding_box(bounding_box_anchors)
    coordinates[car_id] = bounding_box_center

    speed_to_csv = calculate_speed(previous_frame_bounding_box, coordinates)
    accelerations_to_csv = calculate_acceleration(previous_speeds_to_acceleration, speed_to_csv)

    for _ in speed_to_csv:
        if car_id in speed_to_csv:
            Modules.Values.variables.vx, Modules.Values.variables.vy, Modules.Values.variables.vt = speed_to_csv[car_id]

    for _ in accelerations_to_csv:
        if car_id in accelerations_to_csv:
            Modules.Values.variables.ax, Modules.Values.variables.ay, Modules.Values.variables.at = accelerations_to_csv[car_id]

    csv_values = [current_frame, format_time_elapsed, class_id,
                  confidence_value * 100, car_id, bounding_box_center[0],
                  bounding_box_center[1], bounding_box_center[0] * GSD, bounding_box_center[1] * GSD,
                  vx, vy, vt, ax, ay, at
                  ]
    # speed
    for car_id in coordinates:
        if car_id not in previous_frame_bounding_box:
            previous_frame_bounding_box[car_id] = coordinates[car_id]

    for car_id in coordinates:
        previous_frame_bounding_box[car_id] = coordinates[car_id]

    # acceleration
    for car_id in speed_to_csv:
        if car_id not in previous_speeds_to_acceleration:
            previous_speeds_to_acceleration[car_id] = speed_to_csv[car_id]

    for car_id in speed_to_csv:
        previous_speeds_to_acceleration[car_id] = speed_to_csv[car_id]

    return csv_values


def format_report_values(car_zone_value_list):
    # Assuming the vehicle types are always at every 4th position in the list
    vehicle_types = car_zone_value_list[3::4]
    # Assuming the zone timers are always at every 4th position in the list
    zone_timers = car_zone_value_list[1::4]
    # Assuming the zone names are always at every 4th position in the list
    zone_names = car_zone_value_list[::4]

    # Create a dictionary to store counts and zone timers for each zone
    zone_counts = {}

    for vehicle_type, zone_timer, zone_name in zip(vehicle_types, zone_timers, zone_names):
        if zone_name not in zone_counts:
            # If the zone name is not in the dictionary, add it
            zone_counts[zone_name] = {}

        if vehicle_type not in zone_counts[zone_name]:
            # If the vehicle type is not in the inner dictionary, add it
            zone_counts[zone_name][vehicle_type] = {'Zone timer': zone_timer, 'Count': 0}

        # Add 1 to the count for the corresponding vehicle type in the given zone
        zone_counts[zone_name][vehicle_type]['Count'] += 1

    # Pass the argument to the write_excel_file method
    write_excel_file(zone_counts)
