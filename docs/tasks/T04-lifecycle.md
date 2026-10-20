# T04 — Complete lifecycle and recovery

Status: done. Depends on: T02 + T03 (done). Executor: neutral tool agent.
Accepted scope, evidence and next handoff: [T04 acceptance](T04-acceptance.md).
Read [handoff](README.md), technical-plan sections 3–4, T03 evidence and
[ADR 0001](../decisions/0001-selective-guidance-reading.md).
T03's [acceptance and next-agent order](T03-acceptance.md) govern the connection;
do not resume superseded feasibility queues. Neutral implementation started 2026-10-20;
the owner declined a new OpenCode-version trial. No live integration is authorized.

## Goal

Implement complete install/update/restore/status/verify/remove operations using
the tested native mechanisms, without a consumer-owned wrapper or probe.

## Work

- One operation performs preparation, connection and verification. Preview may be
  available but is not a mandatory separate configure/install sequence. Applying
  a retained proposal never re-resolves source tips.
- Persist confirmed bundle/client/scope selection. Routine updates preserve local
  exceptions and lint choices, and do not reinstall a compatible executable.
- Inventory only selected clients; preserve local instruction authority, user
  configuration/comments and unrelated guards. Detect competing legacy loaders.
- Track owned files/blocks, before/after bytes and a durable transaction journal;
  recheck preimages, publish activation last and retain working selections.
- Recover interrupted operations without overwriting unknown edits. Multi-file
  changes are not an atomic transaction merely because each file uses rename.
- Remove only owned integration; preserve unrelated edits and recorded selections.
  Modified owned material needs explicit resolution. No silent cache deletion.
- Verification is offline comparison against retained expected identity, not an
  implicit repair, source refresh or policy rebaseline.
- Connect the T03-accepted short-entry route for root-started work; leave topic
  relevance/dependencies authored beside the content. Do not add a selector engine,
  mandatory per-patch reads, all-topic injection or behavioral enforcement to `verify`.
- Keep strict integrity/ownership checks separate from observed client delivery,
  voluntary topic reads and application. Host success cannot certify model compliance.
- Report restart/reload needs. No live snapshot rewrite or hot-context guarantees.

## Accepted connection prerequisites from T03

- Start at the project/selected-worktree root, not a subdirectory. Retain/check the
  root identity separately from environment strings; `cwd` and `PWD` must agree.
- Claude imports the short index natively. Preserve existing root/folder policies;
  never bypass host-managed permissions or fabricate external-import approval.
- OpenCode V2 uses native `instructions`. The tested managed-host route keeps
  `OPENCODE_DISABLE_PROJECT_CONFIG=1` and supplies a host-controlled read-only
  `OPENCODE_CONFIG` with `instructions: ["{env:PWD}/AGENTS.md"]`. A fixed parent path
  fails worktree isolation; stale/missing `PWD` can silently select the wrong index.
- Define owned registration/merge/rollback and report operator prerequisites when
  host configuration is not writable or not authorized. Do not change live managed
  settings, add consumer launchers or broaden access as an implicit install step.
- Native entry arrival, selected-topic behavior and guard enforcement are different
  checks. No terminal-protection claim follows from a run that never offered that
  tool. Consumer guard verification and authorized activation remain separate.

## Acceptance

`unittest` covers complete lifecycle, no-ops, concurrent preparation, faults at
every write/publication stage, restart/retry, altered owned blocks, unrelated user
edits, changed content updates, retained-version recovery and exact restores.
Check engine/schema mismatches, root/scoped registration and source/link integrity.
Prove preservation of user bytes, not only equivalent parsed settings.

Run distribution/clean-install checks and macOS/Linux tests for supported behavior.
Repeat installed-client checks when the implementation changes T03's mechanism.
Confirm the installed root entry supports relevant topic reads and reuse under
T03's accepted limits, without duplicating folder/root delivery. Do not require a
monitoring service or ongoing read audit to install or use the package.
Measure every required setup/update/restore/removal step, including initial Python/
Git/tool acquisition. A wrapper hiding many required configurations is not success.

