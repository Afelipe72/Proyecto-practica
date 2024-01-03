import numpy as np
import math
import supervision as sv
from supervision import Point
from ultralytics import YOLO
import csv
import openpyxl
from openpyxl import load_workbook
import cv2
from functools import partial

from modules.files import *

from modules.helpers import *

from modules.variables import *

import modules.variables
from modules.variables import *


GSD = 0
frames_per_second = 0.0333

user_input_minutes_raw_csv = 0.1  # Input in minutes
target_second_csv_raw = user_input_minutes_raw_csv * 60

user_input_minutes_zone_timer = 0.1
target_second_zone = user_input_minutes_zone_timer * 60



