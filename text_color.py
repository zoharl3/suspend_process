
from colorama import * 

init( strip=False )

def warn( *a ):
    s = ' '.join(a)
    global last_printed_string
    last_printed_string = s
    print( 'WARNING:', Fore.YELLOW + s + Style.RESET_ALL)

def error( *a ):
    s = ' '.join(a)
    global last_printed_string
    last_printed_string = s
    print( 'ERROR:', Fore.RED + s + Style.RESET_ALL )

def emphasize( *a ):
    s = ' '.join(a)
    global last_printed_string
    last_printed_string = s
    print( Fore.GREEN + s + Style.RESET_ALL )

def emphasize2( *a ):
    s = ' '.join(a)
    global last_printed_string
    last_printed_string = s
    print( Fore.CYAN + s + Style.RESET_ALL )

def emphasize3( *a ):
    s = ' '.join(a)
    global last_printed_string
    last_printed_string = s
    print( Fore.MAGENTA + s + Style.RESET_ALL )

def soft( *a ):
    s = ' '.join(a)
    global last_printed_string
    last_printed_string = s
    print( Fore.YELLOW + Style.DIM + s + Style.RESET_ALL )
    
def print_line():
    global last_printed_string
    if last_printed_string:
        print( '-' * ( len( last_printed_string ) - 1 ) )

