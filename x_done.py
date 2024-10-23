import subprocess
import time
import numpy as np
import sys

from screenshot import screenshot
from num_detector_row_upd_def import row_detector
from num_detector_col_upd_def_v2 import col_detector
from solvers.solver_120_rows import NonogramSolver
from wlk_through_tbl_snd_comms_def import solving
from check_complete import competition
from lvl_check import is_enter
import cv2

    
paint_x_min ,paint_x_max = 195, 880
paint_y_min, paint_y_max = 820, 1520

book_pages = {
    11: {'shape': 6, 'puzzle_shape': 15},
    12: {'shape': 6, 'puzzle_shape': 15},
    13: {'shape': 8, 'puzzle_shape': 15},
    14: {'shape': 8, 'puzzle_shape': 15},
    15: {'shape': 5, 'puzzle_shape': 20},
    16: {'shape': 5, 'puzzle_shape': 20},
    17: {'shape': 6, 'puzzle_shape': 20},
    18: {'shape': 6, 'puzzle_shape': 20},
    19: {'shape': 8, 'puzzle_shape': 20},
    20: {'shape': 10, 'puzzle_shape': 20},
    # 21: {'shape': None, 'puzzle_shape': None},
    # 22: {'shape': None, 'puzzle_shape': None},
    # 23: {'shape': None, 'puzzle_shape': None},
    # 24: {'shape': None, 'puzzle_shape': None},
}

# path_to_save = 'D:\\vs_projects\\nonogram_solver_lunastory\\screenshots\\screenshot_temp.png '
while True:

    # Capture the screen using adb
    png_stdout_bytes = subprocess.check_output("adb exec-out screencap -p ")
    # Convert the stdout bytes to a numpy array
    png_bytes = np.frombuffer(png_stdout_bytes, np.uint8)
    # Decode the image from the numpy array
    img = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)

    for page in book_pages:

        paint_shape = book_pages[page]['shape']
        puzzle_shape = book_pages[page]['puzzle_shape']
        
        matrix = np.ones((paint_shape, paint_shape))

        # Расчет шагов по x и y
        x_step = (paint_x_max - paint_x_min) / paint_shape  # paint_shape столбцов
        y_step = (paint_y_max - paint_y_min) / paint_shape  # paint_shape строки

        for i in range(paint_shape):
            for j in range(paint_shape):
                if matrix[i][j] == 1:
                    lvl = i*paint_shape+j+1
                    if lvl < 6:
                        continue
                    
                    # Вычисление координат для центра каждого квадрата
                    x = int(paint_x_min + j * x_step + x_step / 2)
                    y = int(paint_y_min + i * y_step + y_step / 2)

                    subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)

                    time.sleep(0.5)
                    # screenshot(path_to_save)
                    if not is_enter(img):
                        print(f'{lvl} уровень уже пройден\n')
                        continue

                    print('Ищем числа в колонках...')
                    COLS = col_detector(img, puzzle_shape)
                    # COLS = col_detector()

                    print('Ищем числа в строках...')
                    ROWS = row_detector(img, puzzle_shape)
                    # ROWS = row_detector()

                    print('Думаем как решать...')
                    board = NonogramSolver(ROWS_VALUES=ROWS, COLS_VALUES=COLS).board

                    print('Решаем задачу...')
                    solving(board)
                    time.sleep(1)
                    
                    print('Проверка...')
                    # screenshot(path_to_save)

                    attempts = 0
                    max_attempts = 3
                    while not competition(img):
                        print('Нажму еще раз...')
                        solving(board)
                        # screenshot(path_to_save)
                        attempts += 1
                        if competition(img) == True:
                            break
                        elif attempts >= max_attempts:
                            print("3 раза не смог собрать емае, глянь че там")
                            sys.exit()
                    print('Переходим на NEXT LEVEL\n')
                    subprocess.run(["pwsh", "-Command", f'adb shell input tap {538} {1758}'], check=False)
                    time.sleep(1)

        time.sleep(7)
        print('ща следующую картинку будем собирать...')
        subprocess.run(["pwsh", "-Command", f'adb shell input tap {955} {1705}'], check=False)
    
    
    break