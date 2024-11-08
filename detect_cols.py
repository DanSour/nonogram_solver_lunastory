import cv2
import pytesseract
import numpy as np


def ptshp_image(image):
    # Blur = cv2.GaussianBlur(image, (5, 5), 0)
    Blur = cv2.GaussianBlur(image, (3, 3), 0)
    GRAY = cv2.cvtColor(Blur, cv2.COLOR_BGR2GRAY)
    THRESH = cv2.threshold(GRAY, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    return THRESH


def improve_image_processing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return enhanced


def recognition(image, custom_config):

    # Передача в Tesseract
    wops_result = pytesseract.image_to_string(image, config=custom_config)
    # print('wops_result', wops_result)
    # cv2.imshow('wops', image)
    
    cropped = cv2.resize(image, (0, 0), fx=1.4, fy=1.4)
    croped_result = pytesseract.image_to_string(cropped, config=custom_config)
    # ps_result = pytesseract.image_to_string(ptshp_image(image), config=custom_config)
    # print('ps_result', ps_result)
    # cv2.imshow('ptshp_image', ptshp_image(image))
    
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_result = pytesseract.image_to_string(gray_image, config=custom_config)
    # print('gray_result', gray_result)
    # cv2.imshow('gray_image', gray_image)
    
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # binary_result = pytesseract.image_to_string(binary_image, config=custom_config)
    # print('binary_result', binary_result)
    # cv2.imshow('binary_image', binary_image)
    
    # improve_result = pytesseract.image_to_string(improve_image_processing(image), config=custom_config)
    # print('improve_result', improve_result)
    # cv2.imshow('improve', improve_image_processing(image))
    
    # result = max([wops_result, ps_result, improve_result], key=len)
    result = max([wops_result, croped_result], key=len)

    result = [int(char) for char in result[:-1].split('\n') if char.isdigit()] or []
    # cv2.waitKey(0)
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
        cropped = image[int(puzzle_y_min+puzzle_y_max*0.5):puzzle_y_max, x_start:x_end]
        result = recognition(cropped, custom_config)
        COLS_VALUES.append(result)

    return COLS_VALUES 


# from detect_field import detect_field_coords
# # from frame_take import frame
# import cv2

# # img = cv2.imread(r'screenshots\screenshot_20x20_.png')
# img = cv2.imread(r'screenshots\screenshot_temp.png')
# img = cv2.resize(img, (0, 0), fx=1.4, fy=1.4)

# # puzzle_coords = detect_field_coords(frame())
# det = col_detector(img, 
#                    puzzle_coords=detect_field_coords(img), 
#                    puzzle_shape= 20)
# # print(answer == det)
# print(det)
# # print(col_detecto r(frame(), puzzle_coords, puzzle_shape))