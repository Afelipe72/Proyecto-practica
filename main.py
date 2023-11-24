import numpy as np
import math
import supervision as sv
from supervision import Point
from ultralytics import YOLO
import csv


model = YOLO("yolov8x.pt")
tracker = sv.ByteTrack()

box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()

coordinates = {}
previous_frame_bounding_box = {}
previous_speeds_to_acceleration = {}
current_frame = 0
time_elapsed = 0
vx, vy, vt = 0, 0, 0
ax, ay, at = 0, 0, 0
format_time_elapsed = ""
format_time_elapsed_test = ""
header_written_raw_csv = False
header_written_zone = False
CLASS_NAMES_DICT = model.model.names

GSD = 0.08687
frames_per_second = 0.0333

accumulated_data = []
zone_timer = 0
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

            x_change = (current_x - prev_x) * GSD / frames_per_second
            y_change = (current_y - prev_y) * GSD / frames_per_second
            speed_vehicle = math.sqrt(x_change ** 2 + y_change ** 2)
            c_speeds[key] = (x_change, y_change, speed_vehicle)
        else:
            c_speeds[key] = (0, 0, 0)
    return c_speeds


def calculate_acceleration(speed_x_y_total_previous_frame, speed_x_y_total_current_frame) -> dict:
    acceleration = {}
    for key in speed_x_y_total_previous_frame:
        if key in speed_x_y_total_current_frame:
            x_value_previous, y_value_previous, total_val_previous = speed_x_y_total_previous_frame[key]
            x_value_current, y_value_current, total_val_current = speed_x_y_total_current_frame[key]
            x_change = (x_value_current - x_value_previous) / frames_per_second
            y_change = (y_value_current - y_value_previous) / frames_per_second
            acceleration_vehicle = math.sqrt(x_change ** 2 + y_change ** 2)
            acceleration[key] = (
                f"{x_change:.9f}",
                f"{y_change:.9f}",
                f"{acceleration_vehicle:.9f}"
            )
        else:
            acceleration[key] = (0, 0, 0)
    return acceleration


def format_csv_values(tracker_id, bounding_box_anchors, class_id, confidence_value) -> list:
    global coordinates, previous_frame_bounding_box, previous_speeds_to_acceleration, GSD, \
        format_time_elapsed, vx, vy, vt, ax, ay, at
    car_id = tracker_id
    bounding_box_center = get_center_bounding_box(bounding_box_anchors)
    coordinates[car_id] = bounding_box_center

    speed_to_csv = calculate_speed(previous_frame_bounding_box, coordinates)
    accelerations_to_csv = calculate_acceleration(previous_speeds_to_acceleration, speed_to_csv)

    for _ in speed_to_csv:
        if car_id in speed_to_csv:
            vx, vy, vt = speed_to_csv[car_id]

    for _ in accelerations_to_csv:
        if car_id in accelerations_to_csv:
            ax, ay, at = accelerations_to_csv[car_id]

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


def write_values_on_csv_raw(csv_values):
    global header_written_raw_csv
    if not header_written_raw_csv:
        vehicles_csv_header = ['Frame', 'Tiempo(S)', 'Tipo de vehiculo', '% Certeza', 'Id Vehículo', 'X (Coordenadas)',
                               'Y (Coordenadas)', 'X (m)', 'Y (m)', 'Vx (m/s)', 'Vy(m/s)', 'Vt(m/s)', 'Ax(m/s)',
                               'Ay(m/s)', 'At(m/s)']
        with open('raw.csv', 'a', newline='') as vehicles_csv:
            writer = csv.writer(vehicles_csv)
            writer.writerow(vehicles_csv_header)

        header_written_raw_csv = True

    # Open the CSV file in append mode and write the values
    with open('raw.csv', 'a', newline='') as vehicles_csv:
        writer = csv.writer(vehicles_csv)
        writer.writerow(csv_values)


def polygon_zone() -> dict:
    polygon_zone_dict = {}
    video_info = sv.VideoInfo.from_video_path("vehicle-counting.mp4")
    number_of_entries = int(input("number of entries"))

    zones_dict = {}  # Dictionary to store zones and their annotators

    for i in range(1, number_of_entries + 1):
        polygon_zone_name = input('polygon zone name\n')
        x1 = int(input('x1\n '))
        y1 = int(input('y1\n '))

        x2 = int(input('x2\n '))
        y2 = int(input('y2\n '))

        x3 = int(input('x3\n '))
        y3 = int(input('y3\n '))

        x4 = int(input('x4\n '))
        y4 = int(input('y4\n '))
        polygon_zone_dict[polygon_zone_name] = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

        zone = sv.PolygonZone(polygon=polygon_zone_dict[polygon_zone_name], frame_resolution_wh=video_info.resolution_wh)
        zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color(0, 0, 255), thickness=4, text_thickness=8, text_scale=4)

        zones_dict[polygon_zone_name] = {'zone': zone, 'annotator': zone_annotator, 'tracked_vehicles': set(),
                                         'vehicle_count': 0}

    return zones_dict


