from ultralytics import YOLO

excel_file_path = 'FORMATO PARA AFORO DE VEHICULOS.xlsx'
path_report_copy = "Processed_report.xlsx"

model = YOLO("yolov8x_heroes_bien.pt")



excel_file_path_coordinates = 'Coordenadas_heroes.xlsx'


video_info_test = None