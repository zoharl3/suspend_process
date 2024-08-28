
@echo off

rem https://stackoverflow.com/questions/9232308/how-do-i-minimize-the-command-prompt-from-my-bat-file
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

cd c:\prj\python\
python.exe suspend_process.py %* | python tee.py suspend_process.ans

rem pause

exit
