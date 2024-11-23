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
        # Обрезка изображения
        cutted_img = image[750:1750, :].copy()

    # Преобразование в оттенки серого
        gray_img = cv2.cvtColor(cutted_img, cv2.COLOR_BGR2GRAY)

    # Применение алгоритма Хафа для обнаружения окружностей
        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=50, param2=30, minRadius=60, maxRadius=64)
    
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
            cutted_region = image[y+750 + 75: y+750 + 120, x - 70: x + 70]
            # Распознавание текста в обрезанной области
            text = pytesseract.image_to_string(cutted_region, config='--psm 7 -c tessedit_char_whitelist=0123456789/')
            # Удаление пробелов и разделение по '/'
            levels_text = text.strip().split('/')[0]
            # Проверка, является ли распознанный текст числом и входит ли он в диапазон от 0 до 25
            if levels_text.isdigit() and 0 <= int(levels_text) < 26:
                # Добавление координат центра окружности в список
                circles_centers_coords.append([x, y+750])

    except Exception as e:
        logging.error(f"Произошла ошибка при обнаружении кругов: {e}")
        return {'circles': circles_centers_coords}

    return {'circles': circles_centers_coords}
