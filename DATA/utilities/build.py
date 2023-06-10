import os, sys

def rootDir():
    if os.name == 'posix' and getattr(sys, 'frozen', False):
        # Running a built MacOS app
        app_dir = os.path.dirname(sys.executable)
        return f'{app_dir}/DATA'
    else:
        # Everything else
        return 'DATA'
