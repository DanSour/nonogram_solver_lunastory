import cv2
import pytesseract
import numpy as np

def row_detector(image_path, puzzle_coords, puzzle_shape):
    puzzle_xs, puzzle_ys = puzzle_coords
    puzzle_x_min, puzzle_x_max = puzzle_xs
    puzzle_y_min, puzzle_y_max = puzzle_ys
    # puzzle_y_min, puzzle_y_max = 495, 1394  # Минимальные и максимальные координаты по y

    puzzle_x_min, puzzle_x_max = 0, puzzle_x_min  # Минимальные и максимальные координаты по x

    # Чтение изображения
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
    
    image = cv2.filter2D(image, -1, np.array([[0, -1, 0],
                                                [-1, 5, -1],
                                                [0, -1, 0]]))
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Шаг по y (используем float для более точного расчета)
    y_step = (puzzle_y_max - puzzle_y_min) / puzzle_shape 
    ROWS_VALUES = []
    
    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        y_start = int(puzzle_y_min + i * y_step)
        y_end = int(puzzle_y_min + (i + 1) * y_step)

        # Обрезаем изображение по горизонтали
        cropped = image[y_start:y_end, puzzle_x_min:puzzle_x_max]

        # Передача в Tesseract
        custom_config = '--psm 6 digits'
        result = pytesseract.image_to_string(cropped, config=custom_config)
        if result[:-1].isdigit():
            if int(result) > 10:
                # Разбиваем строку на отдельные цифры и преобразуем их в список целых чисел
                result = [int(char) for char in result[:-1] if char != '\n']
            else:
                # Преобразуем строку в список, содержащий одно число
                result = [int(result)]
            ROWS_VALUES += [result]
        else:
            ROWS_VALUES.append([0])

    return ROWS_VALUES