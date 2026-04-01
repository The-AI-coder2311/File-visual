import os

def get_size(path):
    try:
        return os.path.getsize(path)
    except:
        return 0
