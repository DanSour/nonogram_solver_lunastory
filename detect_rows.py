import pytesseract
import cv2


def has_yellow_color(image):
    # Конвертируем в RGB)T
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Создаем маску для желтого цвета
    yellow_mask = cv2.inRange(rgb, (160,160,10), (255, 255, 50))
    
    # Проверяем есть ли желтые пиксели
    return cv2.countNonZero(yellow_mask) > 0


def has_white_color(image):
    white_mask = cv2.inRange(image, (160, 160, 160), (255, 255, 255))
    
    # Проверяем есть ли белые пиксели
    return cv2.countNonZero(white_mask) > 0


def ptshp_image(image, Blur=3):
    Blur = cv2.GaussianBlur(image, (Blur, Blur), 0)
    GRAY = cv2.cvtColor(Blur, cv2.COLOR_BGR2GRAY)
    THRESH = cv2.threshold(GRAY, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return THRESH

def improve_image_processing(image):
    # Использование адаптивной пороговой обработки вместо глобальной
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Использование контрастирования для улучшения видимости цифр
    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    return enhanced


def white_nums_recognition(image, custom_config, blur):
    
    result = pytesseract.image_to_string(ptshp_image(image, Blur=blur), config=custom_config)
    result = [int(char) for char in result[:-1] if char != '\n' and char.isdigit()]
    return result


def row_detector(image, puzzle_coords, puzzle_shape):

    puzzle_x_max, _ = puzzle_coords[0]
    puzzle_y_min, puzzle_y_max = puzzle_coords[1]
    puzzle_x_min = 0

    y_step = (puzzle_y_max - puzzle_y_min) / puzzle_shape 
    h = int(y_step)  # высота каждой строки будет одинаковой

    custom_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    ROWS_VALUES = []
    
    blurs = {
        5: 7,
        10: 3,
        15: 3,
        20: 1
    }

    for i in range(puzzle_shape):
        line = []
        
        # Рассчитываем точные границы с округлением до целого
        y_start = int(puzzle_y_min + i * y_step)
        y_end = int(puzzle_y_min + (i + 1) * y_step)

        # Обрезаем изображение по горизонтали
        cropped = image[y_start:y_end, puzzle_x_min:puzzle_x_max]

        if not has_yellow_color(cropped):
            result = white_nums_recognition(cropped, custom_config, blur=blurs[puzzle_shape])
            ROWS_VALUES.append(result)
            continue

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
