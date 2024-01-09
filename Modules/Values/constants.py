from Modules.Values.files import model

GSD = 0.0434

frames_per_second = 0.0416

user_input_minutes_raw_csv = 0.1  # Input in minutes
target_second_csv_raw = 60

#target_second_csv_raw = user_input_minutes_raw_csv * 60
user_input_minutes_zone_timer = 0.1
target_second_zone = user_input_minutes_zone_timer * 60

CLASS_NAMES_DICT = model.model.names


# zone processing
# zone_dict = polygon_zone()
# zone_vehicle_count = {zone_name: 0 for zone_name in zones_dict.keys()}

