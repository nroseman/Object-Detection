import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture


wincap = WindowCapture('Idle Tower Builder')

loop_time = time()
while True:
    
    screenshot = wincap.get_screenshot()

    cv.imshow('Result', screenshot)

    
    print(f'FPS {1 / (time() - loop_time)}')
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

# Debug Screenshot
# screenshot = wincap.get_screenshot()
# cv.imwrite('Debug.bmp', screenshot)