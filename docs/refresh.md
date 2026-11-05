# Explicit pre-session refresh

Development command for owner-operated, project-route connections. Run from the
project root **before** opening Claude Code or OpenCode:

```sh
agent-guides-cli refresh
```

`refresh-guides`, installed with the package, is the same command for the Git root
containing the current directory, so it also works from a subdirectory. Expose it
on `PATH` explicitly if the tool lives in a private virtual environment.

This fetches the approved branch of each selected source into operator-owned
mirrors, runs the existing journaled update and advances the separately retained
expected selection. No hooks, launchers, daemon, credentials or global config are
installed. No tracked guidance integration file may be changed. It does not update
the executable itself, switch bundle selections or operate on managed connections.
Existing explicit `update` and exact offline restore workflows remain available;
tool compatibility follows the provenance rule below.

A compatible tool update does not invalidate an intact selection. Its recorded
engine identity describes how it was prepared, not which executable must remain
installed. The current schema, retained expectation, content and connection still
must verify. A new refresh records the current tool; a prior selection restored
offline retains its original provenance. Shared task-role identity is separate.

## Opt in on each machine

Connect the project with `install` first. Retain its printed selection outside the
project. Create an external JSON file explicitly, for example
`~/.local/share/agent-guides-cli/example.refresh.json`:

```json
{
  "schema": 1,
  "project": "/absolute/path/to/example",
  "selection_file": "/absolute/path/to/retained-selection",
  "mirrors": {
    "common": "/absolute/path/to/common.git",
    "product": "/absolute/path/to/product.git"
  }
}
```

The root must match exactly; another checkout requires its own approval/settings.
Use `--project PATH --settings FILE` to select a different root or settings file.
Default settings use the project directory's basename, but exact root binding
prevents accidental reuse by a same-named clone. All settings, mirrors and the
expectation must be outside the project, without symbolic links. Every selected
source needs exactly one distinct bare mirror whose origin is the approved URL.
Pinned selections are refused: use explicit `update` for that workflow.

The fetch uses existing operator Git authentication, noninteractively, without
source hooks, submodules or raw network error logs. Each fetch has a 30-second
timeout. All selected mirrors are locked through the update; simultaneous refresh
of another project sharing a mirror can return the intact-copy warning instead
of claiming it checked upstream. It never refreshes unselected sources.

## Read the result before starting work

- `freshness: checked`: selected branches were fetched and the connection updated
  and verified. Exact source commits and selection are reported. This is a point-
  in-time check, not a promise against later upstream changes.
- `freshness: not_checked`: refresh failed, but the previous installed copy still
  passes integrity verification. It may be out of date; tell the owner and report
  that limitation. A partial fetch never activates a mixed selection.
- Nonzero exit: no usable verified result. Inspect the error; do not describe the
  guides as valid or reconnect/recover silently.

Already-running conversations retain their previous context. Open a fresh session
after refreshing; do not use this command to replace a conversation's instructions.
Native loading and actual guide use remain separate checks from host verification.

## Interrupted expectation publication

Project update uses the existing journal. The separate external expectation is
atomically replaced **after** success, not in a cross-filesystem transaction.
A process cut or disk error in between may leave a newer project lock and the old
expectation. Next refresh refuses that mismatch; it never adopts generated data
as authority. Inspect the prior retained record, transaction state and update
result, then explicitly restore the old connection or approve and retain the new
expectation. Recovery is not an implicit side effect of an offline fallback.
