import win32gui, win32ui, win32con
import numpy as np

class WindowCapture:

    def __init__(self, window_name) -> None:
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window not found {window_name}')
        
        # Get Window Size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # Remove Titlebar and Borders
        self.titlebar_pixels = 30
        self.border_pixels = 8
        self.w = self.w - (self.border_pixels * 2)
        self.h = self.h - self.titlebar_pixels - self.border_pixels

        # Set Offset for Accurate Screen Positions
        self.offset_x = window_rect[0] + self.border_pixels
        self.offset_y = window_rect[1] + self.titlebar_pixels

    def get_screenshot(self):
        # Fast screen capture code from https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.border_pixels, self.titlebar_pixels), win32con.SRCCOPY)

        # Save Screenshot
        # dataBitMap.SaveBitmapFile(cDC, Debug.bmp)

        # Convert BMP to NP Array
        signed_ints_array = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Return OpenCV-compatible array
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img
    
    def get_screen_position(self, pos):
        # Disclaimer: Do not move window after running main.py, or these values will be off
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)