import subprocess
from screenshot import screenshot
import time
import numpy as np

from num_detector_row_upd_def import row_detector
# from num_detector_col_upd_def import col_detector
from num_detector_col_upd_def_v2 import col_detector
from solvers.solver_120_rows import NonogramSolver
from wlk_through_tbl_snd_comms_def import solving
from check_complete import competition


paint_x_min = 195
paint_x_max = 880
paint_y_min = 820
paint_y_max = 1520

paint_shapes = [10, 10, 10, 10, 12,12]

for paint_shape in [1]:

    # matrix = np.ones((paint_shape, paint_shape))

    # Расчет шагов по x и y
    x_step = (paint_x_max - paint_x_min) / (paint_shape)  # paint_shape столбцов
    y_step = (paint_y_max - paint_y_min) / (paint_shape)  # paint_shape строки

    matrix = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 1, 1, 1, 1, 1, 1, 1], 
                [1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]

    # Размеры сетки
    paint_rows = len(matrix)
    paint_cols = len(matrix[0])

    # Расчет шага по x и y, учитывая дополнительный интервал
    x_step = (paint_x_max - paint_x_min) / paint_cols
    y_step = (paint_y_max - paint_y_min) / paint_rows

    comm = ''
    # Проход по таблице и отправка команд
    for i in range(paint_rows):
        for j in range(paint_cols):
            if matrix[i][j] == 1:
                # Вычисление координат для центра каждого квадрата
                x = int(paint_x_min + j * x_step + x_step / 2)
                y = int(paint_y_min + i * y_step + y_step / 2)

                subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)
                print('Вошли в уровень')
                time.sleep(1)

                path_to_save = 'D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot_temp.png '
                screenshot(path_to_save)
                print('Сделали скрин')
                time.sleep(1)

                print('Ищем числа в строках...')
                ROWS = row_detector()

                print('Ищем числа в колонках...')
                COLS = col_detector()

                print('Думаем как решать...')
                board = NonogramSolver(ROWS_VALUES=ROWS, COLS_VALUES=COLS).board

                print('Решаем задачу...')
                solving(board)
                
                print('Ща проверю решение...')
                screenshot(path_to_save)
                time.sleep(1)

                attempts = 0
                max_attempts = 3
                while not competition(path_to_save):
                    solving(board)
                    attempts += 1
                    if competition:
                        break
                    elif attempts >= max_attempts:
                        print("3 раза не смог собрать емае, глянь че там")
                        break
                    
                print('Задача решена')
                time.sleep(1)

                print('Ввыходим из задачи')
                subprocess.run(["pwsh", "-Command", f'adb shell input tap {538} {1758}'], check=False)
                time.sleep(1)

    print('ща следующую картинку будем собирать...')