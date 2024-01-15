from ultralytics import YOLO

excel_file_path = 'FORMATO PARA AFORO DE VEHICULOS.xlsx'
path_report_copy = "Processed_report.xlsx"

model = YOLO("yolov8x_estacion_polo_2.pt")



excel_file_path_coordinates = None


video_info_resolution = None