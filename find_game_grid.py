import cv2
# from screenshot import screenshot

# screenshot_path = "D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot_10x10.png"
screenshot_path = "D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png"

# Загрузка изображения
image = cv2.imread(screenshot_path) # ориг
# image = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)

# # Перевод в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применение порога для создания бинарного изображения
binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1] # ориг

# Нахождение контуров
contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

board = sorted(contours, key=len)[16]
print(board)

# НАРИСОВАТЬ

# Отображение изображения с контурами
cv2.drawContours(image, board, -1, (0, 0, 255), 5)
# Resize the image to be 50% smaller
width = int(image.shape[1] * 0.45)
height = int(image.shape[0] * 0.45)
image = cv2.resize(image, (width, height))
cv2.imshow('Contours', image)
cv2.waitKey(0)