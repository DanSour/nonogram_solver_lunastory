import cv2
import pytesseract

def col_detector(image, puzzle_coords, puzzle_shape):
    # # Параметры обрезки
    # puzzle_xs, puzzle_ys = puzzle_coords
    # puzzle_x_min, puzzle_x_max = puzzle_xs
    # puzzle_y_min, puzzle_y_max = puzzle_ys

    # # puzzle_x_min, puzzle_x_max = 180, 1079  # Минимальные и максимальные координаты по x
    # puzzle_y_min, puzzle_y_max = 0, puzzle_y_min     # Минимальные и максимальные координаты по y
    
    puzzle_x_min, puzzle_x_max = puzzle_coords[0]
    puzzle_y_max, _ = puzzle_coords[1]
    puzzle_y_min = 0

    #-------------------------------------------------------------------------
    # # Пока идеальный вариант
    # #-------------------------------------------------------------------------
    # Чтение изображения
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # #-------------------------------------------------------------------------
    image = cv2.GaussianBlur(image, (3, 3), 0)
    
    # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.inRange(rgb, (68, 125, 125), (255, 255, 255))
    # image = cv2.inRange(rgb, (47, 110, 112), (255, 255, 255))
    # #-------------------------------------------------------------------------
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #-------------------------------------------------------------------------

    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (puzzle_x_max - puzzle_x_min) / puzzle_shape
    # y_step = (puzzle_y_max - puzzle_y_min) / puzzle_shape

    custom_config = '--psm 6 digits'
    COLS_VALUES = []

    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(puzzle_x_min + i * x_step)
        x_end = int(puzzle_x_min + (i + 1) * x_step)

        # Обрезаем изображение
        cropped = image[int(puzzle_y_min+puzzle_y_max*0.5):puzzle_y_max, x_start:x_end]

        # Передача в Tesseract
        result = pytesseract.image_to_string(cropped, config=custom_config)
        COLS_VALUES.append([int(char) for char in result[:-1].split('\n') if char.isdigit()] or [])

    return COLS_VALUES 