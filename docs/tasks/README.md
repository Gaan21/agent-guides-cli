# agent-guides-cli: start here

Status: T01/T02/T03/T04/T05 done; T06/T07/T08 pending (2026-10-21).
Canonical board in Gaan21/agent-guides-cli.
This is a durable handoff, not a release or consumer activation instruction.

## Read first

1. The working repository's maintainer instructions and current Git status/diff.
2. [Agreed scope](../delivery-scope.md): product decisions; do not reopen them.
3. [ADR 0001](../decisions/0001-selective-guidance-reading.md): current selective-reading
   decision, alternatives, evidence limits and reconsideration criteria.
4. [Technical proposal](../delivery-implementation-plan.md): reuse map and mechanics;
   schema/path/CLI details may be simplified with evidence.
5. The selected task below and completion records of its dependencies.

The core documents have different jobs: scope is the agreement, technical plan
is a design reference, this index owns order/status. Task files define acceptance.
Decision records explain why a direction was chosen; they do not replace the board
or turn bounded experimental results into task acceptance.
Existing package usage docs describe live implementations, not the replacement.

## Closed decisions at a glance

- Public tool repository and neutral Python package: `agent-guides-cli`; common
  guidance in one public `agent-guides` catalog, one bundle per stack/topic
  ([ADR 0003](../decisions/0003-tool-and-guides-repositories.md)). Stable distribution: PyPI and releases; macOS/Linux targets.
- Multiple Git sources; latest approved `develop` resolved once per source on
  install/update, exact recorded selection on restore. Git-only v1.
- Self-contained Markdown bundles: short authored entry, local detail, inventory
  and notices. Reading instructions live beside content, not in the engine.
- Common guidance separate from private `worktracker-architecture-guides` in its
  own new repository. Preserve every rule; uncertainty means WorkTracker.
- Select both bundles in one project connection; no extra architecture profile.
- No delivery hooks/daemon, leases, mandatory end/rebaseline, AI retrieval,
  per-content executable environments, or per-consumer wrappers/probes.
- Root-started work: native short entry, model-selected relevant topics/dependencies,
  reuse while in context. No all-topic/per-patch reads or absolute editing gate.

## Repository map

| Repository | Visibility | Role |
| --- | --- | --- |
| `agent-guides-cli` (this one) | public | Tool, task board and decisions. No authored guidance. |
| `agent-guides` | public | Common guidance catalog; T05 prepares all existing stack/topic bundles. |
| `worktracker-architecture-guides` | private | Product catalog: independently selected product bundles plus private T05 evidence; name retained for now. |
| `flutter-agent-guidelines` | public | Legacy runtime and current Flutter payload; WorkTracker still uses it. |
| `dev-guidelines` | private | Deprecated archive; several non-Flutter consumers still load it. |

