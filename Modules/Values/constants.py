from Modules.Values.files import model

GSD = 0
# Calle 100 GSD: 0.08687

frames_per_second = 0.333

user_input_minutes_raw_csv = None  # Input in minutes
# target_second_csv_raw = user_input_minutes_raw_csv * 60

#target_second_csv_raw = user_input_minutes_raw_csv * 60
user_input_minutes_zone_timer = 0.1
target_second_zone = user_input_minutes_zone_timer * 60

CLASS_NAMES_DICT = model.model.names
