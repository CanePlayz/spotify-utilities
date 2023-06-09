import sys
from cli.cli import CLI

sys.dont_write_bytecode = True


def main():
    instance = CLI()
    instance.get_credentials()


if __name__ == "__main__":
    main()
