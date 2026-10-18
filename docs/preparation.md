# Exact preparation (development)

This is the T02 non-activating slice, not a stable published release. It prepares
whole bundles and records directory bindings; it does not register native entries,
load client instructions, run source commands or activate a consumer. Install,
update, status and remove lifecycle commands are not implemented.

## Prerequisites and inputs

Use an inspected development wheel in a dedicated Python 3.11+ environment, Git,
an existing writable project and a dedicated writable cache. See the root README
for building and clean-install verification. Uncached sources require authorized
network access. Public and credential-free HTTPS Git locators are accepted (no
embedded user/password, query, fragment or custom port). Authentication failures
are reported, not repaired; no credential or global Git configuration is installed.
SSH/local-folder import is not implemented. Disposable tests inject `fixture://`
sources through the Python API; the public CLI does not accept that transport.

An explicit preparation request is an input, not a second persistent project
configuration. For example (placeholder repositories, not live source approval):

```json
{
  "schema": 1,
  "sources": [
    {"id": "common", "url": "https://example.org/owner/common.git", "ref": "refs/heads/develop"},
    {"id": "local-rules", "url": "https://example.org/owner/project-guidance.git"}
  ],
  "bundles": [
    {"source": "common", "path": "bundles/base", "binding": "."},
    {"source": "common", "path": "bundles/mobile", "binding": "mobile"},
    {"source": "local-rules", "path": ".", "binding": "."}
  ]
}
```

`ref` defaults to `refs/heads/develop`. Optional `revision` is an exact lowercase
40-character commit and takes precedence over the branch. Only explicit
`refs/heads/...` channels are accepted; tags/revision expressions are not selectors.
Resolve every source once on preparation, then fetch that recorded commit, never
the branch again. Approval of the request is the project's responsibility; a hash
is not publisher trust. No source discovery/automatic technology activation occurs.

## Self-contained bundle schema 1

Each selected Git tree path contains `guidance-bundle.json`:

```json
{
  "schema": 1,
  "id": "base",
  "entry": "README.md",
  "files": ["README.md", "detail/topic.md", "NOTICE"],
  "notices": ["NOTICE"]
}
```

The inventory lists all bundle files except the declaration, which is retained
automatically. No undeclared files under the selected bundle path are allowed;
unselected repository paths are irrelevant. Entry is a declared `.md` file; at
least one declared notice is required. `manifest.json` is reserved for storage.
Only regular non-executable Git blobs are accepted: no symlinks, executable modes
or submodules. Source bytes and relative topology are preserved, including notices.

Markdown inline links/images, reference definitions and URL autolinks are checked.
Local file targets must be declared in the same bundle; normal `../` links are
allowed only if normalization stays inside it. Local fragments are retained but
anchor existence is not checked. HTTP(S)/mailto links remain external and are not
fetched. Absolute, encoded escapes, backslashes, unknown schemes, case collisions
and ambiguous local query/percent forms fail. This is a conservative Markdown link
subset, not a full HTML/Markdown interpreter; HTML `href`/`src` navigation and
unsupported inline-link syntax fail. Keep bundle navigation in that subset.
Authored entry prose decides what to read, never the engine.

Source/bundle IDs use lowercase letters, digits and hyphens (letter first, max 64).
Paths are canonical relative POSIX paths using ASCII letters/digits/`_.-` segments
(max 240 characters); `.` is allowed only as bundle root/binding. Duplicate source
IDs/locators or bundle/binding pairs fail. A bundle ID may be bound to several
directories only when it identifies the same source/path. Different bundles can
overlap directory bindings; no semantic precedence is inferred.

Bounds: 16 sources, 64 bindings; 512 inventory entries including reserved metadata,
64 KiB declaration, 1 MiB per file/JSON input, 16 MiB bundle/selection content,
2 MiB Git tree output, 30 seconds per Git command. No source command is executed.

## Commands and independently retained expectations

```sh
agent-guides prepare --project PROJECT --request request.json --cache CACHE
agent-guides verify --project PROJECT --expected SELECTION_SHA256
agent-guides restore --project OTHER_PROJECT --lock saved-guidance.lock.json \
  --expected SELECTION_SHA256 --cache CACHE
agent-guides task-pin --project PROJECT --expected SELECTION_SHA256 \
  --output HOST_TASK_RECORD --policy extra-policy.md --overlay exceptions.md
agent-guides task-join --project PROJECT --identity HOST_TASK_RECORD \
  --expected-task HOST_TASK_SHA256
```

Successful commands emit JSON containing identities. Errors exit 1; invalid CLI
arguments exit 2. Capture preparation's selection digest in host execution evidence
before role work; do not derive a review expectation from possibly altered generated
files. Retain `HOST_TASK_RECORD` and its digest independently. `task-pin` creates
exclusively and cannot overwrite evidence or place it in `.guidance`/the lock.
Both roles join the same record; neither resolves latest or repins drift.

`guidance.lock.json` is the single portable selection: schema, exact sources,
bundles/bindings/snapshot digests and engine version/byte digest. Its canonical JSON
SHA-256 is the selection identity. It contains no cache/interpreter/root paths.
The executable remains versioned independently of bundle schema/content; restore
requires its recorded engine. A development version label is not byte identity.

Default cache: `PROJECT/.guidance/cache`; explicit `--cache` permits reuse in another
temporary/project root. Cache contains bare exact Git objects and verified bundle
snapshots. Project-local `.guidance/selections/` contains immutable staged selection
snapshots. Storage snapshot identity is distinct from the portable lock identity.
Verify needs only local selection bytes and the independently retained digest.
Restore is **offline only**: reuse snapshots or reconstruct from complete cached
exact objects. Missing data names the source/commit and fails without a network or
latest fallback. Moving upstream branches does not affect restore or review.

Candidates are validated before the lock is atomically replaced. A conflicting
existing lock, preimage drift or preparation failure preserves existing active
selection bytes. Cache candidates may remain after failure; no automatic pruning.
Writers use explicit directory locks; inspect an abandoned lock before retrying.
Files are read-only as an accidental-write guard, not a same-user sandbox. No live
snapshot is edited. Crash recovery for native multi-file integration belongs to T04.

Host task evidence retains source/bundle identities, selection digest, executable
identity and root `AGENTS.md`/`CLAUDE.md` plus explicit project-relative policy and
overlay hashes. Include nested policies, imported/configuration files explicitly;
automatic discovery is root-only, not an exhaustive native loader model. Native
files remain in place and local exceptions retain authority. No model compliance,
client loading, hot replacement or stable-release approval is implied.

## Verification fixtures

`tests/fixtures.py` creates two disposable Git repositories and three declared
bundles, including two bundles sharing one source commit. Tests move branches,
count resolution, restore to a second root without network, compare retained role
identities and exercise altered/missing/extra files, encoded escapes, tree modes,
case collisions, unsafe locators/refs, publication failures and policy/engine drift.
The distribution unittest rebuilds from sdist and runs the whole unittest suite
against an installed wheel outside checkout. See T02's completion record for actual
runtime results and the independent-review gate.
