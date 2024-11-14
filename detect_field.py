import cv2


def detect_picture_field(image):
    # Создаем маску для основного поля
    field_mask = cv2.inRange(image, (90, 90, 90), (255, 255, 255))
    # Ищем контуры основного поля
    contours, _ = cv2.findContours(field_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(field_contour)

    crop = image[y:y+h, x:x+w]
    mask = cv2.inRange(crop, (250, 250, 250), (255, 255, 255))

    square = False
    aspect_ratio = float(w)/h
    if 0.9 <= aspect_ratio <= 1.1:
            square = True

    # Ищем контуры квадратиков внутри, чтобы определить размер (15*15 или 20*20)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    square_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        area = cv2.contourArea(cnt)
        # Проверяем что контур примерно квадратный (соотношение сторон близко к 1)
        if 0.95 <= aspect_ratio <= 1.05 and area > 1000 and area < 20000:
            square_contours.append(cnt)
            # Рисуем точку в центре квадрата
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(crop, (center_x, center_y), 5, (255, 0, 255), -1)
            cv2.imshow('crop', crop)
            cv2.waitKey(0)
            print(area)

    if square:
        shape = int(len(square_contours)**0.5)
    else:
        shape = None

    return {'coords':[[x, x+w], [y, y+h]], 'shape':shape} 


def puzzle_mask(list_of_masks):
    # Начинаем с первой маски
    result_mask = list_of_masks[0]
    # Объединяем с остальными масками
    for mask in list_of_masks[1:]:
        result_mask = cv2.bitwise_or(result_mask, mask)
    return result_mask


def detect_puzzle(image):

    # Создаем маску для основного поля
    field_mask = cv2.inRange(image, (90, 90, 90), (255, 255, 255))
    # Ищем контуры основного поля
    contours, _ = cv2.findContours(field_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(field_contour)
    # field = detect_field(image)

    # Обрезаем по основному полю
    crop = image[y:y+h, x:x+w]

    # crop = cv2.blur(crop, (5, 5))
    # Создаем маску для рассчета размерности паззла
    # for DeerMyFriend
    mask_dmf = cv2.inRange(crop, (70, 47, 39), (255, 255, 255))
    # mask = cv2.inRange(crop, (68, 47, 36), (255, 255, 255))
    # mask = cv2.inRange(crop, (60, 37, 30), (255, 255, 255))
    # for normal
    mask_normal = cv2.inRange(crop, (95, 69, 66), (255, 255, 255))
    # for big
    mask_big = cv2.inRange(crop, (108, 93, 17), (255, 255, 255))
    mask = puzzle_mask([mask_dmf, mask_normal, mask_big])


    return 


from take_frame import frame

field = detect_picture_field(frame())
print(field)

