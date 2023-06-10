import os, sys, subprocess

def rootDir():
    if sys.platform == 'darwin' and getattr(sys, 'frozen', False):
        # Running a built MacOS app
        app_dir = os.path.dirname(sys.executable)
        return f'{app_dir}/DATA'
    else:
        # Everything else
        return 'DATA'

def showerror(title, body):
    if sys.platform == 'darwin':
        body = body.replace('\n', '\\n').replace('"', '\\"')
        title = title.replace('"', '\\"')
        command = f'display dialog "{body}" with title "{title}" buttons {{"OK"}} default button 1 with icon stop'
        subprocess.run(['osascript', '-e', command])
    else:
        from tkinter import messagebox
        messagebox.showerror(title, body)

