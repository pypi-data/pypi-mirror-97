from argparse import ArgumentParser
from pathlib import Path

import pypk


def main():
    parser = ArgumentParser()
    parser.add_argument("package", help="Path to root package directory")
    parser.add_argument("author", help="Author's name")
    parser.add_argument("email", help="Author's email")
    parser.add_argument("--version", dest="version", default="3.6.0", help="Minimum Python version supported")

    args = parser.parse_args()
    pypk.create(Path(args.package), args.author, args.email, args.version)


if __name__ == "__main__":
    main()
