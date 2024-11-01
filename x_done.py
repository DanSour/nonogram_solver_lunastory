import subprocess
import time
import numpy as np
import sys

from num_detector_row_upd_def_v2 import row_detector
from num_detector_col_upd_def_v2 import col_detector
from solvers.solver_120_rows import NonogramSolver
from wlk_through_tbl_snd_comms_def import solving
from detect_field import detect_field_coords
from check_complete import competition
from lvl_check import is_enter
from frame_take import frame

from variables import book_pages


def main():

        puzzle_coords = None

        picture_coords = detect_field_coords(frame())
        picture_x_min, picture_x_max = picture_coords[0]
        picture_y_min, picture_y_max = picture_coords[1]

        for page in book_pages:

            picture_x_shape, picture_y_shape = book_pages[page]['shape']
            matrix = np.ones((picture_x_shape, picture_y_shape))
            
            # Расчет шагов по x и y
            x_step = (picture_x_max - picture_x_min) / picture_x_shape  # picture_shape столбцов
            y_step = (picture_y_max - picture_y_min) / picture_y_shape  # picture_shape строки
            
            puzzle_shape = book_pages[page]['puzzle_shape']

            for i in range(picture_x_shape):
                for j in range(picture_y_shape):
                    if matrix[i][j] == 1:
                        lvl = i*picture_x_shape+j+1
                        if page == 14 and lvl < 57:
                            continue
                        
                        # Вычисление координат для центра каждого квадрата
                        x = int(picture_x_min + j * x_step + x_step / 2)
                        y = int(picture_y_min + i * y_step + y_step / 2)

                        subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)
                        time.sleep(0.5)

                        if not is_enter(frame()):
                            subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)
                            time.sleep(0.5)
                            if not is_enter(frame()):
                                print(f'{lvl} уровень уже пройден\n')
                                continue
                        
                        print(f'{lvl} уровень')
                        if puzzle_coords == None:
                            puzzle_coords = detect_field_coords(frame())

                        print('Ищем числа сверху...')
                        COLS = col_detector(frame(), puzzle_coords, puzzle_shape)
                        print(COLS)

                        print('Ищем числа слева...')
                        ROWS = row_detector(frame(), puzzle_coords, puzzle_shape)
                        print(ROWS)

                        print('Думаем как решать...')
                        board = NonogramSolver(ROWS_VALUES=ROWS, COLS_VALUES=COLS).board

                        print('Решаем задачу...')
                        solving(board, puzzle_coords)
                        time.sleep(1)
                        print('Проверка...')

                        attempts = 0
                        max_attempts = 3
                        while not competition(frame()):
                            attempts += 1
                            for i in range(5):
                                # Нажать на подсказку 5 раз
                                subprocess.run(["pwsh", "-Command", f'adb shell input tap {1020} {1560}'], check=False)
                            time.sleep(1)
                                
                            if competition(frame()):
                                break
                            elif attempts >= max_attempts:
                                print("3 раза не смог собрать")
                                breakpoint()
                        print('Переходим на NEXT LEVEL\n')
                        subprocess.run(["pwsh", "-Command", f'adb shell input tap {538} {1758}'], check=False)
                        time.sleep(0.01)

            time.sleep(7)
            print('ща следующую картинку будем собирать...')
            subprocess.run(["pwsh", "-Command", f'adb shell input tap {955} {1705}'], check=False)
            time.sleep(1)
        
    
if __name__ == '__main__':
    main()