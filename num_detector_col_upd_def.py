import cv2
import pytesseract

def col_detector():
    # Параметры обрезки
    x_min, x_max = 180, 1079  # Минимальные и максимальные координаты по x
    y_min, y_max = 0, 495     # Минимальные и максимальные координаты по y

    # Количество частей, на которые нужно разрезать изображение
    num_parts = 10

    # Загрузка изображения
    image_path = f"D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot_temp.png"
    #-------------------------------------------------------------------------
    # # Пока идеальный вариант
    # #-------------------------------------------------------------------------
    # image = cv2.imread(image_path)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #-------------------------------------------------------------------------

    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (x_max - x_min) / num_parts
    y_step = (y_max - y_min) / num_parts
    COLS_VALUES = []

    # Проход по частям изображения
    # Чикаем слева-направо и проходимся
    
    for i in range(num_parts):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(x_min + i * x_step)
        x_end = int(x_min + (i + 1) * x_step)
        
        # Чикаем сверху-вниз и проходимся
        one_column = []
        for j in range(num_parts):
            # Рассчитываем точные границы с округлением до целого
            y_start = int(y_min + j * y_step)
            y_end = int(y_min + (j + 1) * y_step)

            cropped = image[y_start:y_end, x_start:x_end]
            
            cropped = cv2.resize(cropped, 
                            (int(cropped.shape[1] * 2), 
                                int(cropped.shape[0] * 2)), 
                            interpolation=cv2.INTER_LINEAR)

            # Передача в Tesseract
            custom_config = '--psm 6 digits'
            result = pytesseract.image_to_string(cropped, config=custom_config)
            try:
                if int(result):
                    one_column.append(int(result))
            except:
                pass
        if one_column == []:
            one_column.append(0)
        COLS_VALUES.append(one_column)
    return COLS_VALUES 