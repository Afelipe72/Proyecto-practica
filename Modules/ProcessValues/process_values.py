import supervision as sv
import numpy as np
import cv2
import openpyxl
from openpyxl import load_workbook
# Method: process_polygon_zone
from Modules.Values.variables import processed_objects
# from Modules.Values.declare_polygon_zone import zone_vehicle_count

from ultralytics import YOLO


# Method: callback
import Modules
from Modules.Values.files import model
from Modules.Values.variables import current_frame, time_elapsed_reset, time_elapsed, zone_timer  # processed_objects

#from Modules.Values.declare_polygon_zone import zones_dict
from Modules.FormatValues.format_values import format_csv_values
from Modules.WriteValuesOnFiles.write_values_on_files import write_values_on_csv_raw, write_csv_polygon_zone
from Modules.Values.constants import CLASS_NAMES_DICT

# Method: process_polygon_zone
from Modules.Values.variables import processed_objects
#from Modules.Values.declare_polygon_zone import zone_vehicle_count
from Modules.Values.constants import CLASS_NAMES_DICT
from Modules.Values.files import excel_file_path_coordinates


# Method: polygon_zone
from Modules.WriteValuesOnFiles.write_values_on_files import create_excel_sheets

fps = 0
def gooey_receiver(args=None):
    global fps
    # Receives the Excel file with the coordinates
    Modules.Values.files.excel_file_path_coordinates = f"{args.Coordenadas}"
    # Receives the Excel file template
    Modules.Values.files.excel_file_path = f"{args.Plantilla}"
    # Receives the Yolo model
    Modules.Values.files.model = YOLO(f"{args.Modelo}")
    Modules.Values.constants.CLASS_NAMES_DICT = Modules.Values.files.model.model.names
    # Receives the GSD
    Modules.Values.constants.GSD = args.GSD
    # Sets the video resolution
    Modules.Values.files.video_info_resolution = f"{args.Video}"
    # Sets raw time threshold
    Modules.Values.constants.user_input_minutes_raw_csv = args.Frecuencia
    # Sets zone time threshold
    Modules.Values.constants.user_input_minutes_zone_timer = args.Rutas * 60
    # Gets the videos fps
    video_test = cv2.VideoCapture(f"{args.Video}")
    fps = round(video_test.get(cv2.CAP_PROP_FPS))
    Modules.Values.constants.frames_per_second = 1 / fps

    # Process the video
    sv.process_video(
        source_path=f"{args.Video}",
        target_path="result.mp4",
        callback=callback
    )


def polygon_zone() -> dict:
    polygon_zone_dict = {}
    video_info = sv.VideoInfo.from_video_path(Modules.Values.files.video_info_resolution)

    zones_dict = {}  # Dictionary to store zones and their annotators

    wb = load_workbook(Modules.Values.files.excel_file_path_coordinates)
    ws = wb.active

    num_rows = ws.max_row
    num_columns = ws.max_column

    for row in ws.iter_rows(min_row=2, min_col=1, max_row=num_rows, max_col=num_columns):
        list_test = []
        polygon_zone_name = None
        for cell in row:
            if cell.column == 1:
                polygon_zone_name = cell.value
            else:
                list_test.append(int(cell.value))
        if polygon_zone_name is not None:
            # Assuming the values are in pairs (x, y), adjust accordingly
            values = np.array(list(zip(list_test[::2], list_test[1::2])))
            polygon_zone_dict[polygon_zone_name] = values

            zone = sv.PolygonZone(polygon=polygon_zone_dict[polygon_zone_name], frame_resolution_wh=video_info.resolution_wh)
            zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color(255, 225, 6), thickness=2, text_thickness=1, text_scale=1, text_padding=0)

            zones_dict[polygon_zone_name] = {
                'zone': zone,
                'annotator': zone_annotator,
                'tracked_vehicles': set(),
                'vehicle_count': 0,
                'polygon_zone_dict': [int(list_test[2]), int(list_test[3])]
            }

            create_excel_sheets(zones_dict)

    return zones_dict

tracker_id_to_zone_id = {}
counts = {}

def update_tracker_info(detections_in_zones, detections) -> sv.Detections:
    global tracker_id_to_zone_id, counts
    detections_all = detections
    for zone_id, detections_zone in enumerate(detections_in_zones):
        for tracker_id in detections_zone.tracker_id:
            tracker_id_to_zone_id.setdefault(tracker_id, zone_id)

    for zone_id, detections_zone in enumerate(detections_in_zones):
        for tracker_id in detections_zone.tracker_id:
            if tracker_id in tracker_id_to_zone_id:
                zone_in_id = tracker_id_to_zone_id[tracker_id]
                counts.setdefault(zone_id, {})
                counts[zone_id].setdefault(zone_in_id, set())
                counts[zone_id][zone_in_id].add(tracker_id)

    # Update class_id in detections_all based on tracker_id_to_zone_id
    detections_all.class_id = np.vectorize(
        lambda x: tracker_id_to_zone_id.get(x, -1)
    )(detections_all.tracker_id)

    # Filter out detections with class_id == -1
    return detections_all[detections_all.class_id != -1]



