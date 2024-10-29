import subprocess
import cv2
import numpy as np
from num_detector_row_upd_def_v2 import row_detector
from num_detector_col_upd_def_v2 import col_detector
from solvers.solver_120_rows import NonogramSolver
from wlk_through_tbl_snd_comms_def import solving
from detect_field import detect_field_coords

while True:

    # Capture the screen using adb
    png_stdout_bytes = subprocess.check_output("adb exec-out screencap -p ")
    # Convert the stdout bytes to a numpy array
    png_bytes = np.frombuffer(png_stdout_bytes, np.uint8)
    # Decode the image from the numpy array
    img = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)
    
    # picture_coords = detect_field_coords(img)
    # picture_x_min, picture_x_max = picture_coords[0]
    # picture_y_min, picture_y_max = picture_coords[1]
    
    # puzzle_coords = detect_field_coords(img)
    
    # # rows = row_detector(img, 10)
    # rows = row_detector(img, puzzle_coords, 15)
    # # cols = col_detector(img, 10)
    # cols = col_detector(img, puzzle_coords, 15)
    # board = NonogramSolver(ROWS_VALUES=rows, COLS_VALUES=cols).board
    # solving(board, puzzle_coords)
    # break
    # Resize the image to be 50% smaller
    # width = int(img.shape[1] * 0.3)
    # height = int(img.shape[0] * 0.3)
    # img = cv2.resize(img, (width, height))

    # cv2.imshow('Screen Capture', img)
    cv2.imshow('Screen Capture', cv2.resize(img, 
                                            (int(img.shape[1] * 0.3), 
                                             int(img.shape[0] * 0.3))
                                            )
               )
    cv2.waitKey(1)

