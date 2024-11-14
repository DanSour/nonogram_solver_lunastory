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

    # Ищем контуры квадратиков внутри, чтобы определить размер (15*15 или 20*20)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    square_contours = []
    for cnt in contours:
        cnt_x, cnt_y, cnt_w, cnt_h = cv2.boundingRect(cnt)
        aspect_ratio = float(cnt_w)/cnt_h
        area = cv2.contourArea(cnt)
        # Проверяем что контур примерно квадратный (соотношение сторон близко к 1)
        if 0.95 <= aspect_ratio <= 1.05 and area > 1000 and area < 20000:
            # Рисуем точку в центре каждого квадрата
            center_x = cnt_x + cnt_w // 2
            center_y = cnt_y + cnt_h // 2
            square_contours.append([x+center_x, y+center_y])

    return square_contours


def puzzle_mask(list_of_masks):
    # Начинаем с первой маски
    result_mask = list_of_masks[0]
    # Объединяем с остальными масками
    for mask in list_of_masks[1:]:
        result_mask = cv2.bitwise_or(result_mask, mask)
    return result_mask


def detect_puzzle(image):

    # Создаем маску для рассчета размерности паззла
    # for DeerMyFriend
    mask_dmf = cv2.inRange(image, (70, 47, 39), (255, 255, 255))
    # mask = cv2.inRange(image, (68, 47, 36), (255, 255, 255))
    # mask = cv2.inRange(image, (60, 37, 30), (255, 255, 255))
    # for normal
    mask_normal = cv2.inRange(image, (95, 69, 66), (255, 255, 255))
    # for big
    mask_big = cv2.inRange(image, (108, 93, 17), (255, 255, 255))
    mask = puzzle_mask([mask_dmf, mask_normal, mask_big])

    # Создаем маску для основного поля
    # field_mask = cv2.inRange(image, (90, 90, 90), (255, 255, 255))
    # Ищем контуры основного поля
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(field_contour)

    # Обрезаем по основному полю
    crop = mask[y:y+h, x:x+w]
    cv2.imshow('crop', crop)
    # cv2.imshow('crop', cv2.resize(crop, None, fx=0.45, fy=0.45))
    cv2.waitKey(0)

    cnt = cv2.findContours(crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image[y:y+h, x:x+w], cnt, -1, (255, 0,255), 2)
    cv2.imshow('image', cv2.resize(image, None, fx=0.45, fy=0.45))
    cv2.waitKey(0)

    print(len(cnt))

    return 


from take_frame import frame

field = detect_puzzle(frame())
print(field)

