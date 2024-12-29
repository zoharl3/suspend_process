
import os, sys

if len(sys.argv) < 2:
    print( "Usage: ... | python", os.path.basename( sys.argv[0] ), "<log_file>" )
    sys.exit()
     
fname = sys.argv[1]

f = open( fname, 'w' )

while 1:
    ch = sys.stdin.read(1)
    if ch == '': # EOF
        break
    
    print( ch, end = '' )
    sys.stdout.flush()
    
    f.write( ch )
    f.flush()
    
    