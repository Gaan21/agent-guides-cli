# agent-guides: start here

Status: T01 done; T02 implemented, independent review and matrix pending (2026-10-17).
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
| T02 | [Exact multi-source preparation](T02-preparation.md) | in_progress | Implemented locally; independent review and Linux/minimum-Python checks pending. |
| T03 | [Native loading feasibility](T03-native-loading.md) | pending | T02; installed-client/consumer agent. |
| T04 | [Complete lifecycle and recovery](T04-lifecycle.md) | pending | T02 + T03; tool agent, then client confirmation. |
| T05 | [Lossless common/private content split](T05-content-split.md) | pending | T01 + T02; consumer agent with private access. |
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

Current next-agent assignment: **independently review T02**, not start T03/T05.
Read T02's implementation record and `docs/preparation.md`. Compare working source,
tests and exact retained artifacts with `.git/T02-identity.json` and the evidence
identified in `.git/T02-results.md`; do not rerun capture or replace expectations.
Local macOS Python 3.14/3.15 checks passed; Linux and Python 3.11 checks for the new
implementation remain pending. The prior T01 matrix does not cover T02.
T01's closure was committed/pushed with session authorization. The owner subsequently
authorized T02 staging/commit/push in this session to run its CI; results follow in
T02's record. Future sessions must obtain their own publication authorization.
After independent acceptance, mark T02 done and T03/T05 ready in board and headers;
otherwise record the precise gap and retain T02 open. Preserve both task identities.
No release, registry publication or consumer activation is authorized by this handoff.
