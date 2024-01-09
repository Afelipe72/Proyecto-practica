import csv
from openpyxl import load_workbook
import shutil

# Method: write_values_on_csv_raw
import Modules
from Modules.Values.variables import header_written_raw_csv

# Method: write_csv_polygon_zone
from Modules.Values.variables import header_written_zone, format_time_elapsed
from Modules.FormatValues.format_values import format_report_values

# Method: write_excel_file
from Modules.Values.files import path_report_copy
from Modules.Values.constants import CLASS_NAMES_DICT

# Method: create_excel_sheets
from Modules.Values.files import excel_file_path


def write_values_on_csv_raw(csv_values):
    if not header_written_raw_csv:
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
    if not header_written_zone:
        # minuto , topologia , tipo carro, nombre de la zona, conteo
        vehicles_csv_header = ['Zona', 'Minuto', 'Conteo general', 'Tipología del vehiculo', 'ID Unico']
        with open('csv_routes.csv', 'a', newline='') as polygon_zone_csv:
            writer = csv.writer(polygon_zone_csv)
            writer.writerow(vehicles_csv_header)

        Modules.Values.variables.header_written_zone = True

    for key, car_values in accumulated_data.items():
        for value in car_values:
            # items_accumulated_data = {'zone':key, **value}
            zone_name = key
            vehicle_count = value['vehicle_count']
            tracker_id = value['tracker_id']
            class_id = value['class_id']
            class_names = value['class_names']
            confidence = value['confidence']

            # Append the extracted Values to the list
            car_values_list.extend([zone_name, format_time_elapsed, vehicle_count, class_names, tracker_id])

            car_value_list_report.extend([zone_name, format_time_elapsed, vehicle_count, class_names])

            # Open the CSV file in append mode and write the Values
            with open('csv_routes.csv', 'a', newline='') as polygon_zone_csv:
                writer = csv.writer(polygon_zone_csv)
                writer.writerow(car_values_list)

            # Clear the list for the next row
            car_values_list = []

    format_report_values(car_value_list_report)


def write_excel_file(vehicle_type_counts):
    print(vehicle_type_counts)
    # Write the vehicles
    # {'test': {'carros': {'Zone timer': ' 1.000', 'Count': 8}},
    # 'test2': {'carros': {'Zone timer': ' 1.000', 'Count': 1}}}

    # for zone_name, zone_items in vehicle_type_counts.items():
    #     print(f"Zone_name: {zone_name}")
    #     for vehicle_type, zone_timer_and_count in zone_items.items():
    #         print(f"Vehicle Type: {vehicle_type}")
    #         for zone_timer, vehicle_count in zone_timer_and_count.items():
    #             print(f"Zone Timer: {zone_timer}")
    #             print(f"Count: {vehicle_count}")
    wb = load_workbook(path_report_copy)
    ws = wb.active

    # Write the header for the file
    for zone_name, _ in vehicle_type_counts.items():
        for sheet in wb.worksheets:
            if zone_name == sheet.title:
                ws = wb[zone_name]
                start_column_index = 3
                # start column index to set the start value
                for col_idx, (key, value) in enumerate(CLASS_NAMES_DICT.items(), start=start_column_index):
                    # Col idx to increase the column
                    for row in ws.iter_rows(min_row=9, min_col=col_idx, max_row=9, max_col=col_idx):
                        for cell in row:
                            cell.value = value
    wb.save(path_report_copy)

    # Time zone for the Excel file
    timer = 0
    for zone_name_w, _ in vehicle_type_counts.items():
        for sheet in wb.worksheets:
            if zone_name_w == sheet.title:
                ws = wb[zone_name_w]
                for zone_name, zone_items in vehicle_type_counts.items():
                    for vehicle_type, zone_timer_and_count in zone_items.items():
                        timer = zone_timer_and_count['Zone timer']
                for row in ws.iter_rows(min_row=Modules.Values.variables.counter_zone_timer + 10, min_col=2, max_row=Modules.Values.variables.counter_zone_timer+10, max_col=2):
                    for cell in row:
                        cell.value = timer
    Modules.Values.variables.counter_zone_timer += 1
    wb.save(path_report_copy)

    # Vehicle writer counter
    start_column_index_counter = 3
    vehicle_counter_tracker = 0
    # Puts the vehicle type in a list
    header_order = [CLASS_NAMES_DICT[i] for i in range(len(CLASS_NAMES_DICT))]
    # start column index to set the start value
    for zone_name, zone_items in vehicle_type_counts.items():
        for sheet in wb.worksheets:
            if zone_name == sheet.title:
                ws = wb[zone_name]
                for vehicle_type, zone_timer_and_count in zone_items.items():
                    # Find the index of the current vehicle type in the header order
                    col_idx = header_order.index(vehicle_type) + start_column_index_counter
                    # Get the count value for the current vehicle type
                    vehicle_counter_tracker = zone_timer_and_count['Count']
                    # Write the count value to the corresponding cell in the Excel file
                    for row_idx in range(Modules.Values.variables.vehicle_counter_zone_timer + 10, Modules.Values.variables.vehicle_counter_zone_timer + 11):
                        for cell in ws.iter_cols(min_col=col_idx, max_col=col_idx, min_row=row_idx, max_row=row_idx):
                            for c in cell:
                                c.value = vehicle_counter_tracker
                    wb.save(path_report_copy)
    Modules.Values.variables.vehicle_counter_zone_timer += 1


def create_excel_sheets(number_of_zones):
    shutil.copy(excel_file_path, path_report_copy)
    wb = load_workbook(path_report_copy)
    target_worksheet = wb['template']
    for key, zone_items in number_of_zones.items():
        new_sheet = wb.copy_worksheet(target_worksheet)
        new_sheet.title = key
    del wb['template']
    wb.save(path_report_copy)
