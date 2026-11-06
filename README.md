# <img src="https://avatars.githubusercontent.com/u/353243247?v=4" alt="" width="32" height="32"> path-coverage/schemas

The JSON Schemas (draft 2020-12) of the two files every path coverage
port writes at the end of a run, and nothing else:

- [`path_coverage.schema.json`](path_coverage.schema.json): the counts,
  for AIs and other tools. Every decision, the paths each took, the
  totals, and each method's card.
- [`path_coverage.source.schema.json`](path_coverage.source.schema.json):
  what drawing each file's code needs and only a parser of its language
  can work out: each line's text and coloured tokens, where each
  decision is, and its fold's rows.

They are the contract between the ports that write the files,
[ruby](https://github.com/path-coverage/ruby) and
[python](https://github.com/path-coverage/python), and what reads
them, eg [html-reporter](https://github.com/path-coverage/html-reporter).

## Testing

`bin/test.sh`, in Docker, checks every sample under `samples/valid`, a
demo run of each port, is valid, and every sample under
`samples/invalid` is not.