zones_dict = polygon_zone()
zone_vehicle_count = {zone_name: 0 for zone_name in zones_dict.keys()}

passed_vehicles_set = set()

def process_polygon_zone(zones_dict, detections, frame):
    processed_objects = []

    for zone_name, zone_data in zones_dict.items():
        zone = zone_data['zone']
        zone_annotator = zone_data['annotator']
        tracked_vehicles = zone_data['tracked_vehicles']
        vehicle_count = zone_vehicle_count[zone_name]

        print(f"Processing zone: {zone_name}")

        zone.trigger(detections=detections)
        mask = zone.trigger(detections=detections)
        in_zone_detections = detections[mask]

        for i, detection in enumerate(in_zone_detections):
            tracker_id = detection[4]

            if tracker_id not in tracked_vehicles:
                # Increment the vehicle count
                zone_vehicle_count[zone_name] += 1
                tracked_vehicles.add(tracker_id)

            class_id = int(detection[3])
            class_names = CLASS_NAMES_DICT.get(class_id)
            confidence = round(float(detection[2]) * 100)

            data_to_accumulate = {
                'vehicle_count': vehicle_count,
                'tracker_id': tracker_id,
                'class_id': class_id,
                'class_names': class_names,
                'confidence': confidence,
            }
            processed_objects.append(data_to_accumulate)

        frame = zone_annotator.annotate(scene=frame)

    print(
        f"{processed_objects}")

    return processed_objects

def write_csv_polygon_zone(accumulated_data):
    global header_written_zone

    for accumulated_data_values in accumulated_data:
        print(accumulated_data_values)

    if not header_written_zone:
        vehicles_csv_header = ['zone_name', 'passed_vehicles', 'tracker_id', 'class_id', 'class_names', 'confidence']
        with open('csv_routes.csv', 'a', newline='') as polygon_zone_csv:
            writer = csv.writer(polygon_zone_csv)
            writer.writerow(vehicles_csv_header)

        header_written_zone = True


    # Open the CSV file in append mode and write the values
    with open('csv_routes.csv', 'a', newline='') as polygon_zone_csv:
        writer = csv.writer(polygon_zone_csv)
        writer.writerow(accumulated_data)

# line_zone
# test = sv.LineZone(start=Point(2029, 704), end=Point(2262, 620))
# line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=1, text_scale=1)
# test.trigger(detections=detections)
# line_annotator.annotate(frame=frame, line_counter=test)


def callback(frame: np.ndarray, _: int) -> np.ndarray:
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    global current_frame, time_elapsed, format_time_elapsed, CLASS_NAMES_DICT, zones_dict, zone_timer, accumulated_data,\
        format_time_elapsed_test
    current_frame += 1
    time_elapsed += 1 / 30
    format_time_elapsed = f"{time_elapsed: 0.3f}"

    for car_value in range(len(detections)):
        values_to_csv = format_csv_values(detections.tracker_id[car_value], detections.xyxy[car_value],
                                          CLASS_NAMES_DICT.get(detections.class_id[car_value]), detections.confidence[car_value])
        write_values_on_csv_raw(values_to_csv)

    process_polygon_zone(zones_dict, detections, frame)

    zone_timer += 1 / 30
    format_time_elapsed_test = f"{zone_timer: 0.3f}"
    print(format_time_elapsed_test)
    if abs(float(format_time_elapsed_test) - 1.0) < 0.001:
        print("daslklmñasklmñadmklñas")
        write_csv_polygon_zone(process_polygon_zone(zones_dict, detections, frame))
        accumulated_data = []
        zone_timer = 0

    labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]
    annotated_frame = box_annotator.annotate(
        frame.copy(), detections=detections)

    annotated_frame = label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels)

    return trace_annotator.annotate(
        annotated_frame, detections=detections)


sv.process_video(
    source_path="vehicle-counting.mp4",
    target_path="result.mp4",
    callback=callback
)
