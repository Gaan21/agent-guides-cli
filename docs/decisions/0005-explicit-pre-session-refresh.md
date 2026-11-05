# ADR 0005 — Explicit pre-session refresh for direct work

Date: 2026-11-04. Status: implemented in the development candidate; host refresh
verified in existing owner-operated project connections. Not a stable release.

## Decision

The owner chooses one explicit command before opening the usual client, rather
than a hook or a replacement launcher. A bounded native Claude Code observation
found that a SessionStart hook changing an imported index did not replace the old
index in the first outgoing request. Waiting for the hook was insufficient.

`refresh` opts an already connected project into fetching its selected sources
from their approved branch through explicitly selected operator-owned mirrors,
then reuses the existing journaled `update`. A separate external expectation is
advanced after success. It never creates connections, installs hooks, changes
global configuration or edits tracked integration files. Managed-host workflows
remain separate and unchanged.

On download/update failure, an intact connection verified against the retained
expectation may be used with an explicit stale-copy warning. Modified data or an
incomplete transaction is not an offline fallback. No background refresh or
mid-conversation guide replacement is introduced.

This is an opt-in addition to the original explicit-update scope, not permission
to update every consumer on startup or change implementation/review identity.
Usage, recovery and evidence limits: [pre-session refresh](../refresh.md).

## Tool updates are not content tampering

An activation attempt exposed a historical equality check against the entire
executing tool's source digest in lock validation. Any source update made existing
connections unreadable, even with unchanged guide bytes. The owner chose to verify
the effect rather than require the old executable: recorded engine identity is
preparation provenance, not a permanent executable requirement. The current tool
validates the supported schema, independent expected selection, snapshots and
rendered connection. `update` records the current engine in its new selection;
exact restore retains the original provenance. Task-role evidence still compares
the executing engine and local policy independently for that task.

Tests cover unchanged old connections across a tool update, new source content,
offline restore across engines, altered local indices, changed provenance without
approval and an executing-engine difference between task roles.
