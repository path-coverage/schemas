#!/usr/bin/env bash
# Checks the schemas against the samples, in Docker.
set -Eeu

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly IMAGE=python:3.13-slim

if [ "${1:-}" = '-h' ]; then
  cat <<EOF
Usage: bin/test.sh

In Docker, with jsonschema installed, checks every sample under
samples/valid is valid against its schema, and every sample under
samples/invalid is not. Prints a line per sample, and the first errors
of each that comes out wrong; exits non-zero if any does.

Options:
  -h    Show this help

Example:
  bin/test.sh
EOF
  exit 0
fi

docker run --rm \
  --volume "${ROOT}:/schemas:ro" \
  "${IMAGE}" \
  sh -c 'pip install --quiet --root-user-action=ignore jsonschema==4.26.0 && python /schemas/test/validate.py'
