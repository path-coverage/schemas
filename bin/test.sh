#!/usr/bin/env bash
# Builds the validator image and checks the schemas against the samples in it.
set -Eeu

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly IMAGE=ghcr.io/path-coverage/schemas

if [ "${1:-}" = '-h' ]; then
  cat <<EOF
Usage: bin/test.sh

Builds the validator image, then, in it, checks every sample under
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

docker build --quiet --tag "${IMAGE}" "${ROOT}" > /dev/null
docker run --rm "${IMAGE}"
