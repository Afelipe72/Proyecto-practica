from ultralytics import YOLO

excel_file_path = 'FORMATO PARA AFORO DE VEHICULOS.xlsx'
path_report_copy = "Processed_report.xlsx"

model = YOLO("yolov8x_calle_100.pt")
