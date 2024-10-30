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
import cv2
from screenshot import screenshot
from variables import book_pages


# while True:
#     # Capture the screen using adb
#     png_stdout_bytes = subprocess.check_output("adb exec-out screencap -p ")
#     # Convert the stdout bytes to a numpy array
#     png_bytes = np.frombuffer(png_stdout_bytes, np.uint8)
#     # Decode the image from the numpy array
#     frame = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)

def main():
    # while True:
    #     # Capture the screen using adb
    #     png_stdout_bytes = subprocess.check_output("adb exec-out screencap -p ")
    #     # Convert the stdout bytes to a numpy array
    #     png_bytes = np.frombuffer(png_stdout_bytes, np.uint8)
    #     # Decode the image from the numpy array
    #     frame = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)
    
    #     cv2.imshow('Screen Capture', cv2.resize(frame, 
    #                                         (int(frame.shape[1] * 0.3), 
    #                                          int(frame.shape[0] * 0.3))
    #                                         )
    #            )
    #     cv2.waitKey(1)
        path = r'D:\vs_projects\nonogram_solver_lunastory\screenshots\screenshot_temp.png'
        screenshot(path)
        frame = cv2.imread(path)


        puzzle_coords = None

        picture_coords = detect_field_coords(frame)
        picture_x_min, picture_x_max = picture_coords[0]
        picture_y_min, picture_y_max = picture_coords[1]

        # picture_xs, picture_ys = picture_coords
        # picture_x_min, picture_x_max = picture_xs
        # picture_y_min, picture_y_max = picture_ys

        for page in book_pages:

            # picture_shape = book_pages[page]['shape']
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
                        if lvl < 8:
                            continue
                        
                        # Вычисление координат для центра каждого квадрата
                        x = int(picture_x_min + j * x_step + x_step / 2)
                        y = int(picture_y_min + i * y_step + y_step / 2)

                        subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)
                        # subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)

                        screenshot(path)
                        frame = cv2.imread(path)
                        
                        if not is_enter(frame):
                            print(f'{lvl} уровень уже пройден\n')
                            continue
                        screenshot(path)
                        frame = cv2.imread(path)
                        
                        print(f'{lvl} уровень запущен')
                        if puzzle_coords == None:
                            puzzle_coords = detect_field_coords(frame)

                        print('Ищем числа сверху...')
                        COLS = col_detector(frame, puzzle_coords, puzzle_shape)
                        print(COLS)

                        print('Ищем числа слева...')
                        ROWS = row_detector(frame, puzzle_coords, puzzle_shape)
                        print(ROWS)

                        print('Думаем как решать...')
                        board = NonogramSolver(ROWS_VALUES=ROWS, COLS_VALUES=COLS).board

                        print('Решаем задачу...')
                        solving(board, puzzle_coords)
                        print('Проверка...')
                        # time.sleep(1)
                        screenshot(path)
                        frame = cv2.imread(path)

                        attempts = 0
                        max_attempts = 3
                        while not competition(frame):
                            print('Нажму еще раз...')
                            solving(board, puzzle_coords)
                            attempts += 1
                            
                            screenshot(path)
                            frame = cv2.imread(path)
                            
                            if competition(frame):
                                break
                            elif attempts >= max_attempts:
                                print("3 раза не смог собрать")
                                breakpoint()
                        print('Переходим на NEXT LEVEL\n')
                        subprocess.run(["pwsh", "-Command", f'adb shell input tap {538} {1758}'], check=False)
                        # time.sleep(1)
            time.sleep(7)
            print('ща следующую картинку будем собирать...')
            subprocess.run(["pwsh", "-Command", f'adb shell input tap {955} {1705}'], check=False)
        
    
if __name__ == '__main__':
    main()