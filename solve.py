import random
import subprocess
import time

def solving(board, puzzle_coords):
    
    puzzle_x_min, puzzle_x_max = puzzle_coords[0]
    puzzle_y_min, puzzle_y_max = puzzle_coords[1]

    # Размеры сетки
    rows = len(board)
    cols = len(board[0])

    # Расчет шага по x и y, учитывая дополнительный интервал
    x_step = (puzzle_x_max - puzzle_x_min) / cols
    y_step = (puzzle_y_max - puzzle_y_min) / rows

    comm = []
    # Проход по таблице и отправка команд
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == True:
                # Вычисление координат для центра каждого квадрата
                x = int(puzzle_x_min + j * x_step + x_step / 2)
                y = int(puzzle_y_min + i * y_step + y_step / 2)

                # Формирование команды
                comm.append(f'adb shell input tap {x} {y} ; Start-Sleep -Milliseconds 2.9 ; ')

    # Перемешиваем список
    random.shuffle(comm)
    comm = ' '.join(comm)

    subprocess.run(["pwsh", "-Command", comm[:-1]], check=False)
    time.sleep(1)

    return