## Handoff

Record one documented usage path and tested commands. Mark T06 ready only after
T05 also passes. Do not migrate existing consumers in this task.
Keep [T08 observation](T08-lightweight-observation.md) out of lifecycle dependencies;
record instrumentation gaps rather than implementing unapproved capture machinery.
Full-task acceptance: done for neutral root-started tooling; production activation
and consumer acceptance remain separate. Historical implementation progress follows.

The completion record below supersedes the earlier checkpoint's implementation gaps
and queue without relabeling any failed/pending observations. Do not infer unavailable
client/platform checks from host tests.

## Implementation checkpoint — 2026-10-20

Owner authorized continuing T04 without another OpenCode-version experiment.
This checkpoint implements neutral project-local tooling only; T04 stays
**in_progress**. No production settings, consumer migration or publication occurred.

Delivered:

- `src/agent_guides/lifecycle.py`, `native.py`, `transactions.py`: one-operation
  project install/update, connected offline restore, status/verify, owned removal
  and restartable recovery. Native routes are a Claude import and a new owned
  OpenCode project `instructions` file, not installed-client acceptance evidence.
- Reused T02 acquisition/staging through `preparation.py`; source selectors resolve
  once and exact revision policies persist. Prepared-only commands cannot overwrite
  a recorded native connection. Prior selections/locks and completed/rolled-back
  transaction bytes remain retained. No snapshot is edited or cache pruned.
- Durable preimage checks, activation-last lock publication, conflict-preserving
  rollback, LF/CRLF/outside-byte preservation and file-mode retention. Local ignored
  storage does not modify root ignore rules. Only selected client settings are
  inventoried; known legacy collisions fail rather than trigger migration.
- Lifecycle task records retain selected project settings and ownership identity
  independently for both roles. Public documentation is [lifecycle.md](../lifecycle.md),
  with README/preparation updates; no product content or consumer wrapper is added.
- `tests/test_lifecycle.py`, `test_transactions.py`, CLI orchestration and exact
  distribution inventories cover the new candidate and existing T02 behavior.

Checks on **macOS 27.0.1 arm64 / Python 3.15.0**:

```sh
.venv-t04/bin/python -m unittest discover -s tests -p 'test_transactions.py' -v
.venv-t04/bin/python -m unittest discover -s tests -p 'test_*.py' -v
AGENT_GUIDES_ARTIFACT_DIR="$PWD/.git/T04-artifacts" .venv-t04/bin/python tests/check_distribution.py -v
.venv-t04/bin/python .git/t04_review_candidate.py
git diff --check
```

Eight focused transaction tests and all **58** suite tests pass. The distribution
check builds wheel from sdist, checks resources/notices, installs cleanly outside
the checkout and passes all **58** installed-wheel tests. Retained development
artifacts/digests are outside source; this is not stable-release approval. Read-only
retained-fixture review passes exact Git object/bundle, engine, selection, local
policy and ownership comparisons; it is **not an independent review**.

Evidence: original `.git/T04-start.json`, independently retained
`.git/T04-review-expected.json`, `.git/T04-evidence/`, `.git/T04-artifacts/` and
`.git/T04-results.md`. Do not recapture expectations or resolve tips for review.
The initial source-only invocation failed without installation; an early suite
timed out, and another ran while engine files were changing and failed identity
comparisons. Those attempts remain recorded; only the stable rerun/artifacts above
are passing evidence. An initial evidence-fixture root rejection and read-only
review-script path error were corrected without replacing source/task expectations.

Remaining before T04 acceptance:

1. Implement the approved managed-host registration/root prerequisites, without
   touching live settings implicitly. This candidate deliberately refuses disabled
   project discovery; it does not yet implement T03's managed `PWD` route.
2. Resolve existing `.opencode` JSONC integration through a scoped design/spike or
   obtain an explicit accepted boundary. The current safe refusal is not full merge
   support, and modified owned config is preserved for explicit resolution.
