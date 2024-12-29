
import win32api, win32process, win32con, win32event, win32gui, win32console
import time
from ctypes import *

user32 = windll.user32
EnumWindowsProc = WINFUNCTYPE( c_int, c_int, c_int )

# To get a process's parent:
#     psutil.Process().ppid()

# Returns handles to windows with matching titles
def get_handle( title, classname ):
    #print('get_handle()')
    hwnds = []
    def EnumCB(hwnd, lparam, title = title, classname = classname, hwnds = hwnds):
        title2 = c_buffer(b' ' * 256)
        user32.GetWindowTextA(hwnd, title2, 255)
        title2 = title2.value.decode('UTF-8')
        
        classname2 = c_buffer(b' ' * 256)
        user32.GetClassNameA(hwnd, classname2, 255)
        classname2 = classname2.value.decode('UTF-8')
        
        #print( title2, classname2 )
        #if title2.value.startswith(title) and (classname is None or classname2.value == classname):
        if title in title2 and ( classname is None or classname2 == classname ):
        #if title2 == title:
            hwnds.append(hwnd)
            #print("Title:", title2)
            #print("Class name:", classname2)
            #return False
        return True

    user32.EnumWindows( EnumWindowsProc( EnumCB ), 0 )
    return hwnds
    
def test_process_file_name( pid, filename) :
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    exe = win32process.GetModuleFileNameEx(handle, 0)
    win32api.CloseHandle(handle)
    #print(pid, exe)
    if exe.lower().find(filename.lower()) >= 0:
        return True
    else:
        return False
        
def get_pid_by_file_name( filename ):
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
def get_hwnds_for_pid( pid ):
    def callback( hwnd, hwnds ):
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

# https://stackoverflow.com/questions/78946027/change-console-icon-on-taskbar/78948103#78948103
def set_console_title_and_icon( title, img ):
    # give it a unique title to locate the real window
    unique_title = '_unique123_'
    win32console.SetConsoleTitle( unique_title ) # resets when the script ends
    
    while 1:
        time.sleep( 0.1 ) # wait for the title to change
        hwnds = get_handle( unique_title, 'CASCADIA_HOSTING_WINDOW_CLASS' )
        if hwnds:
            hwnd = hwnds[0]
            break
    #print( hex(hwnd) )

    # change title
    if title:
        win32gui.SetWindowText( hwnd, title )
        win32console.SetConsoleTitle( title ) # change the tab title

    # change icon
    icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
    hicon = win32gui.LoadImage( None, img, win32con.IMAGE_ICON, 0, 0, icon_flags )
    win32gui.SendMessage( hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon )
    win32gui.SendMessage( hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon )




