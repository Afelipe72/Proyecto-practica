from gooey import Gooey, GooeyParser

import Modules.Values.constants
from Modules.ProcessValues.process_values import gooey_receiver
from Modules.Values.constants import GSD, user_input_minutes_raw_csv


@Gooey(program_name="Conteo Vehicular", program_description= 'Contar carros :)' ,  default_size=(1020, 610), language='spanish', tabbed_groups=True)
def main():
    # Gooey GUI Configuration
    parser = GooeyParser()

    # upload files group
    upload_files_group = parser.add_argument_group(
        "Subir archivos",
        "Suba los archivos necesarios para realizar el conteo."
    )

    # Upload file Selection
    upload_files_group.add_argument(
        "Video", help="Seleccione el video para el aforo", widget='FileChooser',
    )
    upload_files_group.add_argument(
        "Modelo", help="Seleccione el archivo .pt para la inferencia YOLO", widget='FileChooser',
    )
    upload_files_group.add_argument(
         "Coordenadas", help="Seleccione el archivo con las coordenadas", widget='FileChooser',
    )
    upload_files_group.add_argument(
         "Plantilla", help="Seleccione la plantilla de aforo vehicular (Archivo excel)",widget='FileChooser'
    )

    # Input Parameters (gsd & timers) group
    parameters_group = parser.add_argument_group(
        "Valores para realizar el conteo",
        "Escriba los valores de GSD y temporizadores para realizar el conteo."
    )

    # Input Parameters (gsd & timers)
    parameters_group.add_argument(
        "GSD", type=float, help="GSD (metros)", action="store"
    )
    parameters_group.add_argument(
        "Frecuencia", type=float, help="Frecuencia de toma de datos general (Segundos)", action="store"
    )
    parameters_group.add_argument(
        "Rutas", type=float, help="Frecuencia de toma de datos para las rutas (Minutos)", action="store"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process the input
    gooey_receiver(args)


if __name__ == "__main__":
    main()