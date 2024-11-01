import cv2
import pytesseract


def ptshp_image(image):
    Blur = cv2.GaussianBlur(image, (5, 5), 0)
    GRAY = cv2.cvtColor(Blur, cv2.COLOR_BGR2GRAY)
    THRESH = cv2.threshold(GRAY, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    return THRESH


def col_detector(image, puzzle_coords, puzzle_shape):
    
    puzzle_x_min, puzzle_x_max = puzzle_coords[0]
    puzzle_y_max, _ = puzzle_coords[1]
    puzzle_y_min = 0


    # Шаг по x и по y (используем float для более точного расчета)
    x_step = (puzzle_x_max - puzzle_x_min) / puzzle_shape

    custom_config = '--psm 6 digits'
    COLS_VALUES = []

    # Проход по частям изображения
    for i in range(puzzle_shape):
        # Рассчитываем точные границы с округлением до целого
        x_start = int(puzzle_x_min + i * x_step)
        x_end = int(puzzle_x_min + (i + 1) * x_step)

        # Обрезаем изображение
        cropped = image[int(puzzle_y_min+puzzle_y_max*0.5):puzzle_y_max, x_start:x_end]

        # Передача в Tesseract
        # result = pytesseract.image_to_string(cropped, config=custom_config)
        ps_result = pytesseract.image_to_string(ptshp_image(cropped), config=custom_config)
        wops_result = pytesseract.image_to_string(cropped, config=custom_config)
        result = max(ps_result, wops_result, key=len)

        COLS_VALUES.append([int(char) for char in result[:-1].split('\n') if char.isdigit()] or [])
        # print(result)
        # cv2.imshow('cropped', cropped)
        # cv2.waitKey(0)

    return COLS_VALUES 


# from detect_field import detect_field_coords
# from frame_take import frame

# puzzle_coords = detect_field_coords(frame())
# puzzle_shape = 15

# print(col_detector(frame(), puzzle_coords, puzzle_shape))