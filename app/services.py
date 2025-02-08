from json import dumps
from pathlib import Path
from typing import Any


class ArchiveJson:
    filepath: Path

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def update(self, data: dict[str, Any]) -> None:
        self.filepath.write_text(dumps(data, indent=4))
