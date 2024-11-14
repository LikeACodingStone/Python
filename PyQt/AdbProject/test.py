import ctypes
import sys

def set_console_size(width, height):
    # 获取控制台句柄
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    
    # 设置缓冲区大小
    buffer_width = width // 6  # 大约每个字符6像素
    buffer_height = height // 12  # 大约每个字符12像素
    ctypes.windll.kernel32.SetConsoleScreenBufferSize(hwnd, ctypes.wintypes._COORD(buffer_width, buffer_height))

    # 设置窗口大小
    ctypes.windll.user32.MoveWindow(hwnd, 100, 100, width, height, True)

if __name__ == '__main__':
    # 设置命令行窗口的宽度和高度 (以像素为单位)
    set_console_size(800, 600)
    
    print("命令行窗口大小已更改。")