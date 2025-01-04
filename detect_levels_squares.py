import cv2
import pytesseract
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_squares(img):
    """
    Обнаруживает квадраты на изображении и распознает какие из них не пройдены.

    :param img: Изображение в формате numpy array.
    :return: Словарь с координатами центров квадратов 
    """
    height, width = img.shape[:2]
    
    try:
        # Обрезка изображения с использованием процентов от высоты
        top = int(0.4 * height)
        bottom = int(0.74 * height)
        image = img[top:bottom, :].copy()
        # Обработка изображения
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # Алгоритм нахождения границ Canny
        edged = cv2.Canny(gray, 50, 150)

        # Находим все возможные контуры в обрезанном (центре) изображении
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Создаем список, туда будем записывать местоположения нерешенных квадратов
        square_centers = []
        # Перебор всех найденных контуров
        for contour in contours:
            
            # Аппроксимируем контур многоугольником с точностью 2%
            approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
            # Проверяем, что фигура имеет четыре угла, что может указывать на квадрат
            if len(approx) == 4:
                # Вычисляем прямоугольник, охватывающий контур
                cnt_x, cnt_y, cnt_w, cnt_h = cv2.boundingRect(approx)
                # Вычисляем площадь контура
                area = cv2.contourArea(approx)
                # Вычисляем соотношение сторон контура
                aspect_ratio = float(cnt_w) / cnt_h
                # Проверяем, является ли соотношение сторон близким к единице и площадь контура достаточной
                if (aspect_ratio >= 0.95 and aspect_ratio <= 1.05) and area >= 20:
                    # Вычисляем центр контура по оси X
                    center_x = cnt_x + cnt_w // 2
                    # Вычисляем центр контура по оси Y
                    center_y = cnt_y + cnt_h // 2

                    # Обрезаем область вокруг центра квадрата для распознавания текста
                    y_offset = int(0.011 * height)  # Отступ от центра зоны вверх-вниз
                    x_offset = int(0.06481 * width)  # Отступ от центра зоны влево-вправо
                    cutted_region = image[center_y - y_offset: center_y + y_offset, center_x - x_offset: center_x + x_offset]
                    text = pytesseract.image_to_string(cutted_region, config='--psm 7 -c tessedit_char_whitelist=/ ')
                    # Если есть текст - значит уровень пройден, если нет - не пройден, он нам и нужен
                    if text == '':
                        # Добавляем центр квадрата в список
                        square_centers.append([center_x, center_y + top])
        # Сортируем центры квадратов сначала по оси X, затем по оси Y
        square_centers.sort(key=lambda center: (center[1], center[0]))

    except Exception as e:
            logging.error(f"Произошла ошибка при обнаружении квадратов: {e}")
            return {'squares': square_centers}

    return {'squares': square_centers}
