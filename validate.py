"""Validates path coverage runs' JSON files against the schemas beside this
file.

Usage: validate.py [DIR...]

Given DIRs, checks the path_coverage.json and path_coverage.source.json in
each against their schemas, and exits 1 if any is invalid. Given none,
checks the schemas against the samples: every file under samples/valid
must be valid, every file under samples/invalid must not be. Prints a line
per file, and the first errors of each that comes out wrong."""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMAS = {
    "path_coverage.json": "path_coverage.schema.json",
    "path_coverage.source.json": "path_coverage.source.schema.json",
}


def errors_of(path):
    """The schema errors of the JSON file at path, none when it is valid."""
    schema = json.loads((ROOT / SCHEMAS[path.name]).read_text())
    Draft202012Validator.check_schema(schema)
    return list(Draft202012Validator(schema).iter_errors(json.loads(path.read_text())))


def checked(path, valid, label):
    """1 when the file at path comes out other than valid says, else 0,
    printing a line for it, labelled label, and, when it should be valid
    but is not, its first errors."""
    errors = errors_of(path)
    right = not errors if valid else bool(errors)
    print(f"{'ok   ' if right else 'WRONG'} {label} {path}")
    if valid:
        for error in errors[:3]:
            print(f"    {'/'.join(map(str, error.absolute_path))}: {error.message[:150]}")
    return 0 if right else 1


def main(dirs):
    """Checks dirs' files, or the samples when none are given; returns
    the exit status."""
    if dirs:
        wrong = sum(checked(Path(d) / name, True, "valid") for d in dirs for name in SCHEMAS)
    else:
        wrong = sum(
            checked(path, kind == "valid", kind)
            for kind in ("valid", "invalid")
            for path in sorted((ROOT / "samples" / kind).glob("*/*.json"))
        )
    print(f"{wrong} file(s) wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
