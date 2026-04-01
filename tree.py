import os

def print_tree(path, prefix=""):
    try:
        items = os.listdir(path)
    except PermissionError:
        print(prefix + "[Permission Denied]")
        return

    for item in items:
        full = os.path.join(path, item)

        if os.path.isdir(full):
            print(prefix + "[D] " + item)
            print_tree(full, prefix + "  ")
        else:
            print(prefix + "[F] " + item)
