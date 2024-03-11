import csv
from openpyxl import load_workbook
import shutil

# Method: write_values_on_csv_raw
import Modules
from Modules.Values.variables import header_written_raw_csv

# Method: write_csv_polygon_zone
from Modules.Values.variables import header_written_zone, format_time_elapsed
from Modules.FormatValues.format_values import format_report_values

# Method: create_excel_sheets
from Modules.Values.files import excel_file_path, path_report_copy


def write_values_on_csv_raw(csv_values):
    if not Modules.Values.variables.header_written_raw_csv:
        vehicles_csv_header = ['Frame', 'Tiempo(S)', 'Tipo de vehiculo', '% Certeza', 'Id Vehículo', 'X (Coordenadas)',
                               'Y (Coordenadas)', 'X (m)', 'Y (m)', 'Vx (m/s)', 'Vy(m/s)', 'Vt(m/s)', 'Ax(m/s)',
                               'Ay(m/s)', 'At(m/s)']
        with open('raw.csv', 'a', newline='') as vehicles_csv:
            writer = csv.writer(vehicles_csv)
            writer.writerow(vehicles_csv_header)

        Modules.Values.variables.header_written_raw_csv = True

    # Open the CSV file in append mode and write the Values
    with open('raw.csv', 'a', newline='') as vehicles_csv:
        writer = csv.writer(vehicles_csv)
        writer.writerow(csv_values)


def write_csv_polygon_zone(accumulated_data):
    car_values_list = []
    car_value_list_report = []
    if not Modules.Values.variables.header_written_zone:
        # minuto , topologia , tipo carro, nombre de la zona, conteo
        vehicles_csv_header = ['Zona', 'Minuto', 'Conteo general', 'Tipología del vehiculo', 'ID Unico']
        with open('csv_routes.csv', 'a', newline='') as polygon_zone_csv:
            writer = csv.writer(polygon_zone_csv)
            writer.writerow(vehicles_csv_header)

        Modules.Values.variables.header_written_zone = True

    for key, car_values in accumulated_data[0].items():
        for value in car_values:
            # items_accumulated_data = {'zone':key, **value}
            zone_name = key
            vehicle_count = value['vehicle_count']
            tracker_id = value['tracker_id']
            class_id = value['class_id']
            class_names = value['class_names']
            confidence = value['confidence']

            # Append the extracted Values to the list
            car_values_list.extend([zone_name, float(Modules.Values.variables.format_time_elapsed)/60, vehicle_count, class_names, tracker_id])

            car_value_list_report.extend([zone_name, Modules.Values.variables.format_time_elapsed, vehicle_count, class_names])

            # Open the CSV file in append mode and write the Values
            with open('csv_routes.csv', 'a', newline='') as polygon_zone_csv:
                writer = csv.writer(polygon_zone_csv)
                writer.writerow(car_values_list)

            # Clear the list for the next row
            car_values_list = []

    format_report_values(car_value_list_report)


def create_excel_sheets(number_of_zones):
    shutil.copy(Modules.Values.files.excel_file_path, path_report_copy)
    wb = load_workbook(path_report_copy)
    target_worksheet = wb['template']
    for key, zone_items in number_of_zones.items():
        new_sheet = wb.copy_worksheet(target_worksheet)
        new_sheet.title = key
    del wb['template']
    wb.save(path_report_copy)