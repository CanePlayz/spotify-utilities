import sys

sys.dont_write_bytecode = True

from cli.cli import CLI


def main():
    instance = CLI()
    instance.get_credentials()


if __name__ == "__main__":
    main()
