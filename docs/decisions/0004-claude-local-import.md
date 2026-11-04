# ADR 0004 — Project-route Claude import in `CLAUDE.local.md`

Date: 2026-11-04. Status: implemented in the development candidate; installed-client
loading still to be observed in the first live connection.

## Problem

The project route appended its owned import block to the root `CLAUDE.md`. That file
is usually tracked: committing the block would publish an import of a file that
exists only on one machine, and a managed host that installs its own index refuses
a base that already carries a competing registration. The owner wants the tracked
`CLAUDE.md` to stay a plain `@AGENTS.md` everywhere.

## Decision

- Project route: the owned block lives in root `CLAUDE.local.md`, the personal
  instructions file that Claude Code loads together with `CLAUDE.md` (string present
  in the installed 2.1.318 client; loading is observed at connection, not claimed).
  Projects ignore that file. The tracked `CLAUDE.md` is never written.
- A guidance block or entry import left in the tracked `CLAUDE.md` is rejected in
  the project route, so the index cannot load twice; removing it is explicit.
- Managed route: unchanged (`AGENTS.md` block and the existing `CLAUDE.md` import).
- No compatibility path for earlier project-route connections that wrote `CLAUDE.md`:
  remove them with the previous engine before reconnecting.

## Verification

Unit tests cover install, update, remove, restore, recovery and fault injection on
the new surface, plus two cases: the tracked `CLAUDE.md` stays byte-identical, and a
stale block in it is rejected without writing anything.
