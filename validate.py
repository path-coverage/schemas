"""Validates path coverage runs' JSON files against the schemas beside this
file, one version of them in each v<N> directory.

Usage: validate.py [DIR...]

Given DIRs, checks the path_coverage.json and path_coverage.source.json in
each against the schema its "$schema" names, and exits 1 if any is invalid
or names no schema here. Given none, checks each version's schemas against
its own samples: every file under v<N>/samples/valid must be valid, every
file under v<N>/samples/invalid must not be. Prints a line per file, and
the first errors of each that comes out wrong."""

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMAS = {
    "path_coverage.json": "path_coverage.schema.json",
    "path_coverage.source.json": "path_coverage.source.schema.json",
}


def versions():
    """The directories of ROOT holding a version of the schemas, eg v1,
    oldest first."""
    found = [d for d in ROOT.iterdir() if d.is_dir() and re.fullmatch(r"v[0-9]+", d.name)]
    return sorted(found, key=lambda d: int(d.name[1:]))


def schemas_by_id():
    """{ a schema's $id => its file } for every schema of every version."""
    files = [version / schema for version in versions() for schema in SCHEMAS.values()]
    return {json.loads(file.read_text())["$id"]: file for file in files}


def errors_of(path, schema_file):
    """The errors of the JSON file at path against the schema in
    schema_file, none when it is valid."""
    schema = json.loads(schema_file.read_text())
    Draft202012Validator.check_schema(schema)
    return list(Draft202012Validator(schema).iter_errors(json.loads(path.read_text())))


def report(path, valid, label, errors):
    """1 when errors make the file at path come out other than valid says,
    else 0, printing a line for it, labelled label, and, when it should be
    valid but is not, its first errors."""
    right = not errors if valid else bool(errors)
    print(f"{'ok   ' if right else 'WRONG'} {label} {path}")
    if valid:
        for error in errors[:3]:
            print(f"    {'/'.join(map(str, error.absolute_path))}: {error.message[:150]}")
    return 0 if right else 1


def named_errors(path, known):
    """The errors of the report at path against the schema its "$schema"
    names, among known, { $id => file }; a single error naming the problem
    when it names none of them."""
    named = json.loads(path.read_text()).get("$schema")
    if named not in known:
        return [UnknownSchema(named)]
    return errors_of(path, known[named])


class UnknownSchema:
    """The error of a report whose "$schema" names no schema here, shaped
    as report prints a jsonschema error."""

    def __init__(self, named):
        """The error of a report naming named, a URL or None."""
        self.absolute_path = ["$schema"]
        self.message = f"names no schema here: {named!r}"


def check_dirs(dirs):
    """How many of the reports in dirs come out invalid, each checked
    against the schema it names."""
    known = schemas_by_id()
    return sum(
        report(path, True, "valid", named_errors(path, known))
        for path in (Path(d) / name for d in dirs for name in SCHEMAS)
    )


def check_samples():
    """How many samples come out other than their directory says, each
    checked against its own version's schema."""
    return sum(
        report(path, kind == "valid", kind, errors_of(path, version / SCHEMAS[path.name]))
        for version in versions()
        for kind in ("valid", "invalid")
        for path in sorted((version / "samples" / kind).glob("*/*.json"))
    )


def main(dirs):
    """Checks dirs' files, or the samples when none are given; returns
    the exit status."""
    wrong = check_dirs(dirs) if dirs else check_samples()
    print(f"{wrong} file(s) wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
