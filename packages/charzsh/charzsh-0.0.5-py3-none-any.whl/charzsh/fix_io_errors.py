import sys

from charzsh.utils import fix_io_errors


def main():
    if len(sys.argv) < 2:
        print("Usage: chzsh-fix-io-errors SOURCE_DIR")
        exit(1)
    source_dir = sys.argv[1]
    fix_io_errors(source_dir)


if __name__ == "__main__":
    main()
    exit(0)
