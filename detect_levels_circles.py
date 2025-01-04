import cv2
import numpy as np
import pytesseract
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_circles(image) -> dict[str, list[list[int]]]:
    """
    Обнаруживает круги на изображении и распознает количество пройденных уровней внутри них.

    :param image: Изображение в формате numpy array.
    :return: Словарь с координатами центров кругов в формате {'circles': [[x1, y1], [x2, y2], ...]}.
    """
    try:
        height, width = image.shape[:2]
        
        # Обрезка изображения
        top = int(height * 0.31)
        bottom = int(height * 0.74)
        cutted_img = image[top:bottom, :].copy()

        # Преобразование в оттенки серого
        gray_img = cv2.cvtColor(cutted_img, cv2.COLOR_BGR2GRAY)

    # Применение алгоритма Хафа для обнаружения окружностей
        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=30, minRadius=int(0.0532786885 * width), maxRadius=int(0.0614754 * width))
                                    # param1=50, param2=30, minRadius=65, maxRadius=75)
        circles_centers_coords = []  # Список для хранения координат центров кругов

    # Проверка обнаружения кругов
        if circles is None:
            logging.warning("Круги на изображении не обнаружены.")
            return {'circles': circles_centers_coords}

        # Преобразование координат окружностей в целые числа с округлением
        circles = np.int16(np.round(circles))

        # Перебор всех найденных окружностей
        for circle in circles[0, :]:
            x, y = circle[:2]

            # Обрезка региона с числом уровней внутри окружности
            region_mid = y + int(height * 0.04)

            y_offset = int(0.011 * height)  # Отступ от центра зоны вверх-вниз
            x_offset = int(0.06481 * width)    # Отступ от центра зоны влево-вправо

            cutted_region = cutted_img[region_mid - y_offset: region_mid + y_offset, x - x_offset: x + x_offset]
            
            # Распознавание текста в обрезанной области
            text = pytesseract.image_to_string(cutted_region, config='--psm 7 -c tessedit_char_whitelist=0123456789/')
            # Удаление пробелов и разделение по '/'
            levels_text = text.strip().split('/')[0]
            # Проверка, является ли распознанный текст числом и входит ли он в диапазон от 0 до 25
            if levels_text.isdigit() and 0 <= int(levels_text) < 26:
                # Добавление координат центра окружности в список
                circles_centers_coords.append([x, y + top])

        circles_centers_coords.sort(key=lambda coord: (coord[1], coord[0]))  # Сортировка по x, затем по y

    except Exception as e:
        logging.error(f"Произошла ошибка при обнаружении кругов: {e}")
        return {'circles': []}
    
    return {'circles': circles_centers_coords}
