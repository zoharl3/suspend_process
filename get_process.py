
from ctypes import *
import win32api, win32process, win32con, win32event, win32gui

user32 = windll.user32
EnumWindowsProc = WINFUNCTYPE(c_int, c_int, c_int)

# Returns handles to windows with matching titles
def get_handle(title, classname):
    print('get_handle()')
    hwnds = []
    def EnumCB(hwnd, lparam, title = title, classname = classname, hwnds = hwnds):
        title2 = c_buffer(b' ' * 256)
        user32.GetWindowTextA(hwnd, title2, 255)
        classname2 = c_buffer(b' ' * 256)
        user32.GetClassNameA(hwnd, classname2, 255)
        #print(title2.value)
        #if title2.value.startswith(title) and (classname is None or classname2.value == classname):
        if title in str(title2.value) and (classname is None or str(classname2.value) == classname):
        #if title2.value == title:
            hwnds.append(hwnd)
            #print("Title:", title2.value)
            #print("Class name:", classname2.value)
#			return False
        return True

    user32.EnumWindows(EnumWindowsProc(EnumCB), 0)
    return hwnds

def test_process_file_name(pid, filename):
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    exe = win32process.GetModuleFileNameEx(handle, 0)
    win32api.CloseHandle(handle)
    #print(pid, exe)
    if exe.lower().find(filename.lower()) >= 0:
        return True
    else:
        return False
        
def get_pid_by_file_name(filename):
    processes = win32process.EnumProcesses()
    for pid in processes:
        try:
            if test_process_file_name(pid, filename):
                return pid
        except:
            pass
    return -1

# get process that matches file_find and has a window title_find
def get_pid_by_file_name_and_window_title( file_find, title_find ):
    pid = -1
    hwnds = get_handle(title_find, None)
    for hwnd in hwnds:
        (threadid, pidw) = win32process.GetWindowThreadProcessId(hwnd)
        if pidw and test_process_file_name(pidw, file_find):
            pid = pidw
            break
    return pid

# http://timgolden.me.uk/python/win32_how_do_i/find-the-window-for-my-subprocess.html
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        found_pid = -1
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        if 1:
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


