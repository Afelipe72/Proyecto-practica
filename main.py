from gooey import Gooey, GooeyParser

import Modules.Values.constants
from Modules.ProcessValues.process_values import gooey_receiver
from Modules.Values.constants import GSD, user_input_minutes_raw_csv


@Gooey(program_name="Conteo Vehicular", default_size=(1020, 610), language='spanish')
def main():
    # Gooey GUI Configuration
    parser = GooeyParser()

    # Input Parameters
    parser.add_argument("GSD", type=float, help="GSD (metros)", action="store",)
    parser.add_argument("Frecuencia", type=float, help="Frecuencia de toma de datos general (Segundos)", action="store")
    parser.add_argument("Rutas", type=float, help="Frecuencia de toma de datos para las rutas (Minutos)", action="store")

    # File Selection
    parser.add_argument("Video", help="Seleccione el video para el aforo", widget='FileChooser')
    parser.add_argument("Modelo", help="Seleccione el archivo .pt para la inferencia YOLO", widget='FileChooser')
    parser.add_argument("Coordenadas", help="Seleccione el archivo con las coordenadas", widget='FileChooser')
    parser.add_argument("Plantilla", help="Seleccione la plantilla de aforo vehicular (Archivo excel)", widget='FileChooser')

    # Parse the arguments
    args = parser.parse_args()

    # Process the input
    gooey_receiver(args)


if __name__ == "__main__":
    main()