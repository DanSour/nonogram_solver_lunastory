import cv2
import pytesseract

# Параметры обрезки
x_min, x_max = 0, 180  # Минимальные и максимальные координаты по x
y_min, y_max = 495, 1394     # Минимальные и максимальные координаты по y

# Количество частей, на которые нужно разрезать изображение
num_parts = 10

# Загрузка изображения
image_path = f"D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot_{num_parts}x{num_parts}.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Шаг по y (используем float для более точного расчета)
y_step = (y_max - y_min) / num_parts
ROWS_VALUES = []
# Проход по частям изображения
for i in range(num_parts):
    # Рассчитываем точные границы с округлением до целого
    y_start = int(y_min + i * y_step)
    y_end = int(y_min + (i + 1) * y_step)

    # Обрезаем изображение по горизонтали
    # cropped = image[y_start:y_end, int(x_min+x_max*0.5):x_max]
    cropped = image[y_start:y_end, x_min:x_max]

    # Передача в Tesseract
    custom_config = '--psm 6 digits'
    result = pytesseract.image_to_string(cropped, config=custom_config)
    '''
    '''
    try:
        if int(result) > 10:
            # Разбиваем строку на отдельные цифры и преобразуем их в список целых чисел
            result = [int(char) for char in result if char != '\n']
        else:
            # Преобразуем строку в список, содержащий одно число
            result = [int(result)]
        ROWS_VALUES += [result]
        print(result)
    except:
        ROWS_VALUES.append([0])
        print([0])

    # Проверка результатов
    cv2.imshow('cropped', cropped)
    cv2.waitKey(0)

print(ROWS_VALUES)
cv2.destroyAllWindows()
