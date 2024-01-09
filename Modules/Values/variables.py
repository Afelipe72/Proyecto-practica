from Modules.ProcessValues.process_values import polygon_zone

coordinates = {}
previous_frame_bounding_box = {}
previous_speeds_to_acceleration = {}
current_frame = 0
time_elapsed = 0
time_elapsed_reset = 0
vx, vy, vt = 0, 0, 0
ax, ay, at = 0, 0, 0
format_time_elapsed = ""
format_time_elapsed_test = ""
header_written_raw_csv = False
header_written_zone = False

accumulated_data = []

zone_timer = 0


processed_objects = {}


counter_header_file = 0
counter_zone_timer = 0
vehicle_counter_zone_timer = 0


zones_dict = polygon_zone()
zone_vehicle_count = {zone_name: 0 for zone_name in zones_dict.keys()}
