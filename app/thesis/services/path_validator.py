from pathlib import Path
from typing import List


class PathValidator:
    def clean_path_string(self, path_str: str) -> str:
        return path_str.strip()
    
    def is_valid_directory (self, path_str: str) -> bool:
        path_obj = Path(path_str)
        return path_obj.exists() and path_obj.is_dir()
    
    def get_valid_directories(self, raw_folders: list[str]) -> list[Path]:
        valid_paths = []

        for raw_str in raw_folders:
            cleaned_str = self.clean_path_string(raw_str)

            if self.is_valid_directory(cleaned_str):
                valid_paths.append(cleaned_str)
            else:
                print(f"Путь не существует или не является папкой'{cleaned_str}'")
        return valid_paths

    def get_pdf_files_from_dirs(self, valid_dirs: list[Path]) -> list[Path]:
        pdf_files = []
        for directory in valid_dirs:
            pdf_files.extend(directory.glob("*.pdf"))   
        return pdf_files
