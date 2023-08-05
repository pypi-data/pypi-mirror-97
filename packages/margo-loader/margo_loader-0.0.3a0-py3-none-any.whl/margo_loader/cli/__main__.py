import argparse
from .commands import extract, makefile


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    extract.register(subparsers)
    makefile.register(subparsers)

    args = parser.parse_args()
    if args.subcommand == "extract":
        extract.main(args)
    if args.subcommand == "makefile":
        makefile.main(args)


if __name__ == "__main__":
    main()
