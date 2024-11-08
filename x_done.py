import subprocess
import time
import numpy as np
import sys
from dataclasses import dataclass
from typing import Tuple

from detect_rows import row_detector
from detect_cols import col_detector
from detect_field import detect_field_coords
from check_complete import competition
from solve import solving
from check_lvl import is_enter
from solvers.solver_120_rows import NonogramSolver
from take_frame import frame
from variables import book_pages
from check_solving import try_solve_with_hints, try_solve_manually

@dataclass
class PuzzleCoordinates:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    
    @property
    def x_range(self) -> Tuple[int, int]:
        return (self.x_min, self.x_max)
    
    @property
    def y_range(self) -> Tuple[int, int]:
        return (self.y_min, self.y_max)

def tap_screen(x: int, y: int, delay: float = 0.5):
    """Выполняет тап по экрану через ADB"""
    subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)
    time.sleep(delay)

def solve_puzzle(puzzle_coords: PuzzleCoordinates, puzzle_shape: Tuple[int, int]) -> bool:
    """Решает один пазл и возвращает True если решение успешно"""
    print('Ищем числа сверху...')
    cols = col_detector(frame(), puzzle_coords, puzzle_shape)
    print(cols)

    print('Ищем числа слева...')
    rows = row_detector(frame(), puzzle_coords, puzzle_shape)
    print(rows)

    print('Думаем как решать...')
    board = NonogramSolver(ROWS_VALUES=rows, COLS_VALUES=cols).board

    print('Решаем задачу...')
    solving(board, puzzle_coords)
    time.sleep(1)
    
    print('Проверка...')
    if not competition(frame()):
        return try_solve_with_hints() or try_solve_manually(board, puzzle_coords)
    return True

def main():
    start_lvl = 5
    puzzle_coords = None

    field_coords = detect_field_coords(frame())
    picture_coords = PuzzleCoordinates(
        x_min=field_coords[0][0],
        x_max=field_coords[0][1],
        y_min=field_coords[1][0],
        y_max=field_coords[1][1]
    )

    for page, page_info in book_pages.items():
        picture_shape = page_info['shape']
        matrix = np.ones(picture_shape)
        
        x_step = (picture_coords.x_max - picture_coords.x_min) / picture_shape[1]
        y_step = (picture_coords.y_max - picture_coords.y_min) / picture_shape[0]
        
        puzzle_shape = page_info['puzzle_shape']

        for i in range(picture_shape[0]):
            for j in range(picture_shape[1]):
                if matrix[i][j] != 1:
                    continue
                    
                lvl = i * picture_shape[0] + j + 1
                if page == 15 and lvl < start_lvl:
                    continue

                x = int(picture_coords.x_min + j * x_step + x_step / 2)
                y = int(picture_coords.y_min + i * y_step + y_step / 2)

                # Пытаемся войти в уровень
                tap_screen(x, y, delay=1)
                if not is_enter(frame()):
                    tap_screen(x, y, delay=1)
                    if not is_enter(frame()):
                        print(f'{lvl} уровень уже пройден\n')
                        continue

                print(f'{lvl} уровень')
                if puzzle_coords is None:
                    puzzle_coords = detect_field_coords(frame())

                if not solve_puzzle(puzzle_coords, puzzle_shape):
                    print("3 раза не смог собрать")
                    sys.exit()

                print('Переходим на NEXT LEVEL\n')
                tap_screen(538, 1758, delay=0.01)

        time.sleep(7)
        print('ща следующую картинку будем собирать...')
        tap_screen(955, 1705, delay=1)

if __name__ == '__main__':
    main()