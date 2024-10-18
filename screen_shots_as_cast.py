import subprocess
import cv2
import numpy as np
# from time import time

COMMAND = 'adb exec-out screencap -p'

while True:
#   tLast = time()

  # Capture the screen using adb
  png_stdout_bytes = subprocess.check_output(COMMAND)

  # Convert the stdout bytes to a numpy array
  png_bytes = np.frombuffer(png_stdout_bytes, np.uint8)

  # Decode the image from the numpy array
  img = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)

  # Resize the image to be 50% smaller
  width = int(img.shape[1] * 0.3)
  height = int(img.shape[0] * 0.3)
  resized_img = cv2.resize(img, (width, height))

#   fps = 1 / (time() - tLast)
#   cv2.putText(resized_img, f'FPS: {fps:.2f}', (10, 30),
#               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

  # Display the resized image
  cv2.imshow('Screen Capture', resized_img)
  cv2.waitKey(1)