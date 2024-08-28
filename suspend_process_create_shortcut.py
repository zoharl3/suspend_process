
# create a shortcut for suspend_process

import re, subprocess, time, shutil, os, sys
from pathlib import Path
import psutil
import ctypes
from text_color import *
import functools
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt
from PySide6 import QtGui
import win32con, win32api, win32ui, win32gui, win32process
import winshell
 
# to resolve: "This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem."
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'c:\Python37\Lib\site-packages\PySide6\plugins\platforms' 

# script path
g_dir = os.path.dirname( os.path.realpath( __file__ ) ) + '\\'
g_wins = []

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        n = win32gui.GetWindowText( hwnd )
        if n:
            g_wins.append( hwnd )
            #print( n )

def create_shortcut( hwnd, name ):
    pid = win32process.GetWindowThreadProcessId( hwnd )
    pid = pid[-1]
    exe = psutil.Process( pid ).name()
    exe = Path( exe ).stem
    print( hwnd, pid, name, exe, sep='\n' )
    
    if len( name ) > 20:
        name = name[:20]
        
    link_filepath = os.path.join( winshell.desktop(), f"suspend {name}.lnk" )
    with winshell.shortcut( link_filepath ) as link:
        link.working_directory = g_dir
        link.path = g_dir + 'suspend_process.bat'
        link.arguments = f"{exe} -t {name}"
        link.description = name
        link.icon_location = ( g_dir + 'suspend.ico', 0 )
        
        #link.dump()
    print( 'created desktop shortcut' )

class Form( qtw.QDialog ):
    def __init__( self, parent=None ):
        super( Form, self ).__init__( parent )

        layout = qtw.QVBoxLayout()
        
        self.lst = qtw.QListWidget( self )
        layout.addWidget( self.lst )

        btn = qtw.QPushButton( 'Create a shortcut', self )
        btn.clicked.connect( self.on_btn_click )
        layout.addWidget( btn )

        # populate list
        for hwnd in g_wins:
            pid = win32process.GetWindowThreadProcessId( hwnd )
            exe = psutil.Process( pid[-1] ).exe()

            name = win32gui.GetWindowText( hwnd )
            name2 = f'{name} | {exe}'
            item = qtw.QListWidgetItem( name2 )
            
            # icon
            large, small = win32gui.ExtractIconEx( exe, 0 )
            if large:
                hdc = win32ui.CreateDCFromHandle( win32gui.GetDC( 0 ) )
                hbmp = win32ui.CreateBitmap()
                ico_x = win32api.GetSystemMetrics( win32con.SM_CXICON )
                ico_y = win32api.GetSystemMetrics( win32con.SM_CYICON )
                hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_y )
                hdc = hdc.CreateCompatibleDC()
                hdc.SelectObject( hbmp )
                hdc.DrawIcon( ( 0, 0 ), large[0] )
                bitmapbits = hbmp.GetBitmapBits( True )
                img = QtGui.QImage( bitmapbits, ico_x, ico_y, QtGui.QImage.Format_ARGB32_Premultiplied )
                
                pixmap = QtGui.QPixmap( img )
                icon = QtGui.QIcon( pixmap )
                item.setIcon( icon )
            else:
                continue
            
            item.setData( Qt.ItemDataRole.UserRole, [hwnd, name] )
            font = QtGui.QFont( 'Consolas', 12 )
            item.setFont( font )
            self.lst.addItem( item )
        self.lst.sortItems()
            
        self.setLayout( layout )
        self.setGeometry( 400, 100, 600, 600 )
        self.setWindowTitle( 'select window' )
        self.show()

    def on_btn_click( self ):
        print( f'on_btn_click()' )
        sel = self.lst.selectedItems()
        if not sel:
            return
        sel = sel[0]
        hwnd, name = sel.data( Qt.ItemDataRole.UserRole )
        create_shortcut( hwnd, name )
        self.close()

def main():
    win32gui.EnumWindows( winEnumHandler, None )
    
    app = qtw.QApplication()
    win = Form()
    win.show()
    app.exec()

#
main()

