import os

def run_keyboard():
    files = os.listdir(".")
    index = 0

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        for i, f in enumerate(files):
            if i == index:
                print("> " + f)
            else:
                print("  " + f)

        key = input()

        if key == "q":
            break
        elif key == "w":
            index = max(0, index - 1)
        elif key == "s":
            index = min(len(files) - 1, index + 1)
