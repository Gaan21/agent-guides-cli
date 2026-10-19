# T03 — Accepted feasibility and T04 handoff

Status: done, owner accepted 2026-10-19. Parent: [T03](T03-native-loading.md).
Next task: [T04 — lifecycle and recovery](T04-lifecycle.md), ready, not started.
This accepts bounded feasibility, not an installed integration or stable release.

## Accepted workflow and connection

Start each agent at the **project root or the root of its selected worktree**, with
the process working directory and `PWD` identifying that same root. Deliver only a
short native index; the model selects applicable guides and explicit dependencies,
reuses content still in context and reads new topics when work changes layers.
No automatic pre-edit folder injection, all-topic startup load or per-patch reread
is promised. This is the direction in [ADR 0001](../decisions/0001-selective-guidance-reading.md).

| Client | Accepted native route | Boundary |
| --- | --- | --- |
| Claude Code | Root `CLAUDE.md` imports the short index; shared `AGENTS.md` can contain it. | Preserve product root/folder instructions and native import/permission authority. Project instructions are user-role context, not system-level enforcement. |
| OpenCode V2 | Native `instructions` supplies the short index alongside applicable native policies. | A managed host that disables project configuration needs an explicitly approved host-controlled route; model discovery is not a substitute. |

The Linux managed-host candidate retains `OPENCODE_DISABLE_PROJECT_CONFIG=1` and
passes a host-controlled, read-only configuration through `OPENCODE_CONFIG`:

```json
{"instructions": ["{env:PWD}/AGENTS.md"]}
```

That exact candidate works at both project and real nested-worktree roots. An
absolute path fixed to the parent checkout is rejected: it loads the parent's
instructions when starting in a worktree. `PWD` was explicitly set by the trial
runner; correct binding by the actual production launcher is **not yet proven**.
Missing/stale `PWD` can silently select no index or the wrong one. T04 must treat
root identity and entry availability as host prerequisites, not assume them from
the environment variable or delegate them to the model.

The tested host-controlled overlay does not authorize replacing live host settings.
Choosing an owned registration in existing host configuration versus an approved
native config supplied by the host remains an integration/ownership decision.
Do not add a per-consumer wrapper, widen permissions or enable arbitrary project
configuration to make this route work.

## Evidence and acceptance basis

- **macOS 27.0.1 arm64:** installed Claude Code **2.1.303**, model
  `claude-opus-5-5`; OpenCode **V2 2.0.32**, model `openai/gpt-6.1-sol`.
- **Debian 13 x86_64:** the same client versions and models, exercised in a
  managed model sandbox using authorized model access. These are tested versions,
  not a claim about future versions or stable-release approval.
- Fresh root-started sessions show relevant guide/dependency reads before edits,
  reuse, repository/web layer changes, no unrelated viewmodel topic and application
  of guide-only rules. Native folder authority and parent/worktree separation have
  bounded observed evidence. The corrected Linux OpenCode candidate passes both
  root cases, one configured-model run per case.
- Claude native attachments establish initial index loading. OpenCode initial
  request composition is captured with a local diagnostic provider; delivery to
  the real configured provider is inferred from observed behavior, not a captured
  real-provider system prompt. Diagnostic responses are not remote-model evidence.
- Repeated processes resume the same session. Actual compaction and fresh screen/
  dependency reads are observed. Recent web guidance remained/restored in context;
  reuse is not proof of web-rule loss and recovery.
- Exact retained original Git objects match all three earlier prepared bundles.
  Missing historical working-source directories were not recreated. The Linux
  trials retain their own source/task identities rather than reconstruct macOS runs.
- Independent read-only reviews support the bounded macOS findings, source/worktree
  checks, Linux Claude root route and corrected Linux OpenCode candidate. The owner
  now accepts this root-start scope and authorizes documentation commit/push only.

## Explicit exclusions and retained failures

- Subdirectory startup is outside the accepted workflow. Linux Claude subdirectory
  starts omitted the root-index import and missed rules. Its interactive TUI failed
  a connectivity preflight; the cause was not established. Linux Claude compaction
  was exercised with native `/compact` in print mode, **not** the TUI. Neither case
  is relabeled passing or required to reopen this accepted root-start decision.
- Earlier Linux OpenCode worktree runs were invalid because of stale `PWD`; the
  separately sealed corrected candidate supplies the valid root-worktree result.
  The earlier navigation-only startup failure remains a failure.
- Native managed protections rejected bounded protected operations. Project-level
  permission rules were not authoritative under the managed host policy. Guidance
  cannot supply permissions or repair ignored guard rules.
- Earlier forbidden terminal attempts remain compliance misses. Zero attempts in
  the corrected candidate are **not** a protection/compliance pass: that tool was
  not exercised and may not have been offered. Consumer guard acceptance stays in
  T06; no universal tool coverage, bypass resistance or model compliance is claimed.
- Tiny synthetic trials with one model per client do not establish a population
  success rate, long-task reliability or an absolute editing gate.

## Checks, records and publication boundary

Python **3.15.0/macOS**: clean sdist/wheel resources, clean installation and all
**32** unittests pass. Linux **Python 3.13.5**: the same suite/distribution checks
pass, with one case-insensitive-filesystem test skipped. Earlier source-only CLI
test failures and failed client/PTY attempts remain recorded, not erased.

Private evidence stays in local Git metadata: `.git/T03-root-evidence/`,
`.git/T03-finish-evidence/`, `.git/T03-linux-evidence/` and their independent review
records/manifests. Local closure review/check results are under
`.git/T03-close-evidence/`; read-only checker: `.git/t03_close_checks.py`.
Historical seals are checked against their original archived handoff bytes, not
rewritten to fit this closure. Evidence is **not uploaded by the documentation push**.
On another checkout, obtain authorized evidence or retain new trials; do not claim
old local checks passed merely from this public summary.

Public changes are the task board, this acceptance record, T03 evidence summaries,
T04 handoff, scope/technical-plan alignment and native-loading/ADR status. No engine
or package behavior changed. This session's commit/push authorization does not
authorize a release, registry publication, production configuration, migration,
consumer activation or deletion of retained evidence.

## Next-agent execution order

1. Inspect status/diff, read the task board, this acceptance, scope, ADR and T04.
   Continue **T04**, not the historical T03 experiment queues. T05 can run separately
   with private access. T08 still needs an authorized T06 pilot; it is not a gate.
2. Pin one task identity and inspect T02 preparation/ownership primitives. Design
   the smallest transactional install/update/restore/status/verify/remove path.
3. Preserve existing root/folder policies, exact selections and host-managed controls.
   Implement/report root/`PWD` prerequisites and owned short-index registration;
   do not silently mutate a managed host or introduce a consumer-specific launcher.
4. Test lifecycle faults, recovery, user edits, ownership/removal and clean packaging
   per T04. Confirm actual installed-client behavior when integration changes the
   tested route. Keep host integrity, native loading and behavior separate.
5. Report remaining operator actions and measured setup/restart steps. T04 may
   implement neutral tooling; applying it to the live managed host/consumer requires
   separate authorization and verification. Do not start T06 migration or publish.
