import os
import sys

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern


def load_gitignore(directory: str):
    gitignore_path = os.path.join(directory, '.gitignore')
    if not os.path.isfile(gitignore_path):
        return None

    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    spec = PathSpec.from_lines(GitWildMatchPattern, lines)
    return spec


def print_tree(base_directory: str, current_directory: str, spec, prefix: str = ""):
    try:
        entries = os.listdir(current_directory)
    except PermissionError:
        return

    entries = sorted(entries)

    filtered_entries = []
    for e in entries:
        path = os.path.join(current_directory, e)
        rel_path = os.path.relpath(path, base_directory)

        if e.startswith('.'):
            continue

        if spec and spec.match_file(rel_path):
            continue

        filtered_entries.append(e)

    for i, entry in enumerate(filtered_entries):
        path = os.path.join(current_directory, entry)
        is_last = (i == len(filtered_entries) - 1)

        connector = "└── " if is_last else "├── "

        if os.path.isdir(path):

            print(prefix + connector + entry + "/")

            new_prefix = prefix + ("    " if is_last else "│   ")

            print_tree(base_directory, path, spec, new_prefix)
        else:
            print(prefix + connector + entry)


def main():
    if len(sys.argv) > 1:
        directory = os.path.abspath(sys.argv[1])
    else:
        directory = os.getcwd()

    spec = load_gitignore(directory)

    print(os.path.basename(directory) + "/")

    print_tree(directory, directory, spec, prefix="")


if __name__ == "__main__":
    main()
