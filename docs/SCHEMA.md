# Input and Output Schema

This document defines the supported input structures and the converter's row, column, flattening, and array behavior.

## Supported inputs

### Top-level array of objects

```json
[
  {"id": 1, "user": {"name": "Ada"}},
  {"id": 2, "user": {"name": "Lin"}}
]
```

Each array item is one input record and normally becomes one CSV row. Parsing is incremental with `ijson.items(..., "item")`.

### Object containing an array

```json
{"data": {"results": [{"id": 1}, {"id": 2}]}}
```

By default, the converter selects the shallowest array containing objects, then the largest array at that level. It prints the selected path and candidate counts when there is more than one candidate. For the example, it selects `data.results`. Use `--input-path data.results` or config key `input_path` to select an array explicitly. The path is a dot-separated sequence of object keys and points to the array itself. Each item in the selected array becomes one input record. If the object contains no array of objects, it is treated as one record.

### NDJSON

```text
{"id":1,"name":"Ada"}
{"id":2,"name":"Lin"}
```

Files with `.ndjson` or `.jsonl` extensions are read one line at a time; blank lines are skipped. Each nonblank line must contain one complete JSON value, normally an object. `input_path` is not used for NDJSON.

## Flattening strategies

Input record:

```json
{"id":7,"user":{"name":"Ada","address":{"city":"London"}},"meta":{"source":"api"}}
```

`none` emits columns `id`, `meta`, `user`; object values are compact JSON strings. Example cell: `{"name":"Ada","address":{"city":"London"}}`.

`depth:2` (default) expands object keys to two levels. It emits `id`, `meta.source`, `user.address`, and `user.name`; the `user.address` cell is `{"city":"London"}`.

`full` emits `id`, `meta.source`, `user.address.city`, and `user.name`.

`paths` selection uses an explicit ordered list, provided with `--columns id,user.address.city` or config `"columns": ["id", "user.address.city"]`. Only selected values are output. Missing paths become empty cells; nested values are serialized as compact JSON strings.

Per-path `flatten` overrides use `overrides` entries with a glob-like `path` and a `flatten` value, for example `{"path":"user.address","flatten":"full"}`.

## Array strategies

Input record:

```json
{"id":7,"tags":["prod","edge"],"owner":{"name":"Ada"}}
```

`json` (default) emits one row; `tags` is the compact JSON text `["prod","edge"]`.

`columns` emits `tags_0=prod` and `tags_1=edge`. For nested object elements, fields use suffix and dot paths such as `tags_0.name`. If the array has more than `array_cap` elements (default 10), the full array is serialized in the unsuffixed `tags` cell.

`join` emits `tags=prod; edge` by default. `array_delimiter` changes the separator. Object/array members are represented as compact JSON text before joining.

`explode` emits one row per array item, repeating other scalar fields. An array of objects is flattened using the selected flattening depth. Independent exploded arrays can multiply rows; conversion stops with an error unless Cartesian expansion is explicitly enabled with `--allow-cartesian` or config `allow_cartesian`.

An array strategy can be overridden at a path. Override paths use `*` to match any object key or array item path. Later matching overrides take precedence.

## Column names and ordering

- Nested object keys are joined with `.`.
- Array columns use a zero-based underscore suffix: `items_0`, `items_1`.
- Column names are discovered over the first pass and sorted alphabetically by default.
- `column_order: "first_seen"` uses order first encountered during discovery.
- Explicit columns preserve their given order and exclude every other field.
- Missing values are empty fields; nested objects/arrays in a cell use compact JSON.

## CSV encoding and dialect

Output is UTF-8 by default, comma-delimited, with CRLF record separators. Quoting is minimal by default and can be set to `all`. Embedded newlines remain inside correctly quoted cells. The configured `encoding` controls CSV output and NDJSON text decoding; regular JSON documents are streamed as bytes to `ijson`.
