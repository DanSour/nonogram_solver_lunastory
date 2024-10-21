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
x_step = (x_max - x_min) / int(num_parts/2)
y_step = (y_max - y_min) / num_parts

# Проход по частям изображения
# Чикаем сверху-вниз и проходимся
for i in range(num_parts):
    # Рассчитываем точные границы с округлением до целого
    y_start = int(y_min + i * y_step)
    y_end = int(y_min + (i + 1) * y_step)

    # Чикаем слева-направо и проходимся
    for j in range(5):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(x_min + j * x_step)
        x_end = int(x_min + (j + 1) * x_step)

        cropped = image[y_start:y_end, x_start:x_end]

        # Передача в Tesseract
        custom_config = '--psm 6 digits'
        result = pytesseract.image_to_string(cropped, config=custom_config)
        print(result)

        # # Проверка результатов
        cv2.imshow('cropped', cropped)
        cv2.waitKey(0)

#     # Обрезаем изображение по горизонтали
#     # cropped = image[y_start:y_end, int(x_min+x_max*0.5):x_max]
#     cropped = image[y_start:y_end, x_min:x_max]

#     # Передача в Tesseract
#     custom_config = '--psm 6 digits'
#     result = pytesseract.image_to_string(cropped, config=custom_config)
#     print(result)

#     # Проверка результатов
#     cv2.imshow('cropped', cropped)
#     cv2.waitKey(0)

# cv2.destroyAllWindows()
