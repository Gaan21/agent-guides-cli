# agent-guides: start here

Status: T01/T02 done; T03 blocked; T04 pending; T05 ready (2026-10-18).
Canonical board in Gaan21/agent-guides.
This is a durable handoff, not a release or consumer activation instruction.

## Read first

1. The working repository's maintainer instructions and current Git status/diff.
2. [Agreed scope](../delivery-scope.md): product decisions; do not reopen them.
3. [Technical proposal](../delivery-implementation-plan.md): reuse map and mechanics;
   schema/path/CLI details may be simplified with evidence.
4. The selected task below and completion records of its dependencies.

These three documents have different jobs: scope is the agreement, technical plan
is a design reference, this index owns order/status. Task files define acceptance.
Existing package usage docs describe live implementations, not the replacement.

## Closed decisions at a glance

- New public repository and neutral Python package: `agent-guides` (availability
  unverified). Stable distribution: PyPI and releases; macOS/Linux targets.
- Multiple Git sources; latest approved `develop` resolved once per source on
  install/update, exact recorded selection on restore. Git-only v1.
- Self-contained Markdown bundles: short authored entry, local detail, inventory
  and notices. Reading instructions live beside content, not in the engine.
- Common guidance separate from private `worktracker-architecture-guides` in its
  own new repository. Preserve every rule; uncertainty means WorkTracker.
- Select both bundles in one project connection; no extra architecture profile.
- No delivery hooks/daemon, leases, mandatory end/rebaseline, AI retrieval,
  per-content executable environments, or per-consumer wrappers/probes.

## Task board

Statuses are `ready`, `pending`, `in_progress`, `blocked`, `done`. Update this board
and the task header together. Mark `done` only with evidence satisfying that task.
T01 establishes the scaffold; T02 adds non-activating preparation. Integration is pending.

| ID | Task | Status | Dependencies / executor |
| --- | --- | --- | --- |
| T01 | [Bootstrap neutral repository/package](T01-bootstrap.md) | done | Independent review accepted; see T01 completion record. |
| T02 | [Exact multi-source preparation](T02-preparation.md) | done | Independent corrective review accepted; refreshed four-job CI passed. |
| T03 | [Native loading feasibility](T03-native-loading.md) | blocked | Installed V2 rechecked: configured startup and inline read-triggered entries work; root-started edit-first delivery still fails. |
| T04 | [Complete lifecycle and recovery](T04-lifecycle.md) | pending | T02 + T03; tool agent, then client confirmation. |
| T05 | [Lossless common/private content split](T05-content-split.md) | ready | T01 + T02 done; consumer agent with private access. |
| T06 | [WorkTracker acceptance and migration](T06-migration.md) | pending | T03 + T04 + T05; consumer agent and owner. |
| T07 | [Release readiness and authorized publication](T07-release.md) | pending | T06; release maintainer and owner. |

After T02, T05 can run alongside T03/T04 in separate repositories/owned files.
Do not assign concurrent agents the same task or shared mutable selection.
Use independent implementation/review against one retained task identity.

## Execution boundaries

- T01 must obtain the actual owner and approved workspace and check repository/
  package-name availability. Fixed product decisions do not authorize remote
  creation, staging, commits, pushes, releases, registry publication or activation.
  Obtain specific authorization when that action is needed; do not repeat approval
  requests for already authorized routine work.
- Preserve current changes and live consumers. No legacy deletion or automatic
  migration while developing the replacement. Do not edit live snapshots.
- Pin source, selection, engine, local policy and overlay identity once per task.
  Keep expected identity independently of generated files for the reviewer.
- Public records contain no private paths, consumer logs, architecture rules or
  product APIs. Detailed preservation/classification records stay private.
- Verify host integrity, observed client loading and model compliance separately.
  Tests may establish the first without establishing the other two.
- Read-only inspection before implementation is fine. Tests must exercise real
  supported available runtimes; label unavailable macOS/Linux/client checks pending.

## Moving the handoff to the new repositories

This folder is the bootstrap home because the new repositories do not exist yet.
At T01, carry scope, technical reference and the task board into `agent-guides`,
preserving maintainer policy and fixing relative links. Record its actual location
here and leave a pointer; do not keep two independently edited task boards.
Relevant private task instructions may be linked/copied as a handoff, but detailed
WorkTracker content/evidence belongs only in the private repository.

