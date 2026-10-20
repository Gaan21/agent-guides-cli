# Project-local lifecycle (development)

Development tooling with [bounded T04 acceptance](tasks/T04-acceptance.md), **not a
stable release or production activation**. Neutral lifecycle and disposable native
root-started cases are accepted; consumer/guard/migration acceptance remains separate.

## Prerequisites and ownership

Use an inspected development wheel, Python 3.11+, Git, a writable project/worktree
root and explicitly approved sources/clients. Source-build acquisition is in the
root README; [preparation](preparation.md) defines bundle/request inputs. Reuse
one tools environment across content updates. Credentials/global settings are not
installed. Uncached HTTPS sources need authorized access.

Change connections between tasks, with selected clients quiescent; the tool cannot
detect active sessions. Restart affected clients once afterward. No hot-context
replacement is promised. Agent sessions must start at the selected root, with
matching `cwd`/`PWD`. Installation rejects obvious Git subdirectories; this is not
production-launcher binding evidence.

The candidate owns:

- `.guidance/entry.md`: selected authored short entries labeled by scope, with
  Markdown links relocated into immutable selections. Original source/topic bytes
  remain intact. No topic bodies or selector engine are injected.
- A marker-delimited native import in root `CLAUDE.md` for selected Claude Code.
  Outside bytes, CRLF/LF style and existing file permissions are preserved.
- A new `.opencode/opencode.json` for selected OpenCode, or direct `opencode.json`
  when the `.opencode` slot is occupied, with native `instructions` pointing to the
  short entry. Existing documents are never edited. The selected path is recorded.
- In managed mode, an owned scoped short-index block in root `AGENTS.md` instead of
  project configuration. Existing Claude imports of that file are reused, not doubled.
- One portable `guidance.lock.json`; ownership, journal and retained content/locks
  under `.guidance/`. A fixed `.guidance/.gitignore` ignores that local storage
  without changing root ignore rules; it stays when retained content stays.

If both native configuration slots are occupied, installation stops before source
resolution; it never parses/rewrites user JSONC. An edited owned config needs explicit
resolution; it is never silently replaced/deleted. Claude blocks are surgically
edited. Known legacy tokens are checked in selected clients' root instructions and
settings. This bounded inventory is not exhaustive indirect-import/plugin discovery.
Unselected client settings and unrelated guards/lints are not modified or executed.

**Managed OpenCode:** explicitly supply `--host-config HOST_JSON` on install and on
restore to a fresh root. It must be approved, external, read-only JSON containing
`instructions: ["{env:PWD}/AGENTS.md"]` (unrelated host settings are retained). The host
must already set `OPENCODE_DISABLE_PROJECT_CONFIG=1`, bind `OPENCODE_CONFIG` to that
file and run the operation with `cwd` and absolute `PWD` at the selected project/worktree root.
Missing/stale bindings fail before activation. The package never writes the host,
enables discovery or adds a launcher. Updates reuse the approved local registration;
offline verification/removal need not run in the launch directory. These checks do
not prove future production-launcher binding or installed-client loading. See the
[scoped ownership design](decisions/0002-native-config-ownership.md).

## Commands and exact selection

Examples require an approved request/root; they are not consumer activation approval:

```sh
agent-guides-cli install --project PROJECT --request request.json \
  --client claude --client opencode
agent-guides-cli status --project PROJECT --expected SELECTION_SHA256
agent-guides-cli verify --project PROJECT --expected SELECTION_SHA256
agent-guides-cli update --project PROJECT --expected SELECTION_SHA256
agent-guides-cli restore --project PROJECT --lock saved-guidance.lock.json \
  --expected SAVED_SELECTION_SHA256 --current CURRENT_SELECTION_SHA256
agent-guides-cli remove --project PROJECT --expected SELECTION_SHA256
agent-guides-cli recover --project PROJECT
```

Install/update/restore accept `--cache CACHE`, default `PROJECT/.guidance/cache`.
Connected restore is dispatched from the lock; prepared-only locks retain T02's
non-activating restore. A fresh root needs no `--current`. Restoring the currently
recorded selection may omit it; restoring a different one needs its expected current
digest. Applying an existing selection requires independently retained `--expected`.

Retain successful JSON's `selection` in host evidence before role work. Status and
verify are offline comparisons against that expectation, never repair/refresh.
`installed`, `removed` and `prepared` describe host state, not observed client
loading, model compliance or guard enforcement.

Install/update resolve each selected source once. Explicit exact `revision` policy
survives updates. Updates preserve source/bundle/scope/client choices and local
authority, without reinstalling the engine. Repeating install for the same installed
request/expected selection is a no-op, not an implicit update. Remove first to change
clients. Restore never resolves branches or uses the network: complete cached bundles
or exact Git objects are required. Missing identities fail without switching.

## Recovery and retention

Immutable selections and exact portable lock copies are retained before activation.
JSON's `record` names `.guidance/records/SELECTION_SHA256.json`; prior successful
locks remain there for explicit restore. Unactivated candidates may remain after
failure. Nothing is automatically collected. Retain reviewed engine wheels separately;
restore requires the recorded engine byte identity, not merely its version label.

The fsynced `.guidance/transaction.json` retains a transaction identity, old/new
selection identities, before/after bytes and modes before native writes. Each
preimage is rechecked; the portable lock is published last. Completed and rolled-back
journals remain under `.guidance/transactions/` before the active journal is cleared.
Retained transaction/lock copies are owner-readable only (`0400`); active journals
use `0600`. Unknown permission changes stop application/recovery or retention rather
than silently widening access or repairing user changes.
New-directory and file-replacement parent synchronization is requested. Individual
renames are **not multi-file atomicity**: do not start clients during an operation
or while a recovery journal exists.

The next mutation recovers first, or run `recover`. Uncommitted work rolls back only
when every path matches its before/after image. Unknown edits stop restoration and
preserve the journal. Committed work remains; its completed journal is cleared.
Recovery is idempotent. Abandoned `writer-lock` directories need operator inspection,
never automatic age-based deletion.

Remove deletes only verified owned integration, retaining locks, cached objects,
prior selections and unrelated user bytes. A newly created `CLAUDE.md` disappears
only when no unrelated bytes remain; a preexisting empty file remains. Cache cleanup
and legacy migration are separate. Task-pin/join additionally retain selected-client
project settings and ownership identity in the independent host record. Nested/host
imports and overlays still need explicit evidence; both roles share one record.

## Remaining acceptance and setup budget

With Python/Git and the inspected executable installed: one install command, at
most one restart per client; one operation per update/restore/remove. First use still
needs a tools environment and exact wheel installation, plus build tooling/builds
when starting from source. Request preparation and independent evidence are explicit
inputs, not hidden consumer scripts. This is a command inventory, not measured
production setup evidence.

Keep `.guidance/` out of source uploads; it can contain private content and recovery
bytes. Its local ignore file is created before acquisition and is checked offline;
an existing incompatible file is a conflict, not permission to overwrite it.

Implemented: managed owned registration and operation-root prerequisites, plus
byte-preserving coexistence with user JSONC through native configuration slots.
Recorded acceptance includes setup/operation inventory, macOS and Linux package
checks, installed macOS client confirmation and independent corrective/closure
reviews. See the acceptance matrix for skips and interruption/input caveats. Future
production-launcher binding is an operator prerequisite, not an implicit host edit;
Linux native-model/TUI and consumer migration/guard checks are not inferred passed.
