import subprocess
from screenshot import screenshot
import time
import numpy as np
import sys

from num_detector_row_upd_def import row_detector
# from num_detector_col_upd_def import col_detector
from num_detector_col_upd_def_v2 import col_detector
from solvers.solver_120_rows import NonogramSolver
from wlk_through_tbl_snd_comms_def import solving
from check_complete import competition
from lvl_check import is_enter


paint_x_min = 195
paint_x_max = 880
paint_y_min = 820
paint_y_max = 1520

paint_shapes = [12,12]

path_to_save = 'D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot_temp.png '

for paint_shape in paint_shapes:

    matrix = np.ones((paint_shape, paint_shape))

    # Расчет шагов по x и y
    x_step = (paint_x_max - paint_x_min) / (paint_shape)  # paint_shape столбцов
    y_step = (paint_y_max - paint_y_min) / (paint_shape)  # paint_shape строки

    # Размеры сетки
    paint_rows = len(matrix)
    paint_cols = len(matrix[0])

    # Расчет шага по x и y, учитывая дополнительный интервал
    x_step = (paint_x_max - paint_x_min) / paint_cols
    y_step = (paint_y_max - paint_y_min) / paint_rows

    for i in range(paint_rows):
        for j in range(paint_cols):
            if matrix[i][j] == 1:
                lvl = i*10+j+1
                # if lvl < 8:
                #     continue
                
                # Вычисление координат для центра каждого квадрата
                x = int(paint_x_min + j * x_step + x_step / 2)
                y = int(paint_y_min + i * y_step + y_step / 2)

                subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)

                time.sleep(0.5)
                screenshot(path_to_save)
                if not is_enter(path_to_save):
                    print(f'{lvl} уровень уже пройден')
                    continue

                print('Ищем числа в строках...')
                ROWS = row_detector()

                print('Ищем числа в колонках...')
                COLS = col_detector()

                print('Думаем как решать...')
                board = NonogramSolver(ROWS_VALUES=ROWS, COLS_VALUES=COLS).board

                print('Решаем задачу...')
                solving(board)
                time.sleep(1)
                
                print('Проверка...')
                screenshot(path_to_save)

                attempts = 0
                max_attempts = 3
                while not competition(path_to_save):
                    print('Нажму еще раз...')
                    solving(board)
                    screenshot(path_to_save)
                    attempts += 1
                    if competition(path_to_save) == True:
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
