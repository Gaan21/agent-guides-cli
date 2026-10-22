# T06 — WorkTracker acceptance and explicit migration

Status: in_progress (clone pilot run). Depends on: T03 + T04 + T05.
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
