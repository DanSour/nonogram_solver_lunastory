import cv2

screenshot_path = "D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png"

# Загрузка изображения
image = cv2.imread(screenshot_path)
# Resize the image to be 50% smaller
width = int(image.shape[1] * 0.6)
height = int(image.shape[0] * 0.4)
image = cv2.resize(image, (width, height))

# Перевод в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применение порога для создания бинарного изображения
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)


# Нахождение контуров
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Отображение контуров на изображении
cv2.drawContours(image, contours, -1, (0, 0, 255), 2)

# Отображение изображения с контурами
cv2.imshow('Contours', image)
cv2.waitKey(0)
