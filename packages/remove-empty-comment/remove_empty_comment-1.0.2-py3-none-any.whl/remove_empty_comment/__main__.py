"""Remove empty comment from code. Used by pre-commit."""

import argparse
import sys
from typing import List, Union


def main(argv: Union[List[str], None] = None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        metavar="FILES",
        help="File names to modify",
    )
    args = parser.parse_args(argv)
    offending_files = []
    for file_name in args.filenames:
        try:
            clean(file_name, offending_files)
        except UnicodeDecodeError:
            pass
    if offending_files:
        print(f"Removed empty comments from {', '.join(offending_files)}.")
        sys.exit(-1)
    sys.exit(0)


def clean(file_name, offending_files):
    with open(file_name, encoding="utf8") as f:
        content = f.readlines()
    new_content = transform(content)
    if len(new_content) != len(content):
        offending_files.append(file_name)
    with open(file_name, "w", encoding="utf8") as f:
        f.writelines(new_content)


def transform(content: List[str]) -> List[str]:
    new_content: List[str] = []
    for line in content:
        if not line.strip() or any(c != "#" for c in line.strip()):
            new_content.append(line)
    return new_content


if __name__ == "__main__":
    main()
