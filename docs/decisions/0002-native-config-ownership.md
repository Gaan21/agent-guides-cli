# ADR 0002 — Native configuration ownership without JSONC rewriting

Date: 2026-10-20. Status: T04 implementation design; not host activation approval
or installed-client acceptance. Scope/acceptance in [T04](../tasks/T04-lifecycle.md)
and [T03](../tasks/T03-acceptance.md) remain authoritative.

## Problem and scoped investigation

The first lifecycle candidate required a free `.opencode/opencode.json` and refused
managed project-discovery-disabled hosts. Editing arbitrary JSONC would require a
proven syntax-preserving editor; stripping comments/reserializing or introducing an
ad hoc parser cannot establish preservation of user settings and comments.

The native V2 configuration contract combines direct project documents and
`.opencode` documents, including their `instructions` entries. T03 separately accepts
a read-only host-controlled JSON route using `{env:PWD}/AGENTS.md` when project
discovery is disabled. These existing mechanisms permit a smaller ownership design
without changing user JSONC at all. References:
[configuration](https://opencode.ai/v2/docs/config/),
[instructions](https://opencode.ai/v2/docs/instructions/).

## Implemented design

- Ordinary discovery: prefer an empty `.opencode/opencode.json(c)` slot; otherwise
  use an empty direct `opencode.json(c)` slot. Create only the `.json` file in that
  slot, with native `instructions` pointing to the prepared short entry. Never create
  a `.json` beside an existing `.jsonc` in the same slot. Persist the chosen path in
  portable connection identity; restore must reproduce it, not choose another path.
- Existing documents, their comments, guard/lint settings and local exceptions stay
  byte-for-byte untouched. When both slots are occupied, stop before resolution or
  activation and report the collision. Do not rename/move user files, guess config
  precedence, recommend disabling discovery as a workaround, or silently merge.
- Managed discovery-disabled hosts: the operator explicitly supplies `--host-config`
  for an already approved external read-only JSON configuration. Its instruction list
  must contain the accepted `{env:PWD}/AGENTS.md` route exactly once. Retain its full
  byte digest in portable identity and its machine-local path only in local ownership.
  No settings, permissions or project-discovery flags are written by the package.
- Check the operation's actual `cwd`, absolute `PWD`, existing disabled-discovery flag and
  `OPENCODE_CONFIG` binding before activation. Reject missing/stale parent-worktree
  bindings. Future client/production-launcher correctness remains a host prerequisite,
  not a claim inferred from those installation-time checks.
- Put only the scoped authored short index in an owned root `AGENTS.md` block; relocate
  links for that containing file. Preserve all local bytes outside it. Claude retains
  its native short-entry import. If root `CLAUDE.md` already imports `AGENTS.md`, reuse
  that import instead of adding a second entry delivery; never own/remove that user
  import. Ambiguous existing imports need explicit resolution.
- All selected project surfaces participate in the same journal/preimage/recovery
  path. Host configuration never enters the write set. Remove touches only owned
  project bytes and leaves the approved host config and user imports intact.

## Evidence and limits

Synthetic unittests cover existing commented settings, shared imports, update/exact
restore/removal, modified host identity, invalid bindings, a real linked worktree and
fault recovery without any host write. These are host tests, not installed-client
or model evidence. An occupied configuration slot or modified owned material remains
an explicit conflict requiring operator resolution; arbitrary JSONC merge is not an
advertised operation. Native loading and the supported-platform matrix still require
their own acceptance evidence. No client/version trial is introduced by this record.
