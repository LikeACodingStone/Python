import ctypes
import time


def writeLog():
    with open("C:\\Users\\a1294.zhou\\WorkingFiles\\NotePad_Files\\Log_shutdown\\winL_Log.txt", "a") as f:
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        f.write(f"Win + L pressed at::: {current_time}\n")
        f.close()

def is_screen_locked():
    user32 = ctypes.windll.user32
    return user32.GetForegroundWindow() == 0
    
if __name__ == "__main__":
    SW_HIDE = 0
    W_SHOW = 5
    lockCount = 0 
    while True:
        if is_screen_locked():
            if lockCount == 0:
                writeLog()
                lockCount = lockCount + 1
        else:
            lockCount = 0
        time.sleep(3)