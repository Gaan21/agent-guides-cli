# T06 — WorkTracker acceptance and explicit migration

Status: in_progress (pilot 002 corrections and disposable-clone rerun). Depends on: T03 + T04 + T05.
Executor: WorkTracker agent with owner-authorized client and migration access.
Read [handoff](README.md), preceding evidence and current consumer instructions.

## Goal

Demonstrate the complete experience with the approved common technology/topic
selection and the private WorkTracker product bundle, then migrate the live project
only under explicit authorization with a tested rollback path. Other private product
bundles are not implicitly selected or migrated.

## Work and acceptance

- Trial the actual neutral package and recorded common/private sources in a
  disposable consumer clone first. Retain one exact engine/source/bundle/local
  policy/overlay/config task identity for implementer and reviewer.
- Measure first install, another-machine preparation, explicit update, daily use,
  verification, recovery and removal. Distinguish temporary-root portability tests
  from a physical second-machine trial; do not invent that evidence.
- Test an update with actual changed guidance, an interrupted update, config edits
  before removal, complete prepared offline use and recovery to the old selection.
- Observe first-turn entry, no duplicate delivery, detail links, local authority,
  two scopes, resume, compaction and interactive TUI in both clients.
- Start ordinary tasks at root. Observe model-selected relevant topics and explicit
  dependencies before applicable edits, reuse on subsequent changes, and newly
  relevant reads after a layer switch or context loss. Compare against expected
  applicability retained before trace review; include a task with an irrelevant
  neighboring guide. Do not force all-topic or repeated per-patch reads.
- Separate host integrity, native delivery, successful content reads and reviewed
  application. Record late/omitted reads, unnecessary reading and unknowns honestly;
  no claim of perfect enforcement or inferred population success rate.
- Verify the consumer correction for the earlier `apply_patch` guard gap separately
  with its owner; reuse its acceptance evidence and check for relevant regressions.
  Preserving plugin bytes or a passing smoke command is not full guard acceptance.
- Check T05's complete requirement coverage in effective delivery, not just bundle
  presence. No guide disappears through migration or selection changes.
  Every rule must remain available in its proper scope; each task need not load
  every guide. Preserve authored dependencies and local exceptions.
- Before live change, identify old installed/legacy adapters and ignored state;
  prepare version-appropriate disconnection and full rollback instructions. Do not
  edit a live old snapshot or remove its only working tools environment.
- If authorized, disconnect old delivery, connect the exact new selection, restart
  clients and repeat acceptance without double injection. Retain originals and
  rollback until success is reviewed.

## Legacy retirement

Only after the migration above is reviewed, and each step separately authorized:

1. Mark `flutter-agent-guidelines` deprecated with successors (`agent-guides-cli`,
   `agent-guides`), as was done for `dev-guidelines`; keep its rollback instructions.
2. Archive it on GitHub (read-only). Do not delete it: exact recorded commits must
   stay restorable for rollback and historical restore.
3. `dev-guidelines` stays as is until its remaining non-Flutter consumers have
   successor bundles in `agent-guides` and are migrated; then archive, not delete.

## Completion rule

If only the clone trial is authorized/completed, report that milestone and keep
live migration pending. Failed guard, TUI or delivery checks must remain visible.
Public records contain a sanitized outcome only; all consumer logs, rules and
coverage maps stay in private evidence. Mark T07 ready only after required
acceptance and migration review. [T08](T08-lightweight-observation.md) may start with
an authorized clone pilot and reuse existing traces, but is not a new completion
dependency. Concrete delivery/behavior failures still require owner/reviewer
disposition; observation is not permission to ignore them or activate live capture.
Completion evidence: pending.

## Clone pilot checkpoint — 2026-10-22

Owner-authorized disposable consumer clone; no live checkout, consumer commit or
activation changed. Exact identities, traces, expectations (sealed before traces),
the consumer patch and the live migration/rollback procedure are private evidence.

- **Engine:** private HTTPS sources failed because Git runs without credentials by
  design. Added `--mirror SOURCE=PATH` (bare copy whose origin equals the approved URL;
  lock keeps only URL + commit). Independent review: accept after corrections; 79/79
  installed-wheel tests and distribution check on macOS/Python 3.15. Not committed.
- **Consumer preflight:** the engine refused while root instructions named the legacy
  package or the generated index path. The consumer change rewrote the delivery and
  guidance-source lines and added a read-before-applicable-edits rule the models saw.
- **Host:** first install ~5 s; temporary-root portability and offline restore; real
  guidance update through a refreshed mirror (a stale mirror silently keeps the old
  commit); offline rollback; owned-config edits block removal; user bytes kept.
  `kill -9` mid-write → refusal until recovery → exact old selection. **Failed/limited:**
  every kill leaves two abandoned empty writer locks that block all operations,
  including `recover`, until an operator removes them; the local Git cache records the
  mirror path (lock and records do not).
