"""Checks the schemas against the samples: every file under samples/valid
must be valid, and every file under samples/invalid must not be. Prints a
line per file, and the first errors of each that comes out wrong; exits 1
if any does."""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = {
    "path_coverage.json": "path_coverage.schema.json",
    "path_coverage.source.json": "path_coverage.source.schema.json",
}


def validator(name):
    """The validator of the schema for a file named name."""
    schema = json.loads((ROOT / SCHEMAS[name]).read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def main():
    """Checks each sample; returns the exit status."""
    wrong = 0
    for expected in ("valid", "invalid"):
        for path in sorted((ROOT / "samples" / expected).glob("*/*.json")):
            errors = list(validator(path.name).iter_errors(json.loads(path.read_text())))
            right = not errors if expected == "valid" else bool(errors)
            wrong += not right
            print(f"{'ok ' if right else 'WRONG'} {expected} {path.relative_to(ROOT)}")
            if expected == "valid":
                for error in errors[:3]:
                    print(f"    {'/'.join(map(str, error.absolute_path))}: {error.message[:150]}")
    print(f"{wrong} sample(s) wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
