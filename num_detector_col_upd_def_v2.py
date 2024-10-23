import cv2
import pytesseract

def col_detector(image_path, puzzle_shape):
    # Параметры обрезки
    x_min, x_max = 180, 1079  # Минимальные и максимальные координаты по x
    y_min, y_max = 0, 495     # Минимальные и максимальные координаты по y

    # image_path = f"D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot_temp.png"
    #-------------------------------------------------------------------------
    # # Пока идеальный вариант
    # #-------------------------------------------------------------------------
    # Чтение изображения
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
    
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #-------------------------------------------------------------------------

    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (x_max - x_min) / puzzle_shape
    # y_step = (y_max - y_min) / puzzle_shape
    COLS_VALUES = []

    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(x_min + i * x_step)
        x_end = int(x_min + (i + 1) * x_step)

        # Обрезаем изображение
        cropped = image[int(y_min+y_max*0.5):y_max, x_start:x_end]

        # Передача в Tesseract
        custom_config = '--psm 6 digits'
        result = pytesseract.image_to_string(cropped, config=custom_config)
        COLS_VALUES.append([int(char) for char in result[:-1].split('\n') if char.isdigit()] or [0])

    return COLS_VALUES 