All are cloned as sibling directories with the repository name. Each new guides
repository has a README/AGENTS.md pointing back to this board. Legacy retirement
order: [T06](T06-migration.md#legacy-retirement).

## Task board

Statuses are `ready`, `pending`, `in_progress`, `blocked`, `done`. Update this board
and the task header together. Mark `done` only with evidence satisfying that task.
T01 establishes the scaffold; T02 adds preparation; T04 delivers accepted neutral
lifecycle/connection tooling. Content split and consumer integration remain separate.

| ID | Task | Status | Dependencies / executor |
| --- | --- | --- | --- |
| T01 | [Bootstrap neutral repository/package](T01-bootstrap.md) | done | Independent review accepted; see T01 completion record. |
| T02 | [Exact multi-source preparation](T02-preparation.md) | done | Independent corrective review accepted; refreshed four-job CI passed. |
| T03 | [Native loading feasibility](T03-native-loading.md) | done | Independent bounded macOS/Linux reviews and owner acceptance; root-start conditions in the acceptance record. |
| T04 | [Complete lifecycle and recovery](T04-lifecycle.md) | done | Independent corrective and bounded closure review accepted; see [acceptance](T04-acceptance.md). |
| T05 | [Lossless common/private content split](T05-content-split.md) | done | Bounded local content acceptance after independent R1–R5 corrections; see [acceptance](T05-acceptance.md). |
| T06 | [WorkTracker acceptance and migration](T06-migration.md) | pending | T03 + T04 + T05; consumer agent and owner. |
| T07 | [Release readiness and authorized publication](T07-release.md) | pending | T06; release maintainer and owner. |
| T08 | [Lightweight selective-reading observation](T08-lightweight-observation.md) | pending | T03 acceptance + authorized T06 clone pilot; client/consumer agent and reviewer. Not a T04/T06/T07 dependency. |

After T02, T05 can run alongside T03/T04 in separate repositories/owned files.
T08 may run alongside the authorized T06 pilot and later authorized ordinary use;
its number does not require waiting for T07 or introduce an observation release gate.
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
At T01, carry scope, technical reference and the task board into the tool repository
(then `agent-guides`, now `agent-guides-cli` per ADR 0003),
preserving maintainer policy and fixing relative links. Record its actual location
here and leave a pointer; do not keep two independently edited task boards.
Relevant private task instructions may be linked/copied as a handoff, but detailed
WorkTracker content/evidence belongs only in the private repository.

T01 transfer completed: this checkout is the authoritative handoff. Public remote:
<https://github.com/Gaan21/agent-guides-cli> (renamed by ADR 0003). Owner subsequently authorized committing
and pushing the scaffold and legacy forwarding changes. Source upload is separate
from releases, registry publication and consumer activation.
The approved checkout is the sibling `agent-guides-cli` directory of the legacy
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

Current handoff (2026-10-21): T05 is done for bounded local content preparation
across the existing technologies/topics. Read [T05 acceptance](T05-acceptance.md).
**Next: T06**, with its own consumer access, retained identity and explicit pilot/
migration authorization. It remains pending; closure does not start it automatically.
The T05 prompt and assignments below are historical, not the current work queue.
Deferred improvement proposals remain separate, not new acceptance gates.

> Read the working repository's maintainer instructions, inspect status/diff,
> then read docs/tasks/README.md (including its repository map), its agreed-scope
> link, ADR 0001, ADR 0003 and T04-acceptance.md. T01–T04 are complete. Continue
> T05 as described in T05-content-split.md: the public `agent-guides` and private
> `worktracker-architecture-guides` repositories exist and are cloned as siblings;
> the private README lists exact inputs. Keep detailed classification/preservation
> evidence in that private repository's `evidence/`. Read only the
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

Historical T04-to-T05 assignment: **T05 — lossless common/private content split**, in a
separately owned workspace with private access. Read [T04 acceptance](T04-acceptance.md)
for the delivered neutral tooling, recorded checks and limits; do not resume its
historical implementation checkpoints or earlier T03 feasibility queues.
Routine sessions start at the project or selected-worktree root. Claude imports the
short index; OpenCode uses native `instructions`, with an explicitly host-controlled
route when project discovery is disabled. The managed Linux candidate depends on
correct `PWD`; production launcher binding/registration is not yet applied or verified.
Preserve isolation, existing guards and all retained failures. Do not reopen strict
automatic injection, subdirectory startup or Linux Claude TUI as feasibility gates.
T06 remains pending T05. T08 still requires an authorized T06 pilot. Task readiness
does not authorize live managed configuration changes, migration or activation.
Repositories for T05 already exist (see the repository map). Authorization status
is recorded in [T05](T05-content-split.md#workspace-destinations-and-authorization);
production changes and releases need their own authorization. Preserve legacy delivery and every rule until authorized T06 migration.

T02 closed after independent corrective acceptance and the refreshed four-job
macOS/Linux × Python 3.11/3.15 matrix; see its final completion record and linked CI.
Corrective source and closure documentation were authorized for upload to
`origin/develop` in this session. Future publication requires its own authorization.

## Historical evidence summaries

The verdicts below describe their original trial criteria and dates; the current
board, ADR 0001 and selective-reading continuation govern the next assignment.

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

Subsequent owner clarification authorizes model-selected relevant guide reading
before applicable edits, with reuse while content remains in context; absolute
enforcement is not required. This supersedes the hard-gate blocker as the current
decision criterion, not its historical observations. T03 is **in_progress** for the
[selective-reading trial](T03-selective-reading.md); T04 remains pending acceptance.

## Decision/task alignment handoff — 2026-10-18

Owner authorized documenting the decision, aligning future tasks and adding T08's
bounded observation plan, plus commit/push of the documentation. ADR 0001 records
problem, alternatives, selected simple route, evidence limits and escalation criteria;
it is a basis for a possible public narrative, not authorization to post externally.
T04 separates host verification from behavior; T05 clarifies authored relevance;
T06 samples selective reading and reuse; T07 limits advertised guarantees. No engine,
monitor, factory integration, consumer activation or new release gate was implemented.

Checks: `python3 .git/t03_handoff_verify.py`, six identity unittests on Python 3.15.0,
and `git diff --check` passed. The pre-edit selective verifier passed unchanged;
its sealed handoff bytes were archived before these edits, not rebaselined. New
read-only handoff review: `.git/t03_handoff_verify.py`; execution/archive record:
`.git/T03-decision-results.md`. Original source Git objects and the pending
Claude/context-loss/TUI/Linux acceptance checks were not recreated or claimed passed.

Evidence under `.git/` is local-only and is not uploaded with source. On this
checkout, use the new read-only review for archived expectations; on a fresh clone,
obtain authorized evidence or retain a new trial before claiming prior checks.
T03 stays in_progress; T04 pending; T05 ready; T08 pending. Continue T03, not T04/T08.

The preceding status is historical. The owner-accepted closure below supersedes
those execution queues, without changing their failed/pending observations.

## Fresh installed-client continuation — 2026-10-19

[Root-started trial](T03-root-startup.md): both real configured models read the
screen guide and its dependency before editing, reuse topics, switch to repository
and web guidance, and apply the native web exception. Both native TUIs compacted;
subsequent mobile work made fresh dependency reads. Initial entry observation and
synthetic guard rejection are recorded separately from remote-model compliance.
Read-only review: `.git/t03_root_verify.py`; exact evidence/failed attempts remain
in `.git/T03-root-evidence/`. Six identity tests pass on Python 3.15.0. No engine
change or activation. Independent read-only review supports bounded macOS
feasibility; `.git/T03-root-independent-results.md` retains its findings. Owner
decision and the recorded limits still prevent claiming full acceptance or starting T04.

Remaining-check continuation: [exact cached Git objects and a real linked worktree](T03-remaining-checks.md)
now have independent bounded acceptance. Original source directories were not
recreated. Claude's worktree-subdirectory topic access requires the tested native
`--settings` overlay; the first automatic-discovery failure remains retained. Linux
clients are still pending because no running Linux environment/model access was
available. Read-only review: `.git/t03_finish_verify.py`. T03 is not marked done.
Python 3.15.0 clean-distribution checks and all 32 installed-wheel unittests pass;
these are host/package checks, not Linux installed-client acceptance.

## T03 completion and T04 handoff — 2026-10-19

Owner accepted closing T03 for **root-started** project/worktree sessions after
independent macOS and Linux reviews. Linux's corrected OpenCode V2 native-index
candidate passes both root cases while preserving disabled project configuration;
the earlier manual-discovery and invalid-worktree results remain failed/invalid.
Claude Linux TUI/subdirectory limits are explicitly outside this accepted workflow.

Read [T03 acceptance](T03-acceptance.md) for routes, versions, exact check references,
private evidence locations, guard limitations and the next-agent execution order.
No permanent integration, production configuration, consumer activation or release
was performed. Documentation commit/push is explicitly authorized for this closure;
future publication and production actions require their own authorization.
**T03 done; T04 ready, not started; T05 ready; T06/T07/T08 pending.**

## T04 implementation checkpoint — 2026-10-20

T04 is now **in_progress**. Project-local lifecycle/recovery commands, immutable
retention, selected-client ownership and offline identity comparison are implemented;
58 source tests and 58 clean installed-wheel tests pass on macOS/Python 3.15.0.
See [T04's checkpoint](T04-lifecycle.md#implementation-checkpoint--2026-10-20)
and the [development lifecycle contract](../lifecycle.md) for exact commands/limits.
Managed-host registration, existing-JSONC handling, Linux/runtime matrix, measured
production setup, installed-client confirmation and independent review remain pending.
The owner declined a new OpenCode-version trial; none was run during implementation.
T05 stays ready; T06/T07/T08 remain pending. No live activation or publication.

## T04 completion and T05 handoff — 2026-10-20

The owner subsequently authorized disposable native-client acceptance, independent
review, Docker-based Linux checks, task-only cleanup and source commit/push. T04 is
**done** after independent corrective and final closure acceptance; its earlier
implementation queues and the preceding checkpoint are historical.

See [T04 acceptance](T04-acceptance.md) for the delivered lifecycle/ownership contract,
73-test package matrix, actual installed-client observations, interruption/input
caveats, independent evidence locations and operator prerequisites. No production
host, live consumer, legacy runtime or stable release was changed or activated.

**Next: T05**, using approved private inputs/access in a separately owned workspace.
Preserve every requirement and keep detailed classification evidence private; uncertain
classification stays in WorkTracker. Do not start T06 migration until T05 passes.
T07/T08 remain pending. This task's commit/push authorization is not permission for
future source publication, private-repository creation, release or consumer activation.

## Tool/guides repository split — 2026-10-20

The owner renamed the tool to `agent-guides-cli` and placed all common guidance in a
new public `agent-guides` catalog; WorkTracker architecture stays private
([ADR 0003](../decisions/0003-tool-and-guides-repositories.md)). Code, tests,
packaging and usage docs use the new name; package and distribution checks pass.
T05 now prepares the Flutter bundle in `agent-guides` plus the private bundle.
Earlier records keep the names they executed. Client trials were not repeated.
The GitHub repository was renamed, the local checkout moved to `agent-guides-cli`,
legacy forwarding links were updated, and both new guides repositories were created,
cloned and given README/AGENTS.md pointers. **Next: T05.**

## T05 completion and T06 handoff — 2026-10-21

T05 is **done** after authorized bounded administrative acceptance of local content
preparation and the independent R1–R5 corrective pass chain. Ten common bundles and
two independently selectable private product bundles are prepared; no engine,
consumer, installed snapshot or legacy delivery was changed by this closure.

See [T05 acceptance](T05-acceptance.md) for recorded commands, 157 final passing
test results, offline restore/selection checks, review limits and upload boundaries.
Exact identities and detailed dispositions remain private; `.git/` seals are
local-only and ordinary source commits do not publish them. This is not stable
release approval, source trust, consumer migration or new native/client/model proof;
T03's accepted scope and limitations are unchanged.

**Next: T06**, subject to its existing prerequisites and separate authorization;
T06/T07/T08 remain pending. No staging, commit, push, upload or activation occurred.
The private T05 upload has prior conditional owner approval; public catalog content
upload still requires explicit approval. Documentation approval is not blanket source
upload permission. Retain T05's [deferred follow-up links](T05-content-split.md#handoff)
and the private evidence index as low-priority improvements, not T05 gates.
