import cv2
import pytesseract
import numpy as np
from detect_rows import ptshp_image

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


def recognition(image, custom_config, blur):

    # Передача в Tesseract
    result = pytesseract.image_to_string(image, config=custom_config)
    result = [int(char) for char in result[:-1].split('\n') if char.isdigit()] or []
    return result


def col_detector(image, puzzle_coords, puzzle_shape):

    puzzle_x_min, puzzle_x_max = puzzle_coords[0]
    puzzle_y_max, _ = puzzle_coords[1]
    puzzle_y_min = 0

    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (puzzle_x_max - puzzle_x_min) / puzzle_shape

    custom_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    COLS_VALUES = []
 
    blurs = {
        5: 7,
        10: 3,
        15: 3,
        20: 7
    }

    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(puzzle_x_min + i * x_step)
        x_end = int(puzzle_x_min + (i + 1) * x_step)

        # Обрезаем изображение
        cropped = image[int(puzzle_y_min + puzzle_y_max * 0.5):puzzle_y_max, x_start + 0:x_end - 0]
        result = recognition(cropped, custom_config, blur=blurs[puzzle_shape])
        COLS_VALUES.append(result)

    return COLS_VALUES 
