import subprocess
import time
from dataclasses import dataclass

from take_frame import frame
from detect_field import *
from check_lvl import is_enter
from detect_rows import row_detector
from detect_cols import col_detector
from solvers.solver_120_rows import NonogramSolver
from solve import solving
from check_complete import competition
from check_solving import try_solve_with_hints, try_solve_manually

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

def level_entry(x: int, y: int, delay: float = 0.5):
    tap_screen(x, y, delay)
    if not is_enter(frame()):
        tap_screen(x, y, delay)
        if not is_enter(frame()):
            return False
    return True

def solve_puzzle(puzzle_coords: PuzzleCoordinates, puzzle_shape: int): 
    """Решает один пазл и возвращает True если решение успешно"""
    try:
        print('Ищем числа сверху...')
        cols = col_detector(frame(), puzzle_coords, puzzle_shape)
        print(cols)

        print('Ищем числа слева...')
        rows = row_detector(frame(), puzzle_coords, puzzle_shape)
        print(rows)

        print('Думаем как решать...')
        board = NonogramSolver(ROWS_VALUES=rows, COLS_VALUES=cols).board

        if len(board) == 0:
            return False

        print('Решаем задачу...')
        solving(board, puzzle_coords)
        time.sleep(1)
        
        print('Проверка...')
        if not competition(frame()):
            if not try_solve_with_hints():
                # try_solve_manually(board, puzzle_coords)
                solving(board, puzzle_coords)
                if not competition(frame()):
                    return False

        return True
    except Exception as e:
        print(f"Ошибка в solve_puzzle: {e}")
        return False

def main(solving_type):
    puzzle = None
    for _ in range(1):
        picture = detect_picture(frame())

        for square in picture['squares'][::-1]:
                x = square[0]
                y = square[1]

                # Вход в уровень
                if not level_entry(x, y, delay=0.3):
                    continue

                if puzzle is None:
                    puzzle = detect_puzzle(frame(), solving_type)

                if solve_puzzle(puzzle['coords'], puzzle['shape']):
                    print('Переходим на NEXT LEVEL\n')
                    tap_screen(538, 1758, delay=0.01)

        time.sleep(7)
        print('ща следующую картинку будем собирать...')
        tap_screen(955, 1705, delay=0.1)

# if __name__ == '__main__':
#     solving_type = 'big'


#     main(solving_type)