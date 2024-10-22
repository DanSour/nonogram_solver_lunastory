import random
import subprocess

def solving(board):
    
    x_min = 180
    x_max = 1079
    y_min = 495
    y_max = 1394

    # Размеры сетки
    rows = len(board)
    cols = len(board[0])

    # Расчет шага по x и y, учитывая дополнительный интервал
    x_step = (x_max - x_min) / cols
    y_step = (y_max - y_min) / rows

    comm = []
    # Проход по таблице и отправка команд
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 1:
                # Вычисление координат для центра каждого квадрата
                x = int(x_min + j * x_step + x_step / 2)
                y = int(y_min + i * y_step + y_step / 2)

                # Формирование команды
                comm.append(f'adb shell input tap {x} {y} ; ')

    # Перемешиваем список
    random.shuffle(comm)
    comm = ' '.join(comm)

    subprocess.run(["pwsh", "-Command", comm[:-1]], check=False)

    return