import argparse
from vfm.core import run_app

def main():
    parser = argparse.ArgumentParser(description="Visual File Manager")

    parser.add_argument("-y", "--yes", action="store_true", help="Auto confirm prompts")
    parser.add_argument("-h", "--help", action="help", help="Show help message")

    args = parser.parse_args()

    run_app(args)

if __name__ == "__main__":
    main()