def process_polygon_zone(zones_dict, detections, frame):
    zone_vehicle_count = {zone_name: 0 for zone_name in zones_dict.keys()}
    # Testing
    detections_in_zone = []

    for zone_name, zone_data in zones_dict.items():
        zone = zone_data['zone']
        tracked_vehicles = zone_data['tracked_vehicles']
        zone_coordinates = zone_data['polygon_zone_dict']
        vehicle_count = zone_vehicle_count[zone_name]

        zone.trigger(detections=detections)
        mask = zone.trigger(detections=detections)
        in_zone_detections = detections[mask]
        zone_objects = Modules.Values.variables.processed_objects.get(zone_name, [])

        # Accumulate detections for each zone
        for i, detection in enumerate(in_zone_detections):
            tracker_id = detection[4]

            if tracker_id not in tracked_vehicles:
                # Increment the vehicle count
                zone_vehicle_count[zone_name] = 1
                tracked_vehicles.add(tracker_id)

                class_id = int(detection[3])
                class_names = Modules.Values.constants.CLASS_NAMES_DICT.get(class_id)
                confidence = round(float(detection[2]) * 100)

                data_to_accumulate = {
                    'vehicle_count': zone_vehicle_count[zone_name],
                    'tracker_id': tracker_id,
                    'class_id': class_id,
                    'class_names': class_names,
                    'confidence': confidence
                }

                zone_objects.append(data_to_accumulate)
        # Store the objects for the current zone in the dictionary
        Modules.Values.variables.processed_objects[zone_name] = zone_objects

        # Testing
        # Accumulate detections for all zones
        detections_in_zone.append(in_zone_detections)

        cv2.putText(frame, zone_name, zone_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        frame = zone_data['annotator'].annotate(scene=frame)

    return Modules.Values.variables.processed_objects, detections_in_zone


tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator(text_scale=0.5, text_padding=1)
trace_annotator = sv.TraceAnnotator(trace_length=100)
mask_annotator = sv.MaskAnnotator()
polygon_annotator = sv.PolygonAnnotator()
corner_annotator = sv.BoxCornerAnnotator()



zones_dict = None


def callback(frame: np.ndarray, _: int) -> np.ndarray:
    global zones_dict, fps
    if not Modules.Values.variables.header_written_process_polygon_zone:
        zones_dict = polygon_zone()
        Modules.Values.variables.header_written_process_polygon_zone = True
    # Process frame
    results = Modules.Values.files.model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    Modules.Values.variables.current_frame += 1

    Modules.Values.variables.time_elapsed_reset += 1 / fps
    format_time_elapsed_reset = f"{Modules.Values.variables.time_elapsed_reset: 0.3f}"
    format_time_elapsed_reset_to_float = float(format_time_elapsed_reset)

    # sv.plot_image(image=frame, size=(16, 16))

    # For the raw_csv without resetting
    Modules.Values.variables.time_elapsed += 1 / fps
    Modules.Values.variables.format_time_elapsed = f"{Modules.Values.variables.time_elapsed: 0.3f}"

    # Process for the raw csv Values
    # for car_value in range(len(detections)):
        # values_to_csv = format_csv_values(detections.tracker_id[car_value], detections.xyxy[car_value],
        #                                   Modules.Values.constants.CLASS_NAMES_DICT.get(detections.class_id[car_value]),detections.confidence[car_value])
        # writes value
        # if abs(format_time_elapsed_reset_to_float - Modules.Values.constants.user_input_minutes_raw_csv) < 0.01:  # Modules.Values.constants.user_input_minutes_raw_csv
            # write_values_on_csv_raw(values_to_csv)
    # resets value
    print(format_time_elapsed_reset_to_float)
    if abs(format_time_elapsed_reset_to_float - Modules.Values.constants.user_input_minutes_raw_csv) < 0.01: # Modules.Values.constants.user_input_minutes_raw_csv
        Modules.Values.variables.time_elapsed_reset = 0

    # Process the polygon zone
    process_polygon_zone(zones_dict, detections, frame)

    # Polygon zone timer
    Modules.Values.variables.zone_timer += 1 / fps
    Modules.Values.variables.format_time_elapsed_test = f"{Modules.Values.variables.zone_timer: 0.3f}"
    print(Modules.Values.variables.format_time_elapsed_test)
    if abs(float(Modules.Values.variables.format_time_elapsed_test) - Modules.Values.constants.user_input_minutes_zone_timer) < 0.01:
        write_csv_polygon_zone(process_polygon_zone(zones_dict, detections, frame))
        Modules.Values.variables.processed_objects = {}
        Modules.Values.variables.zone_timer = 0


    processed_objects_test, detections_in_zone = process_polygon_zone(zones_dict, detections, frame)
    # detections = sv.Detections.merge(detections_in_zone)
    # detections = update_tracker_info(detections_in_zone, detections)

    labels = [
        f"#{tracker_id}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(
        scene=frame.copy(), detections=detections)

    return box_annotator.annotate(
        annotated_frame, detections=detections)

    # # fix labels
    # labels = [
    #     f"#{tracker_id}"
    #     for class_id, tracker_id
    #     in zip(detections.class_id, detections.tracker_id)
    # ]







