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
                            borderValue=(83, 82, 5)
                            )
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

def extend_image_left(image, width_padding=100, height_padding=0, border_color=None):
    height, width = image.shape[:2]
    new_width = width + width_padding
    new_height = height + height_padding
    
    extended = np.full((new_height, new_width, 3), border_color, dtype=np.uint8)
    extended[height_padding:, width_padding:] = image
    
    return extended

# def recognition(image, custom_config):
#     image = extend_image_left(image, width_padding=100, height_padding=0, border_color=(80, 81, 5))
#     # image = rotate_image_simple(image, angle=-10)
#     # image = replace_color_range(image, (80, 80, 5), (86, 86, 6), (80, 81, 5))
#     # image = replace_color_range(image, (114, 114, 51), (255, 255, 255), (255, 255, 255))

    
#     # wops_result = pytesseract.image_to_string(image, config=custom_config)
#     wops_result = ocr.ocr(image)
#     print('wops_result\n', wops_result)
#     cv2.imshow('wops', image)

#     result = max([wops_result], key=len)
#     result = [int(char) for char in result[:-1] if char != '\n' and char.isdigit()]
#     cv2.waitKey(0)

#     return result

def recognition(image, custom_config):

    # image = replace_color_range(image, (80, 80, 5), (86, 86, 6), (80, 81, 5))
    # Передача в Tesseract
    # wops_result = pytesseract.image_to_string(image, config=custom_config)
    # print('wops_result\n', wops_result)
    # cv2.imshow('wops', image)

    x2_cropped = cv2.resize(image, (0, 0), fx=2, fy=2)
    x2_cropped_result = pytesseract.image_to_string(x2_cropped, config=custom_config)
    # print('x2_cropped_result\n', x2_cropped_result)
    # cv2.imshow('x2_cropped', x2_cropped)

    rotatedl = rotate_image_simple(image, angle=-10)
    rotatedl_result = pytesseract.image_to_string(rotatedl, config=custom_config)
    # print('rotatedl_result\n', rotatedl_result)
    # cv2.imshow('rotatedl', rotatedl)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.inRange(image, (211, 218, 14), (255, 255, 255))
    mask = cv2.inRange(rgb, (180, 197, 14), (255, 255, 255))
    mask_result = pytesseract.image_to_string(mask, config=custom_config)
    # print('mask_result\n', mask_result)
    # cv2.imshow('mask', mask)


    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binary_result = pytesseract.image_to_string(binary_image, config=custom_config)
    # print('binary_result\n', binary_result)
    # cv2.imshow('binary_image', binary_image)

    # x2_binary_result = pytesseract.image_to_string(cv2.resize(binary_image, (0, 0), fx=2, fy=2), config=custom_config)
    # print('binary_result2x\n', binary_result)
    # cv2.imshow('binary_image2x', cv2.resize(binary_image, (0, 0), fx=2, fy=2))
    
    # result = max([x2_cropped_result, binary_result, x2_binary_result], key=len)
    result = max([x2_cropped_result, mask_result, rotatedl_result, binary_result], key=len)


    if len(result) == 0:
        image = image[int(image.shape[0]*0.5):image.shape[0], :]
        # kernel = np.ones((2,2), np.uint8)
        # image = cv2.dilate(image, kernel, iterations=1)

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.inRange(image, (237, 237, 237), (255, 255, 255))
        # image = cv2.inRange(image, (160, 160, 160), (255, 255, 255))

        wops_result = pytesseract.image_to_string(image, config=custom_config)
        # print('wops_result\n', wops_result)
        # cv2.imshow('wops', image)

        rotated = rotate_image_simple(image, angle=10)

        rotated_10_result = pytesseract.image_to_string(rotated, config=custom_config)
        # print('rotated_10_result\n', rotated_10_result)
        # cv2.imshow('rotated', rotated)

        x2_rotated_result = pytesseract.image_to_string(cv2.resize(rotated, (0, 0), fx=2, fy=2), config=custom_config)
        # print('x2_rotated_result\n', x2_rotated_result)
        # cv2.imshow('x2_rotated', cv2.resize(rotated, (0, 0), fx=2, fy=2))

        result = max([wops_result, rotated_10_result, x2_rotated_result], key=len)
        # cv2.waitKey(0)

    result = [int(char) for char in result[:-1].split('\n') if char.isdigit()] or []
    cv2.waitKey(0)
    return result


def col_detector(image, puzzle_coords, puzzle_shape):
    
    puzzle_x_min, puzzle_x_max = puzzle_coords[0]
    puzzle_y_max, _ = puzzle_coords[1]
    puzzle_y_min = 0

    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (puzzle_x_max - puzzle_x_min) / puzzle_shape

    # custom_config = '--psm 6 digits'
    custom_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    COLS_VALUES = []

    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(puzzle_x_min + i * x_step)
        x_end = int(puzzle_x_min + (i + 1) * x_step)

        # Обрезаем изображение
        # cropped = image[:, x_start+7:x_end-5]
        cropped = image[int(puzzle_y_min+puzzle_y_max*0.5):puzzle_y_max, x_start+7:x_end-5]
        result = recognition(cropped, custom_config)
        COLS_VALUES.append(result)

    return COLS_VALUES 


# from detect_field import detect_field_coords
# from take_frame import frame
# import cv2

# det = col_detector(frame(), 
#                    puzzle_coords=detect_field_coords(frame()), 
#                    puzzle_shape= 20)
# print(det)
