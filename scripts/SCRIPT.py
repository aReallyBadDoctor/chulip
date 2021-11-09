import os
from pynput.keyboard import Key, Controller
import win32gui
import re
from time import sleep
import pymem
import pymem.process
import pymem.memory

DMC5 = pymem.Pymem("pcsx2.exe")
handle = DMC5.process_handle
address = 0x212aaed0

def write_zeros(n):
    #val = [0 for i in range(int(n/2))]
    #if (n&1):
        #val.append(0x0D)
    #pymem.memory.write_bytes(handle,address,bytes(val),int((n+1)/2))
    if n == 0:
        return False
    val = 0xFF
    if (n&1):
        val = 0xF0
    addressOffset = int((n-1)/2)
    pymem.memory.write_bytes(handle,address+addressOffset,bytes([val]),1)
    return True



#write_halfbyte(3)

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

r = re.compile("PCSX2\.EXE.*")

NUMBER = 1024

keyboard = Controller()

def cycle(i):
    w.find_window_wildcard(".*nterlaced.*")
    w.set_foreground()
    write_zeros(i)
    matches = []
    while(len(matches)<1):
        #w.find_window_wildcard(".*nterlaced.*")
        #w.set_foreground()
        sleep(.01)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        sleep(.01)
        files = next(os.walk("G:/CHULIPTEST/pics"))[2]
        matches = list(filter(r.match,files))
    match = matches[0]
    try:
        os.rename("G:/CHULIPTEST/pics/"+match,"G:/CHULIPTEST/pics/"+str(i)+".bmp")
    except:
        sleep(.5)
        os.rename("G:/CHULIPTEST/pics/"+match,"G:/CHULIPTEST/pics/"+str(i)+".bmp")   

w = WindowMgr()
w.find_window_wildcard(".*nterlaced.*")
w.set_foreground()
for i in range(0,256*128):
    cycle(i)
