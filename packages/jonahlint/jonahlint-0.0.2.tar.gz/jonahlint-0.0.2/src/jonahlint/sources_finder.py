from itertools import chain
from pathlib import Path


class SourcesFinder:

    @classmethod
    def find_sources(cls, path: Path):
        if cls.is_python_source(path):
            return [path]
        if not path.is_dir():
            return []
        return list(
            chain.from_iterable(
                [cls.find_sources(inner_path) for inner_path in path.iterdir()]
            )
        )

    @classmethod
    def is_python_source(cls, path: Path):
        return path.is_file() and path.suffix == ".py"
