import csv
from pathlib import Path
from typing import Generator

csv_file_path: Path = Path(__file__).parent / "csv_files"


def load_csv_file_as_generator(file_name: str, skip_column_definition: bool = True) -> Generator[tuple[str, ...], None, None]:
    with open(csv_file_path / file_name, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        if skip_column_definition:
            next(csv_reader)
        for entry in csv_reader:
            yield tuple(entry)


def load_csv_file(file_name: str, skip_column_definition: bool = True) -> list[tuple[str, ...]]:
    with open(csv_file_path / file_name, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        if skip_column_definition:
            next(csv_reader)
        return [tuple(line) for line in csv_reader]
