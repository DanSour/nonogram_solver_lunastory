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
    
    # Создаем маску для белого цвета
    white_mask = cv2.inRange(rgb, (160, 160, 160), (255, 255, 255))
    
    # Проверяем есть ли желтые пиксели
    return cv2.countNonZero(white_mask) > 0


def ptshp_image(image):
    Blur = cv2.GaussianBlur(image, (7, 7), 0)
    GRAY = cv2.cvtColor(Blur, cv2.COLOR_BGR2GRAY)
    THRESH = cv2.threshold(GRAY, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return THRESH

def improve_image_processing(image):
    # 1. Использование адаптивной пороговой обработки вместо глобальной
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # # 2. Применение морфологических операций для удаления шума
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # cv2.imshow('opening', opening)
    # cv2.waitKey(0)
    
    # 3. Использование контрастирования для улучшения видимости цифр
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    # cv2.imshow('enhanced', enhanced)
    # cv2.waitKey(0)
    
    # 4. Применение детектора границ для выделения контуров цифр
    # edges = cv2.Canny(enhanced, 100, 200)
    # cv2.imshow('edges', edges)
    # cv2.waitKey(0)
    return enhanced


def white_nums_recognition(image, custom_config, reader):
    
    wops_result = pytesseract.image_to_string(image, config=custom_config)
    '''
        # ps_result = pytesseract.image_to_string(ptshp_image(image), config=custom_config)
        # print('ps_result', ps_result)
        # cv2.imshow('white_mask', ptshp_image(image))

        wops_result = pytesseract.image_to_string(
                                                cv2.GaussianBlur(image, (5, 5), 0), 
                                                config=custom_config
                                                )
        # print('wops_result', wops_result)
        # cv2.imshow('GaussianBlur', cv2.GaussianBlur(image, (5, 5), 0))

        improve_result = pytesseract.image_to_string(improve_image_processing(image), config=custom_config)
        # print('improve_result', improve_result)
        # cv2.imshow('improve', improve_image_processing(image))
        # cv2.waitKey(0)

        result = max([improve_result, wops_result, ps_result], key=len)
        result = reader.readtext(image, detail=0)
    '''     
    result = max([wops_result], key=len)

    result = [int(char) for char in result[:-1] if char != '\n' and char.isdigit()]
    # print(result)
    # cv2.imshow('white_mask', THRESH)
    # cv2.waitKey(0)
    return result


def row_detector(image, puzzle_coords, puzzle_shape, reader=None):

    puzzle_x_max, _ = puzzle_coords[0]
    puzzle_y_min, puzzle_y_max = puzzle_coords[1]
    puzzle_x_min = 0

    # custom_config = '--psm 6 digits'
    custom_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    ROWS_VALUES = []

    # image = cv2.filter2D(image, -1, np.array([[0, -1, 0],
    #                                         [-1, 5, -1],
    #                                         [0, -1, 0]]))

    y_step = (puzzle_y_max - puzzle_y_min) / puzzle_shape 
    h = int(y_step)  # высота каждой строки будет одинаковой
    
    # image = cv2.GaussianBlur(image, (6, 6), 0)

    # # Сделать мыльницу из цифр
    # kernel = np.ones((2,2), np.uint8)
    # dil = cv2.dilate(image, kernel, iterations=1)
    
    # erode = cv2.erode(cropped, kernel, cv2.BORDER_REFLECT)  
    
    for i in range(puzzle_shape):
        line = []
        
        # Рассчитываем точные границы с округлением до целого
        y_start = int(puzzle_y_min + i * y_step)
        y_end = int(puzzle_y_min + (i + 1) * y_step)

        # Обрезаем изображение по горизонтали
        cropped = image[y_start:y_end, puzzle_x_min:puzzle_x_max]
        
        if not has_yellow_color(cropped):
            result = white_nums_recognition(cropped, custom_config, reader)
            ROWS_VALUES.append(result)
            continue

        # if h == None:
        #     h = cropped.shape[0]
       
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
                    continue
                temp_yell_num+=digit[0]
                
            elif has_white_color(cropped_digit):
                line.append(int(digit[0]))
        ROWS_VALUES.append(line)

    return ROWS_VALUES



# from detect_field import detect_field_coords
# # from frame_take import frame
# import cv2

# img = cv2.imread(r'screenshots\screenshot_temp.png')
# # puzzle_coords = detect_field_coords(frame())
# det = row_detector(img, 
#                    puzzle_coords=detect_field_coords(img), 
#                    puzzle_shape= 20)
# # print(answer == det)
# print(det)
# # print(col_detecto r(frame(), puzzle_coords, puzzle_shape))