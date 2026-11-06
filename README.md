# <img src="https://avatars.githubusercontent.com/u/353243247?v=4" alt="" width="32" height="32"> path-coverage/schemas

The JSON Schemas (draft 2020-12) of the two files every language's path
coverage tool writes at the end of a run, and nothing else:

- [`path_coverage.schema.json`](path_coverage.schema.json): the counts,
  for AIs and other tools. Every decision, the paths each took, the
  totals, and each method's card.
- [`path_coverage.source.schema.json`](path_coverage.source.schema.json):
  what drawing each file's code needs and only a parser of its language
  can work out: each line's text and coloured tokens, where each
  decision is, and its fold's rows.

They are the contract between the tools that write the files,
[ruby](https://github.com/path-coverage/ruby) and
[python](https://github.com/path-coverage/python), and what reads
them, eg [html-reporter](https://github.com/path-coverage/html-reporter).
Each file names its schema's URL under `$schema`; both are served at
https://path-coverage.github.io/schemas/.

## Validating a run

The image validates the two files in a directory, exiting non-zero if
either is invalid:

```sh
docker run --rm -v "$PWD/coverage:/paths:ro" ghcr.io/path-coverage/schemas /paths
```

## Testing

`bin/test.sh` builds the image and, in it, checks every sample under
`samples/valid`, a demo run of each tool, is valid, and every sample
under `samples/invalid` is not. A push to main tests, then publishes the
image, tagged `latest` and with the commit.
