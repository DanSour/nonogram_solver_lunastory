import subprocess
import cv2
import numpy as np

while True:

  # Capture the screen using adb
  png_stdout_bytes = subprocess.check_output("adb exec-out screencap -p ")

  # Convert the stdout bytes to a numpy array
  png_bytes = np.frombuffer(png_stdout_bytes, np.uint8)

  # Decode the image from the numpy array
  img = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)

  # Resize the image to be 50% smaller
  width = int(img.shape[1] * 0.3)
  height = int(img.shape[0] * 0.3)
  img = cv2.resize(img, (width, height))
