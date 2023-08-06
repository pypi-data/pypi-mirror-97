import sys

# Add module parent directory to path if needed
if __package__ is None and not hasattr(sys, "frozen"):
    import pathlib

    path = pathlib.Path(__file__).absolute()
    sys.path.insert(0, str(path.parent.parent))


import lokrez

if __name__ == '__main__':
    lokrez.main()
