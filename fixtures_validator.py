import dataclasses
from pathlib import Path
from pprint import pprint

import yaml

@dataclasses.dataclass(frozen=True)
class UniqueFixture:
    model: str
    pk: int

def iter_fixtures_files():
    for file in Path("fixtures").glob("*.yaml"):
        yield file

def iter_fixtures_entries() -> list[dict]:
    for file in iter_fixtures_files():
        with file.open() as f:
            yield from yaml.safe_load(f)


def main():
    fixtures = list(iter_fixtures_entries())
    unique_models = [UniqueFixture(model=entry["model"], pk=entry["pk"]) for entry in fixtures]
    duplicates = [fixture for fixture in unique_models if unique_models.count(fixture) > 1]
    assert not duplicates, f"There are duplicated fixtures: {duplicates}"



if __name__ == '__main__':
    main()