3. Confirm changed routes in installed clients only when authorized, run Linux and
   the supported Python matrix, and obtain independent review of the same candidate.
   No client/version trial was run; prior T03 acceptance does not cover these bytes.
4. Measure complete first-use prerequisites/restart/operator steps. Retained synthetic
   API timings are not production setup, another physical machine or native loading.

Continue T04, not T06. T05 remains independently ready with private access. No
staging, commit, push, release, registry publication or live activation is authorized
by this checkpoint.

## Completion record — 2026-10-20

T04 is **done**, after independent corrective and final evidence acceptance under
T03's project/worktree-root scope. See [acceptance and limits](T04-acceptance.md).
The owner subsequently authorized disposable installed-client/model checks, another
agent's independent review, Docker-based Linux checks, task-only cleanup and source
commit/push. This does not authorize a release, registry upload or consumer activation.

Delivered files: new `host.py`, `native.py`, `lifecycle.py`, `transactions.py`; T02
staging/storage/task-identity and CLI integration; lifecycle/host/transaction/CLI
tests; distribution inventory; lifecycle usage, configuration-ownership ADR and
task handoff. Neutral operations now include complete install/update/exact connected
restore/status/verify/remove/recover without a per-consumer runtime or wrapper.

Independent review reproduced three defects and verified their fixes: revalidate
owned removal preimages, freeze/recheck modes during mutation/recovery, and retain
private backups/lock copies as owner-only `0400`. Regression tests preserve unknown
edits rather than repair them. Earlier artifacts, failures and seals remain retained.

Checks:

```sh
.venv-t04/bin/python -m unittest discover -s tests -p 'test_*.py' -v
AGENT_GUIDES_ARTIFACT_DIR="$PWD/.git/T04-retention-artifacts" .venv-t04/bin/python tests/check_distribution.py -v
.venv-t04/bin/python .git/t04_retention_review.py EXPECTED_RECORD_SHA256
.venv-t04/bin/python .git/t04_clients_retention_verify.py
git diff --check
```

macOS/Python 3.15.0: **73** source tests and **73** clean installed-wheel tests pass;
wheel built from sdist with exact resource/license checks. Linux arm64/Python 3.11.17
and 3.15.0: exact-wheel and rebuilt-distribution suites pass **73** cases each, with
one filesystem-specific skip. Outer Docker acknowledgments timed out after an
interruption; completed inner logs, retained artifacts and post-success result
records independently establish package checks, not a successful outer invocation.

Final installed macOS Claude Code 2.1.304 and OpenCode 2.1.0 cases confirm initial
short-entry delivery without duplication, relevant dependency reads before edits,
reuse, layer changes and local authority. Four turns per case share one resumed
session; managed OpenCode includes a real linked worktree. Diagnostic request capture
is local-only and separate from configured-model behavior. The first Claude folder
fixture lacked a native import; that failure remains recorded and final fixtures
include the native bridge before identity capture. Runner-input and sleep/API
interruption caveats are retained; no universal reliability/enforcement claim.

Exact identities/artifacts and source objects remain private in local Git metadata,
including `.git/T04-retention-review-expected.json`, `.git/T04-retention-artifacts/`,
`.git/T04-linux-retention/`, `.git/T04-client-retention/` and independent reports.
They are not uploaded by source publication. The final closure report is
`.git/T04-independent-closure-review.md`; never recapture its expected inputs for review.

Setup/acquisition and operation counts/timings were recorded without inventing
macOS Python/Git installation or another physical machine. Existing host provisioning,
future production-launcher binding, Linux native-model/TUI repetitions and consumer
guards are not claimed. No live snapshots or legacy runtime were deleted or migrated.

Next: **T05**, separately owned and with private access. T06 still requires T05;
T07/T08 remain pending. Future source publication and production actions require
their own authorization beyond this task's explicitly approved commit/push.