T01 transfer completed: this checkout is the authoritative handoff. Public remote:
<https://github.com/Gaan21/agent-guides>. Owner subsequently authorized committing
and pushing the scaffold and legacy forwarding changes. Source upload is separate
from releases, registry publication and consumer activation.
The approved checkout is the sibling `agent-guides` directory of the legacy
checkout; exact machine locations and execution identity remain in local Git
metadata, outside public source. Legacy documents now contain forwarding pointers.
Read [T01 results](T01-bootstrap.md#completion-record--2026-10-17) before T02.

## Every task's completion record

Update its status and append: changed files, delivered behavior, exact check
commands/results, tested platforms/client versions, independently retained task
identity, review result, limitations/blockers and the next ready task. Retain exact
refs in authorized execution evidence, not public source-report dumps. Report
remaining authorization requirements. Do not mark acceptance passed from intent,
generated configuration, or a model's claim of compliance.

## Prompt for the next agent

> Read the working repository's maintainer instructions, inspect status/diff,
> then read docs/tasks/README.md and its agreed-scope link. Execute the first
> ready task whose execution inputs and permissions are available. Read only the
> relevant technical-plan sections and dependency results. Preserve existing work
> and content. Do not reopen closed decisions, activate a consumer, publish or
> perform Git publication actions without authorization. If blocked, record the
> precise missing input rather than guessing. Finish by updating the task board
> and completion record with evidence and the next handoff.

Corrective review evidence: `.git/T02-fix-start.json`, `.git/T02-fix-identity.json`,
exact artifacts in `.git/T02-fix-artifacts/`, `.git/T02-fix-results.md` and
`.git/T02-fix-independent-results.md`. The read-only `.git/t02_fix_review.py` checks
the corrected candidate; never rerun capture scripts or replace expectations.
Original T01/T02 evidence/artifacts remain preserved. Both corrected roles share
one retained identity over the original exact source commits/bundles.

Current next-agent assignment: **review the installed-V2 mechanism/trials and retain
bounded infeasibility unless a native edit-triggered route becomes available**, keeping
all original/corrective identities and evidence. See the
[V2 continuation](T03-native-loading.md#opencode-2032-diagnostic-continuation--2026-10-18)
and preceding independent matrix.
Installed-client access and authorized disposable fixtures are required. T05 is also ready for
a consumer agent with private access and may proceed in a separate owned workspace.
Read the selected task's inputs before work; readiness does not authorize repository
creation, content publication or consumer activation. T04 still depends on T03.

T02 closed after independent corrective acceptance and the refreshed four-job
macOS/Linux × Python 3.11/3.15 matrix; see its final completion record and linked CI.
Corrective source and closure documentation were authorized for upload to
`origin/develop` in this session. Future publication requires its own authorization.

T03's Claude correction passed independent integrity/loading review, with one
reporting correction: the original post-compaction turn restored prior read context
but issued no fresh reads. A supplemental turn now proves three fresh successful
reads in that same session. Original expectations were preserved.

OpenCode 1.19.3's installed loader was observed through local request capture:
initial context contains native navigation directives, not prepared entry contents.
Configured-model trials also show `apply_patch` succeeds before folder policies
arrive; subsequent reads attach them. TUI compaction/resume, local conflicts,
synthetic guard rejection and nested-worktree boundaries were exercised. These
results do not satisfy T03's connection contract. Linux clients and Claude's
worktree-specific external-import approval remain pending.

Supplemental evidence, archived corrective handoff bytes and exact invocations are
in `.git/T03-r3-evidence/`; use read-only `.git/t03_r3_verify.py` and the private
`.git/T03-r3-results.md`. The verifier checks the old seals against archived handoff
bytes, rather than replacing expectations after documentation changes. Do not rerun
arrangement/capture scripts. **T04 remains pending until T03 acceptance.**

OpenCode **2.0.32** was subsequently tested with an official checksum-matched
standalone binary. Native configured `instructions` deliver exact short entries at
root/two subdirectory starts, but do not supply folder policies before a first
root-started `patch`, nor folder-configured entries during later scoped reads.
Eight local-provider diagnostic invocations establish loader/tool timing only;
configured-model behavior and the remaining V2/client/platform matrix are pending.
Evidence and durable replicas: `.git/T03-v2-evidence/`; read-only review:
`.git/t03_v2_verify.py`. Historical temporary roots are unavailable, so the original
full verifier fails; archived seals and bounded observations were checked separately
without rewriting expectations. The V2 diagnostic still does **not** accept T03.

Installed-client continuation confirmed the actual Homebrew-linked binary reports
**2.0.32** and matches the earlier standalone binary byte-for-byte. New fixtures
confirm that inline short entries in folder `AGENTS.md` load on scoped reads or
directory listings, not on first `patch`. Embedded-code inspection explains the
separate startup/configured and read-discovery routes. See the
[installed-V2 record](T03-native-loading.md#installed-v2-mechanism-and-new-candidates--2026-10-18).
New read-only review: `.git/t03_installed_verify.py`; original V2 seals remain
unchanged and their public handoff bytes are archived independently before edits.
T01/T02 stay done, T03 blocked, T04 pending, T05 ready. No integration proceeds.
