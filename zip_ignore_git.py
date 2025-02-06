import os
import sys
import zipfile
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


def zip_directory(base_directory: str, output_zip: str, spec):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_directory):
            rel_root = os.path.relpath(root, base_directory)

            if rel_root == ".":
                rel_root = ""

            # Filtrar diretórios antes de entrar neles
            dirs[:] = [d for d in dirs if not spec or not spec.match_file(
                os.path.join(rel_root, d))]

            for file in files:
                rel_path = os.path.join(rel_root, file)
                if spec and spec.match_file(rel_path):
                    continue
                if rel_path == output_zip:  # Evitar zipar o próprio zip
                    continue
                full_path = os.path.join(base_directory, rel_path)
                zipf.write(full_path, arcname=rel_path)


def main():
    if len(sys.argv) > 1:
        directory = os.path.abspath(sys.argv[1])
    else:
        directory = os.getcwd()

    output_zip = os.path.basename(directory) + ".zip"
    spec = load_gitignore(directory)

    zip_directory(directory, output_zip, spec)
    print(f"Projeto compactado em {output_zip}")


if __name__ == "__main__":
    main()
