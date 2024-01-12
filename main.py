from gooey import Gooey, GooeyParser

from Modules.ProcessValues.process_values import gooey_receiver
from Modules.Values.constants import GSD, user_input_minutes_raw_csv


@Gooey(program_name="Conteo vehícular", default_size=(1020, 610), language='spanish')
def main():
    # CLI to GUI
    parser = GooeyParser()
    # Optional parameter "--"
    # Arguments for the GUI to use
    # GSD Argument
    parser.add_argument("Ground Sampling Distance (GSD)", type=float, help="Inserte el valor del GSD (metros)", default= GSD)
    # Target second Argument
    parser.add_argument("Frecuencia de toma del muestreo", type=float, help="Inserte la frecuencia de toma de datos (minutos)", default=user_input_minutes_raw_csv)
    # Choose video argument
    parser.add_argument("video", help="Seleccione el video para realizar el aforo", widget='FileChooser')
    # Choose .pt model
    parser.add_argument("YOLO",  help="Seleccione el archivo .pt para realizar la inferencia", widget='FileChooser')
    # Choose CSV file
    parser.add_argument("Excel", help="Seleccione el archivo con las coordenadas", widget='FileChooser')

    # Execute callback function
    args = parser.parse_args()
    gooey_receiver(args)


if __name__ == "__main__":
    main()