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

## path_coverage.json

A decision is named by the `path:line:column` its language's tool names
it at, the path relative to the run's root. The keys:

- `decisions`: each decision's operands, in order, each with how often
  it was truthy and falsy; `only` names the one outcome a fixed leaf,
  eg a literal, can have.
- `paths`: each decision's leaves, as `line:column` spans, and each
  possible path with how often it was taken. A path is the outcome of
  each leaf, in order, `null` for a leaf short-circuiting skipped:

```json
"paths": {
  "source/kata.rb:3:23": {
    "leaves": [["3:23", "3:30"], ["3:34", "3:42"]],
    "taken": [
      { "path": [true, true], "count": 2 },
      { "path": [true, false], "count": 0 },
      { "path": [false, null], "count": 1 }
    ]
  }
}
```

- `cards`: each method's card, under its def's name, and each top card,
  for code outside every method, under its first line. A card has a
  row for each decision, and each `return` or `raise`, which ends a
  path; its `ways`, the ways one call can go through it; and its
  `calls`, `null` for a top card:

```json
"cards": {
  "label.rb:1:0": {
    "name": "label", "first": 1, "last": 7, "ways": 2, "calls": 1,
    "rows": [
      { "at": "2:02", "top": "if", "paths": 2, "taken": 1, "decision": "label.rb:2:2" },
      { "at": "3:04", "top": "return", "paths": 1, "taken": 1, "decision": null },
      { "at": "5:04", "top": "return", "paths": 1, "taken": 0, "decision": null }
    ]
  }
}
```

- `tree`: how each card's rows nest, by file, then card, then row. A row
  inside a decision names it as its `parent`, the arm it is `in`, and
  `on`, the indices of the parent's paths that run it, in the order
  `paths` lists them. A row inside one of its parent's leaves names that
  `leaf`, by index; a row that is the whole of that leaf also `gives`
  the leaf's outcome on each of its own paths, `null` where not known:

```json
"tree": {
  "label.rb": {
    "1:0": {
      "2:2": { "parent": null, "in": null, "on": null, "leaf": null, "gives": null },
      "3:4": { "parent": "2:2", "in": "then", "on": [0], "leaf": null, "gives": null },
      "5:4": { "parent": "2:2", "in": "else", "on": [1], "leaf": null, "gives": null }
    }
  }
}
```

- `reached`: how often each statement that is no decision, and each
  method's entry, was reached; absent when not known.
- `totals`: the paths taken of all possible, as [taken, possible]:
  `alone`, `combined`, and, with groups, each group's own under
  `groups`, eg `"groups": {"code": {"alone": [481, 567]}}`.
- `kinds`: the kinds of decision measured. Runs merge only when these,
  `ignored`, `treats` and `measured_by` match, as otherwise their
  decisions list their paths differently.
- `measured_by`: each tool that parsed or measured the run, by name,
  and its version, eg `{"ruby": "4.0.5", "prism": "1.8.1",
  "path_coverage": "0.4.0"}`. A different language, parser or tool
  version can find a file's decisions or paths differently.
- `ignored`, `treats`, `outside`: any operators not measured, any
  treatments, and any paths taken that a treatment rules out.

## path_coverage.source.json

What drawing each file's code needs and only a parser of its language
can work out, so html-reporter never parses code:

- `files`: each covered file's `lines`, each its `text` and coloured
  `tokens`, and its `decisions`, each its `span` of lines and its
  `fold`: the decision's own row, then a row per part, each with a cell
  per possible path, in the order `paths` lists them.
- `labels`: each card row's `top`, coloured.
- `groups`: each group's covered files.

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
