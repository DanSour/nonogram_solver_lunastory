import pytesseract
import cv2
import numpy as np


def has_yellow_color(image):
    # Конвертируем в RGB)T
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Создаем маску для желтого цвета
    # yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
    yellow_mask = cv2.inRange(rgb, (160,160,10), (255, 255, 50))
    
    # Проверяем есть ли желтые пиксели
    return cv2.countNonZero(yellow_mask) > 0


def has_white_color(image):
    # Конвертируем в RGB)T
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Создаем маску для желтого цвета
    # yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
    # white_mask = cv2.inRange(rgb, (160,160,10), (255, 255, 50))
    white_mask = cv2.inRange(rgb, (160, 160, 160), (255, 255, 255))
    
    # Проверяем есть ли желтые пиксели
    return cv2.countNonZero(white_mask) > 0


def white_nums_recognition(image, custom_config):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    white_mask = cv2.inRange(rgb, (160, 160, 160), (255, 255, 255))
    result = pytesseract.image_to_string(white_mask, config=custom_config)
    result = [int(char) for char in result[:-1] if char != '\n']
    return result


def row_detector(image, puzzle_coords, puzzle_shape):

    puzzle_x_max, _ = puzzle_coords[0]
    puzzle_y_min, puzzle_y_max = puzzle_coords[1]
    puzzle_x_min = 0

    h = None
    custom_config = '--psm 6 digits'
    ROWS_VALUES = []

    # image = cv2.filter2D(image, -1, np.array([[0, -1, 0],
    #                                         [-1, 5, -1],
    #                                         [0, -1, 0]]))

    y_step = (puzzle_y_max - puzzle_y_min) / puzzle_shape 
    
    # image = cv2.GaussianBlur(image, (6, 6), 0)

    # # Сделать мыльницу из цифр
    # kernel = np.ones((2,2), np.uint8)
    # dil = cv2.dilate(image, kernel, iterations=1)
    
    # kernel = np.ones((2, 2), np.uint8) 
    # erode = cv2.erode(cropped, kernel, cv2.BORDER_REFLECT)  
    
    image = cv2.filter2D(image, -1, np.array([[0, -1, 0],
                                            [-1, 5, -1],
                                            [0, -1, 0]]))

            
    for i in range(puzzle_shape):
        line = []
        
        # Рассчитываем точные границы с округлением до целого
        y_start = int(puzzle_y_min + i * y_step)
        y_end = int(puzzle_y_min + (i + 1) * y_step)

        # Обрезаем изображение по горизонтали
        cropped = image[y_start:y_end, puzzle_x_min:puzzle_x_max]
        # cv2.imshow('cropped', cropped)
        # cv2.waitKey(0)
        
        if not has_yellow_color(cropped):
            result = white_nums_recognition(cropped, custom_config)
            ROWS_VALUES.append(result)
            continue

        if h == None:
            h = cropped.shape[0]
       
        # Передача в Tesseract
        boxes = pytesseract.image_to_boxes(cropped, config=custom_config)
        temp_yell_num=''
        for digit_info in boxes.splitlines():
            digit = digit_info.split(' ')
            cropped_digit = cropped[h - int(digit[4]) : h - int(digit[2]), int(digit[1]) : int(digit[3])]
            
            if has_yellow_color(cropped_digit):
                if temp_yell_num != '':
                    line.append(int(temp_yell_num+digit[0]))
                    temp_yell_num = ''
                # digit[-1] = 'y'
                temp_yell_num+=digit[0]
                pass
            elif has_white_color(cropped_digit):
                # digit[-1] = 'w'
                line.append(int(digit[0]))
        ROWS_VALUES.append(line)

        # print(result)

    return ROWS_VALUES

# path = r'screenshots\screenshot_temp.png'
# image = cv2.imread(path)
# puzzle_coords = [[180, 1079], [495, 1394]]
# puzzle_shape = 15

# print(row_detector(image, puzzle_coords, puzzle_shape))