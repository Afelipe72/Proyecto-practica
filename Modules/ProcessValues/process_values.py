import supervision as sv
import numpy as np
import cv2

# Method: polygon_zone
from Modules.WriteValuesOnFiles.write_values_on_files import create_excel_sheets

# Method: process_polygon_zone
from Modules.Values.variables import processed_objects, zone_vehicle_count

# Method: callback
import Modules
from Modules.Values.files import model
from Modules.Values.variables import zones_dict, current_frame, time_elapsed_reset, time_elapsed, zone_timer  # processed_objects
from Modules.FormatValues.format_values import format_csv_values
from Modules.WriteValuesOnFiles.write_values_on_files import write_values_on_csv_raw, write_csv_polygon_zone
from Modules.Values.constants import target_second_csv_raw, CLASS_NAMES_DICT


def polygon_zone() -> dict:
    polygon_zone_dict = {}
    video_info = sv.VideoInfo.from_video_path("DJI_0846.mp4")
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
        zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color(255, 225, 6), thickness=2, text_thickness=1, text_scale=1, text_padding=0)

        zones_dict[polygon_zone_name] = {
            'zone': zone,
            'annotator': zone_annotator,
            'tracked_vehicles': set(),
            'vehicle_count': 0,
            'polygon_zone_dict': [x2 + 60, y2 + 10]
        }

        create_excel_sheets(zones_dict)

    return zones_dict


def process_polygon_zone(zones_dict, detections, frame):
    for zone_name, zone_data in zones_dict.items():
        zone = zone_data['zone']
        zone_annotator = zone_data['annotator']
        tracked_vehicles = zone_data['tracked_vehicles']
        zone_coordinates = zone_data['polygon_zone_dict']
        vehicle_count = zone_vehicle_count[zone_name]

        zone.trigger(detections=detections)
        mask = zone.trigger(detections=detections)
        in_zone_detections = detections[mask]
        zone_objects = processed_objects.get(zone_name, [])

        for i, detection in enumerate(in_zone_detections):
            tracker_id = detection[4]

            if tracker_id not in tracked_vehicles:
                # Increment the vehicle count
                zone_vehicle_count[zone_name] = 1
                tracked_vehicles.add(tracker_id)

                class_id = int(detection[3])
                class_names = CLASS_NAMES_DICT.get(class_id)
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
            processed_objects[zone_name] = zone_objects

        cv2.putText(frame, zone_name, zone_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 2, cv2.LINE_AA)
        frame = zone_annotator.annotate(scene=frame)

    return processed_objects


def gooey_receiver(args=None):
    sv.process_video(
        source_path=f"{args.video}",
        target_path="result.mp4",
        callback=callback
    )


def callback(frame: np.ndarray, _: int) -> np.ndarray:
    # Process frame
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    Modules.Values.variables.current_frame += 1
    Modules.Values.variables.time_elapsed_reset += 1 / 30
    format_time_elapsed_reset = f"{Modules.Values.variables.time_elapsed_reset: 0.3f}"
    format_time_elapsed_reset_to_float = float(format_time_elapsed_reset)

    # sv.plot_image(image=frame, size=(16, 16))

    Modules.Values.variables.time_elapsed += 1 / 30
    format_time_elapsed = f"{Modules.Values.variables.time_elapsed: 0.3f}"
    print(format_time_elapsed)
    # Process for the raw csv Values
    for car_value in range(len(detections)):
        values_to_csv = format_csv_values(detections.tracker_id[car_value], detections.xyxy[car_value],
                                          CLASS_NAMES_DICT.get(detections.class_id[car_value]), detections.confidence[car_value])
        # writes value
        if format_time_elapsed_reset_to_float == target_second_csv_raw:
            write_values_on_csv_raw(values_to_csv)
    # resets value
    if format_time_elapsed_reset_to_float == target_second_csv_raw:
        Modules.Values.variables.time_elapsed_reset = 0

    # Process the polygon zone
    process_polygon_zone(zones_dict, detections, frame)
    # Polygon zone timer
    Modules.Values.variables.zone_timer += 1 / 30
    format_time_elapsed_test = f"{Modules.Values.variables.zone_timer: 0.3f}"
    print(format_time_elapsed_test)
    if abs(float(format_time_elapsed_test) - 1.0) < 0.001:
        write_csv_polygon_zone(process_polygon_zone(zones_dict, detections, frame))
        Modules.Values.variables.processed_objects = {}
        Modules.Values.variables.zone_timer = 0

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


tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()



