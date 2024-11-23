import cv2 
import pytesseract
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_squares(img):
    """
    Обнаруживает квадраты на изображении и распознает какие из них не пройдены.

    :param image: Изображение в формате numpy array.
    :return: Словарь с координатами центров квадратов 
    """
    try:
        # Обрезка изображения
        image = img[940:1800, :].copy()

        # Обработка изображения
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # Алгоритм нахождения границ Canny
        edged = cv2.Canny(gray, 50, 150)

        # Находим все возможные контуры в обрезанном (центре) изображения
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Создаем список, туда будем записывать местоположения нерешенных квадратов
        square_centers = []
        # Перебор всех найденных контуров
        for contour in contours:
            
            # Аппроксимируем контур многоугольником с точностью 2%
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            # Проверяем, что фигура имеет четыре угла, что может указывать на квадрат
            if len(approx) == 4:
                # x, y, w, h = cv2.boundingRect(approx)
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
                    # Обрезаем там где есть текст
                    cutted_region = img[center_y+750 + 265: center_y+750 + 305, center_x - 90: center_x + 90]
                    text = pytesseract.image_to_string(cutted_region, config='--psm 3')
                    # Если есть текст - значит уровень пройден, если нет - не пройден, он нам и нужен
                    if text == '':
                        # Добавляем центр квадрата в список
                        square_centers.append([center_x, center_y+940])

    except Exception as e:
            logging.error(f"Произошла ошибка при обнаружении квадратов: {e}")
            return {'squares': square_centers}

    return {'squares':square_centers}
