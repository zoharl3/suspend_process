# suspend_process
A convenient (Python) script to suspend a game on Windows.

## Motivation
I finished playing, and I'd like to continue later. Usually, if you minimize a game (e.g., show desktop), it still runs in the background, taking resources. When closing another task, it usually pops up unexpectedly.

You could manually suspend the process, but the main window will stay in the taskbar and sometimes cause trouble.

If there's a convenient save, you could simply exit. But running the game each time is usually a hassle.

Instead, via a shortcut to a script, a game can be paused and resumed, hiding and showing its main window.

## Installation
- It requires [pssuspend.exe](https://learn.microsoft.com/en-us/sysinternals/downloads/pssuspend) in the script directory.
- `pip install` imported packages.

## Usage
- `suspend_process.py <task_name> [-t <window_title>]`  
The script that suspends a task.
- `suspend_process_create_shortcut.py` is a convenient GUI that asks to choose the main window of a running process, and it creates a desktop shortcut to `suspend_process.py` using the window information.

