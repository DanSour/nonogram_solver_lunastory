import subprocess
from solvers.solver_120_rows import NonogramSolver
import numpy as np

# screenshot_path = "D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png"
# board = find_game_grid(screenshot_path)

# # Преобразуем список в массив NumPy и извлекаем координаты
# board_array = np.vstack(board)
# x_coords = board_array[:, 0, 0]
# y_coords = board_array[:, 0, 1]

# # Нахождение минимальных и максимальных значений
# x_min = np.min(x_coords)
# x_max = np.max(x_coords)
# y_min = np.min(y_coords)
# y_max = np.max(y_coords)

x_min = 180
x_max = 1079
y_min = 495
y_max = 1394

# Расчет шагов по x и y
x_step = (x_max - x_min) / (10)  # 10 столбцов
y_step = (y_max - y_min) / (10)  # 10 строки

# Таблица значений

COLS_VALUES = [[2,1],[4,3],[2,4,1],[2,2,2],[6],[6],[2,2,2],[2,4,1],[4,3],[2,1]]
ROWS_VALUES =  [[1,1], [2,2], [2,2], [2,2],[3,2,3],[8],[6],[2,2,2],[1,4,1],[10]]


board = NonogramSolver(ROWS_VALUES=ROWS_VALUES, COLS_VALUES=COLS_VALUES).board

# Размеры сетки
rows = len(board)
cols = len(board[0])

# Расчет шага по x и y, учитывая дополнительный интервал
x_step = (x_max - x_min) / cols
y_step = (y_max - y_min) / rows

comm = ''
# Проход по таблице и отправка команд
for i in range(rows):
    for j in range(cols):
        if board[i][j] == 1:
            # Вычисление координат для центра каждого квадрата
            x = int(x_min + j * x_step + x_step / 2)
            y = int(y_min + i * y_step + y_step / 2)

            # Формирование команды
            # command = f'adb shell input tap {x} {y}'
            comm += f'adb shell input tap {x} {y} ; '

            # Отправка команды в PowerShell
            # subprocess.run(["pwsh", "-Command", command], check=False)
subprocess.run(["pwsh", "-Command", comm[:-1]], check=False)