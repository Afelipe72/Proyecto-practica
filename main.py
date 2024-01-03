from modules.helpers import *

from modules.variables import *

from modules.variables import format_time_elapsed

def callback(frame: np.ndarray, _: int) -> np.ndarray:
    # Process frame
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)
    # Set variables
    global current_frame, time_elapsed, CLASS_NAMES_DICT, zones_dict, zone_timer, accumulated_data, \
        format_time_elapsed_test, processed_objects, time_elapsed_reset
    current_frame += 1

    time_elapsed_reset += 1 / 30
    format_time_elapsed_reset = f"{time_elapsed_reset: 0.3f}"
    format_time_elapsed_reset_to_float = float(format_time_elapsed_reset)

    time_elapsed += 1 / 30
    modules.variables.format_time_elapsed = f"{time_elapsed: 0.3f}"
    print(format_time_elapsed)
    # Process for the raw csv values
    for car_value in range(len(detections)):
        values_to_csv = format_csv_values(detections.tracker_id[car_value], detections.xyxy[car_value],
                                          CLASS_NAMES_DICT.get(detections.class_id[car_value]), detections.confidence[car_value])

        if format_time_elapsed_reset_to_float == target_second_csv_raw:
            write_values_on_csv_raw(values_to_csv)

    if format_time_elapsed_reset_to_float == target_second_csv_raw:
        time_elapsed_reset = 0

    # Process the polygon zone
    process_polygon_zone(zones_dict, detections, frame)
    # Polygon zone timer
    zone_timer += 1 / 30
    format_time_elapsed_test = f"{zone_timer: 0.3f}"
    print(format_time_elapsed_test)
    if abs(float(format_time_elapsed_test) - 1.0) < 0.001:
        write_csv_polygon_zone(process_polygon_zone(zones_dict, detections, frame))
        modules.variables.processed_objects = {}
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


if __name__ == "__main__":
    sv.process_video(
        source_path="vehicle-counting.mp4",
        target_path="result.mp4",
        callback=callback
    )
