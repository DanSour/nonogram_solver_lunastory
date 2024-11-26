import subprocess
import time
from check_complete import competition
from take_frame import frame

def try_solve_with_hints():
    # Используем подсказки
    for _ in range(5):
        subprocess.run(["pwsh", "-Command", f'adb shell input tap {1020} {1560}'], check=False)
    time.sleep(1)
    return competition(frame())
