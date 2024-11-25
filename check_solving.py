import subprocess
import time
from check_complete import competition
from take_frame import frame
from solve import solving

def try_solve_with_hints():
    # Используем подсказки
    for _ in range(5):
        subprocess.run(["pwsh", "-Command", f'adb shell input tap {1020} {1560}'], check=False)
    time.sleep(1)
    return competition(frame())

def try_solve_manually(max_attempts=3, board=None, puzzle_coords=None):
    try:
        for _ in range(max_attempts):
            solving(board, puzzle_coords)
            time.sleep(1)
    except Exception as e:
            print(f"An error occurred: {e}")
    return competition(frame())

