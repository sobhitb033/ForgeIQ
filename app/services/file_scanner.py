from pathlib import Path


class FileScanner:

    @staticmethod
    def find_python_files(project_folder: Path):

        python_files = []

        for file in project_folder.rglob("*.py"):

            # Ignore macOS metadata folders
            if "__MACOSX" in file.parts:
                continue

            # Ignore AppleDouble files
            if file.name.startswith("._"):
                continue

            python_files.append(file)

        return python_files