from modules.files import model

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
CLASS_NAMES_DICT = model.model.names

accumulated_data = []

zone_timer = 0


processed_objects = {}