import subprocess
import time
import numpy as np
import sys
from dataclasses import dataclass

from take_frame import frame
from detect_field import detect_picture_field, detect_puzzle
from check_lvl import is_enter
from detect_rows import row_detector
from detect_cols import col_detector
from solvers.solver_120_rows import NonogramSolver
from solve import solving
from check_complete import competition
from check_solving import try_solve_with_hints, try_solve_manually
from variables import book_pages

@dataclass
class PuzzleCoordinates:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    
def tap_screen(x: int, y: int, delay: float = 0.5):
    """Выполняет тап по экрану через ADB"""
    subprocess.run(["pwsh", "-Command", f'adb shell input tap {x} {y}'], check=False)
    time.sleep(delay)

def level_entry(x: int, y: int, delay: float = 0.5, lvl: int = None):
    tap_screen(x, y, delay)
    if not is_enter(frame()):
        tap_screen(x, y, delay)
        if not is_enter(frame()):
            print(f'{lvl} уровень уже пройден\n')
            return False
    return True

# def solve_puzzle(puzzle_coords: PuzzleCoordinates, puzzle_shape: Tuple[int, int]) -> bool:
def solve_puzzle(puzzle_coords: PuzzleCoordinates, puzzle_shape: int) -> bool:
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
    start_lvl = 7
    puzzle = None

    big_picture_coords = detect_picture_field(frame())
    picture_coords = PuzzleCoordinates(
        x_min=big_picture_coords['coords'][0][0],
        x_max=big_picture_coords['coords'][0][1],
        y_min=big_picture_coords['coords'][1][0],
        y_max=big_picture_coords['coords'][1][1]
    )

    for page, page_info in book_pages.items():
        picture_shape = page_info['shape']
        matrix = np.ones(picture_shape)
        
        x_step = (picture_coords.x_max - picture_coords.x_min) / picture_shape[1]
        y_step = (picture_coords.y_max - picture_coords.y_min) / picture_shape[0]
        
        # puzzle_shape = page_info['puzzle_shape']

        for i in range(picture_shape[0]):
            for j in range(picture_shape[1]):
                if matrix[i][j] != 1:
                    continue
                    
                lvl = i * picture_shape[0] + j + 1
                if page == 17 and lvl < start_lvl:
                    continue

                x = int(picture_coords.x_min + j * x_step + x_step / 2)
                y = int(picture_coords.y_min + i * y_step + y_step / 2)

                # Пытаемся войти в уровень
                if not level_entry(x, y, delay=0.5, lvl=lvl):
                    continue

                print(f'{lvl} уровень')
                if puzzle is None:
                    puzzle = detect_puzzle(frame())

                if not solve_puzzle(puzzle['coords'], puzzle['shape']):
                    print("3 раза не смог собрать")
                    sys.exit()

                print('Переходим на NEXT LEVEL\n')
                tap_screen(538, 1758, delay=0.01)

        time.sleep(7)
        print('ща следующую картинку будем собирать...')
        tap_screen(955, 1705, delay=1)

if __name__ == '__main__':
    main()