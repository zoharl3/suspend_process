
# currently case-sensitive

import psutil, time, colorama, sys, os
import get_process
import win32gui, win32con, win32api
import threading
import argparse

# script path
g_dir = os.path.dirname( os.path.realpath( __file__ ) ) + '\\'

def show_window( hwnd, op ):
    win32gui.ShowWindow( hwnd, op )
    #print( 'Last err:', win32api.GetLastError() )
    if op > 0:
        win32gui.SetForegroundWindow( hwnd )
    
def toggle_window( bHide, pid, title ):
    #return
    
    if not title:
        return
    
    hwnds = get_process.get_hwnds_for_pid( pid )
    if len(hwnds) == 0:
        return
    
    ts = []
    for i, hwnd in enumerate(hwnds):
        # first only
        if 0 and i != 0:
            break
            
        # top; doesn't filter anything
        if 1 and win32gui.GetWindow( hwnd, win32con.GW_OWNER ) != 0:
            continue
        
        # title
        title2 = win32gui.GetWindowText( hwnd )
        print( f'HWND={hex( hwnd )}, title="{title2}"' )
        if 1 and title and not title in title2:
            continue
            
        op = 0 if bHide else 1
        
        print( f'    Found: HWND={hwnd}, title="{title2}", sending ShowWindow({op})' )
        
        if 0:
            win32gui.ShowWindow( hwnd, op )
        else:
            t = threading.Thread( target=show_window, args=[hwnd, op] )
            t.start()
            ts.append( t )
        
    for t in ts:
        t.join()
    
def toggle_suspend( pname, title, delay ):
    # get latest process
    bSuspend = 0
    proc = []
    field = -1
    for proc2 in psutil.process_iter( attrs=['pid', 'name'] ):
        #print(proc2.info)
        if proc2.name() == pname:
            #field2 = proc2.create_time()
            mem = proc2.memory_info() #'wset'
            field2 = mem.rss
            
            #if field == -1 or field2 < field:
            if field2 > field:
                proc = proc2
                field = field2

    if not proc:
        msg = "There's no process '%s'" % pname
        print( msg )
        win32api.MessageBox( 0, msg, 'suspend_process.py', 48 )
        #input()
        return bSuspend, proc
        
    bSuspend = not proc.status() == psutil.STATUS_STOPPED
    
    print( f"    '{pname}' was found (pid={proc.pid}), bSuspend={bSuspend}" )
        
    if not bSuspend: # resume
        if delay > 0:
            print( f"Waiting for {delay}min:" )
            for i in range( delay ):
                print( "%d " % (delay - i), end = '', flush=True )
                time.sleep( 60 )
            print('')
        
        
        
        if 1:
            # resume doesn't always work; using an external util
            cmd = g_dir + '\pssuspend.exe -nobanner -r %d' % proc.pid
            os.system( cmd )
        else:
            proc.resume()
            
        print( colorama.Fore.GREEN + colorama.Style.BRIGHT + "resumed" + colorama.Style.RESET_ALL )

        if proc.status() != psutil.STATUS_RUNNING:
            print( f"'{pname}'", colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"The process hasn't resumed; status={proc.status()}" + colorama.Style.RESET_ALL )
            input()
        
        print()
        toggle_window( bSuspend, proc.pid, title )
        print()
        
        # check activity
        while 0:
            cp = proc.cpu_percent( interval=1 ) # delay
            if cp < 5:
                print( "cpu_percent=%f" % cp )
                time.sleep( 1 )
            else:
                break
                
    else: # suspend
        print()
        toggle_window( bSuspend, proc.pid, title )
        print()
        
        proc.suspend()
        print( colorama.Fore.RED + colorama.Style.BRIGHT + "suspended" + colorama.Style.RESET_ALL )
        time.sleep( 1 )
        
        while 0 and proc.status() != psutil.STATUS_STOPPED:
            print( f"'{pname}'", colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"The process hasn't stopped; status={proc.status()}" + colorama.Style.RESET_ALL )
            time.sleep( 1 )
            
    return bSuspend, proc
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'pname', nargs='+' )
    parser.add_argument( '--title', '-t', nargs='+' )
    parser.add_argument( '--delay', '-d', type=int, default=0 )
    p = parser.parse_args()
    
    pname = ' '.join( p.pname ) + '.exe'
    title = ''
    if p.title:
        title = ' '.join( p.title )
    print( f'pname="{pname}", title="{title}", delay={p.delay}', flush=True )
    bSuspend, proc = toggle_suspend( pname, title, p.delay )
    
if __name__ == "__main__":
    main()
    