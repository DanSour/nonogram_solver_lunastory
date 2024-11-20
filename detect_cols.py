import cv2
import pytesseract
import numpy as np

def rotate_image_simple(image, angle):
    height, width = image.shape[:2]
    center = (width//2, height//2)
    
    # Вычисляем новые размеры, чтобы избежать обрезки
    diagonal = int(np.sqrt(height**2 + width**2))
    new_height = diagonal
    new_width = diagonal
    
    # Создаем матрицу поворота
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Обновляем матрицу с учетом новых размеров
    M[0, 2] += (new_width - width) // 2
    M[1, 2] += (new_height - height) // 2
    
    # Применяем поворот
    rotated = cv2.warpAffine(image, M, (new_width, new_height), 
                            borderMode=cv2.BORDER_CONSTANT, 
                            # borderValue=(81, 80, 5)
                            borderValue=(83, 82, 5))
    return rotated

# ----------------------------------------------------------------------
def replace_color_range(image, from_color_min, from_color_max, to_color):
    """
    Заменяет диапазон цветов на новый цвет
    from_color_min, from_color_max - кортежи BGR для диапазона исходных цветов
    to_color - кортеж BGR для нового цвета
    """
    # Создаем маску для выбранного диапазона цветов
    mask = cv2.inRange(image, from_color_min, from_color_max)
    
    # Создаем копию изображения
    result = image.copy()
    
    # Заменяем цвета где mask == 255
    result[mask > 0] = to_color
    
    return result


def recognition(image, custom_config):

    # Передача в Tesseract
    image = cv2.inRange(image, (10, 191, 159), (255, 255, 255))

    wops_result = pytesseract.image_to_string(image, config=custom_config)
    result = wops_result
    
    # x2_cropped = cv2.resize(image, (0, 0), fx=2, fy=2)
    # x2_cropped_result = pytesseract.image_to_string(x2_cropped, config=custom_config)

    # rotatedl = rotate_image_simple(image, angle=-10)
    # rotatedl_result = pytesseract.image_to_string(rotatedl, config=custom_config)

    # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # mask = cv2.inRange(rgb, (211, 218, 14), (255, 255, 255))
    # mask = cv2.inRange(rgb, (180, 197, 14), (255, 255, 255))
    # mask_result = pytesseract.image_to_string(mask, config=custom_config)

    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # binary_result = pytesseract.image_to_string(binary_image, config=custom_config)

    # x2_binary_result = pytesseract.image_to_string(cv2.resize(binary_image, (0, 0), fx=2, fy=2), config=custom_config)

    # if len(result) == 0:
        # kernel = np.ones((2,2), np.uint8)
        # image = cv2.dilate(image, kernel, iterations=1)

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.inRange(image, (237, 237, 237), (255, 255, 255))
        # image = cv2.inRange(image, (160, 160, 160), (255, 255, 255)) # удаляет желтый цвет

        # wops_result = pytesseract.image_to_string(image, config=custom_config)

        # rotated = rotate_image_simple(image, angle=10)

        # rotated_10_result = pytesseract.image_to_string(image, config=custom_config)

        # x2_rotated_result = pytesseract.image_to_string(cv2.resize(image, (0, 0), fx=2, fy=2), config=custom_config)

    #     result = max([wops_result, rotated_10_result, x2_rotated_result], key=len)

    result = [int(char) for char in result[:-1].split('\n') if char.isdigit()] or []
    return result


def col_detector(image, puzzle_coords, puzzle_shape):
    puzzle_x_min, puzzle_x_max = puzzle_coords[0]
    puzzle_y_max, _ = puzzle_coords[1]
    puzzle_y_min = 0

    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (puzzle_x_max - puzzle_x_min) / puzzle_shape

    custom_config = '--psm 6 digits'
    # custom_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    COLS_VALUES = []

    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(puzzle_x_min + i * x_step)
        x_end = int(puzzle_x_min + (i + 1) * x_step)

        # Обрезаем изображение
        cropped = image[int(puzzle_y_min + puzzle_y_max * 0.5):puzzle_y_max, x_start + 0:x_end - 0]
        result = recognition(cropped, custom_config)
        COLS_VALUES.append(result)

    return COLS_VALUES 