- **Clients (Claude Code 2.1.308, OpenCode 2.1.3, root start, one `.` scope):** Claude's
  own context report shows the index once (~13k tokens); for OpenCode only the resolved
  configuration was checked, not observed loading. Model behavior is separate: both read
  relevant guides before edits, reused them across a layer switch and skipped an
  irrelevant neighboring stack. Claude omitted required topics (including testing) and
  made no fresh reads after compaction whose summary kept only topic names; OpenCode
  read the required topics plus many unnecessary ones. Non-interactive OpenCode `/compact` is not native compaction. Edits were not
  built, tested or reviewed.
- **Rollback rehearsal:** remove + instruction revert restores the exact consumer tree;
  legacy reconnect/disconnect with its own tool; reinstall gives the identical selection.
- **Guards:** consumer smoke suites pass with the new delivery (regression check only,
  not the guard owner's acceptance).
- **Independent evidence review:** accepted with corrections as a bounded clone-pilot
  milestone; corrections applied.

Pending: interactive TUI (both clients, native compaction, post-loss reads), OpenCode
initial-request capture, two scopes, detail links and local-authority precedence, T05
coverage in effective delivery, guard-owner acceptance, product-edit review, daily use,
Linux, physical second machine, owner disposition of read omissions and lock recovery,
engine commit/push, and separately authorized live migration.

### Follow-up before the next pilot run

Owner decision: record fixes for every failed or weak result; another agent implements
them later and repeats the pilot. T06 stays `in_progress`. Detailed table: private
evidence `FOLLOW-UP.md`. In short:

- Engine: lock holder identity so `recover` can clear locks of dead processes; report
  unchanged sources and mirror freshness; no mirror path in the cache; detect real
  imports instead of prose mentions; measure index size; test other-owner mirrors.
- Content: unmissable routes for common tests/layers/UI; reread after compaction;
  narrower "read when" conditions; optional sibling repositories.
- Consumer/factory: owner review of the instruction patch and of a production MCP
  enabled by default; factory mirrors and deploy key.
- Re-run with the missing checks listed above.

## Pilot 002 continuation — 2026-10-22

Owner authorized development fixes, independent review, a second disposable-clone
pilot with both clients, and scoped develop uploads in the three guidance
repositories. Live migration, production access and factory changes are not
authorized. Detailed identities, expectations, policies and traces stay private.

- Engine E1–E5 corrections received bounded independent acceptance after corrective
  passes: process-identity lock recovery, source/mirror diagnostics, receipt-path
  prevention, syntax-based registration inspection and neutral index measurement.
- An exact archived source tree produced the retained wheel/sdist; distribution
  checks and all 102 installed-wheel tests pass on macOS/Python 3.15.0, with the same
  wheel passing 102 tests each on Python 3.13.9, 3.12.12 and 3.11.14. Python 3.14
  was unavailable. These establish package/host behavior only.
- C1–C4 content corrections received independent preservation/privacy/lint-impact
  review. Clear routes, actual-text rereads, conditional reading and optional sibling
  locations preserve substantive rules; no lint or architecture policy was relaxed.
- Disposable host checks pass for changed/stale mirror updates, no recorded mirror
  path, explicit recovery after resolution/fetch/write cuts without manual lock
  deletion, offline use, edited-config refusal and exact tracked-tree rollback.
  Fresh-root portability is not a physical second-machine trial. The legacy tools
  environment was not used or changed by this continuation.
- Installed OpenCode's local-provider initial-request diagnostic observes the exact
  native index once. This is loading evidence, not remote-model compliance.

Owner requested a pause for the session's remaining budget; **pilot 002 is partial,
not accepted**. Both native TUIs completed a first task; OpenCode also resumed for
a layer switch. Claude's client-generated context report lists one index; detailed
trace/application review is incomplete. Failed harness attempts remain preserved.

New acceptance blockers: actual OpenCode guard plugins fail to load (legacy plugin
API), despite passing smoke tests; focused product tests stop before assertions on
missing disposable assets, and one edited test set fails the required local lint
checkpoint despite a passing final gate. No guard port, suppression or live-consumer
change was made. Obtain guard-owner disposition before more OpenCode model turns.

Pilot-specific additive coverage proof reconciles changed Flutter destinations and
native policy availability, but full compound/native/external requirement coverage
is still unproved. Historical expectations and their failures remain unchanged.
Detailed counts, logs, identities, exact pending turns and commands are retained in
the private pilot-002 `HANDOFF.md`; do not recreate seals or resolve newer sources
for its review. No model processes were left running.

Pending: native compaction/post-loss, remaining client turns, full trace/detail/local
authority/application review, product validation fixes, complete coverage, other-owner
mirrors/Linux (Docker unavailable), guard-owner acceptance, daily use, physical second
machine and separately authorized/reviewed live migration. T06 stays
`in_progress`; T07/T08 status and task order are unchanged. T05's
[deferred follow-ups](T05-content-split.md#handoff) remain low priority.
