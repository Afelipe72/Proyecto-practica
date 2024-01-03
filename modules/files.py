from ultralytics import YOLO
from openpyxl import load_workbook

excel_file_path = 'FORMATO PARA AFORO DE VEHICULOS.xlsx'
path_report_copy = "Processed_report.xlsx"


model = YOLO("yolov8x.pt")
