# T03 — Native loading feasibility

Status: blocked. Depends on: T02 (done). Executor: authorized installed-client agent.
Read [handoff](README.md), scope context behavior and technical-plan section 4.

## Goal

Select and demonstrate a minimal native connection in the actual installed Claude
Code and OpenCode versions before implementing permanent integration mechanics.

## Arrangement

Use prepared neutral bundles and a disposable clone/fixture with realistic local
instructions, two directory scopes and existing guards. Retain one source/engine/
selection/policy identity for implementation and review. No live consumer migration,
global changes or model/credential use outside authorized access.

## Checks

- Inspect actual entry attachment/context, not just the generated file or model
  recall. Record client versions, entry bytes and no duplicate old adapter block.
- Only short entries load initially. Topic reading instructions stay authored
  beside guides; detailed local links work without loading every document globally.
- Root and two folder bindings, root/subdirectory launches, mixed-scope work,
  relative paths, native ancestor precedence and existing import chains.
- Local exceptions remain authoritative. Resume, compaction and interactive TUI;
  record when folder documents reload and any limitations of the native mechanism.
- Preserve unrelated guards. Inventory actual editing tools, including
  `apply_patch`; identify pre-existing guard failures separately from delivery.

## Acceptance / stop condition

Specify one tested connection strategy per client, ownership surface and exact
loading observations. If automatic directory scope or first-turn entry delivery
cannot be established, stop with a bounded gap report before T04 promises support.
A root index describing directory scope is not proof of native scoped loading.
No fallback daemon, injection plugin, hooks or global all-Markdown glob.

Keep reusable fixture logic in the tool tests. Consumer evidence is a one-time
acceptance record, not another maintained per-project probe. Keep private logs
private and distinguish host integrity from observed loading and compliance.

## Handoff

T04 is ready only when a feasible strategy and its limits are reviewed. Unavailable
TUI/client checks remain pending where not exercised, not simulated as passes.
The original Claude subdirectory-start gap is resolved by native approval and bounded
read access. Independent review and supplemental trials below confirm OpenCode
initial-entry/edit-first gaps; no two-client strategy is accepted. See the
[tested prerequisites](../native-loading.md). T04 remains pending until acceptance.

## Bounded feasibility record — 2026-10-17

**Historical verdict: stop before T04; no accepted connection strategy yet.** The
corrective record below supersedes the diagnosis of the subdirectory-start gap.
Owner authorized
both installed clients with configured model access in disposable fixtures. Tested
macOS 27.0.1 arm64, Claude Code **2.1.302** / `claude-opus-5-5` and OpenCode
**1.19.3** / `openai/gpt-6.1-sol`. Linux client acceptance remains pending.

Arrangement and identity:

- Added `tests/native_fixture.py`: reusable offline restoration of an already pinned
  neutral selection, root plus `mobile/` and `web/` bridges, local import/exception
  files, sample files and protected bytes. It runs no clients or source commands.
- Restored T02's exact two-source/three-bundle selection without resolving branches.
  Captured engine, source, selection, all native/configuration policies and empty
  overlays once, outside generated storage, before client calls. The isolated
  external disposable Git root joins that same identity as the retained fixture.
- Exact commands, task identity, entry bytes, transcripts, exports and diagnostic
  logs stay in `.git/T03-evidence/`; orchestration and the read-only verifier stay
  in `.git/t03_run.py` and `.git/t03_verify.py`. Preserve these expectations for
  independent review; do not rerun the one-time arrangement/capture script.
- Candidate ownership: one short marked block per root/folder `CLAUDE.md` importing
  the prepared entry; one per `AGENTS.md` directing an explicit local entry read.
  All six native files are 338–382 bytes, with exactly one owned block each.
  Snapshot bytes remain unchanged. Synthetic config restricts command/network/task
  tools; no delivery hooks/plugins or global configuration edits were introduced.

Observed loading, separately from model reports:

| Check | Claude Code | OpenCode |
| --- | --- | --- |
| Root launch | Transcript `instructions` attachment includes root policy, local import and short prepared entry before the first tool call; no topics or folder entries initially. | Model reports the root native directive; entry/topic reads are visible tool calls. Initial attached context is not independently established by the retained export. |
| Mixed-scope reads | Transcript `nested_memory` attachments deliver each folder policy, local import and prepared entry after scoped sample reads. Topics are explicit later reads. | Read responses and `metadata.loaded` show native `mobile/AGENTS.md` and `web/AGENTS.md` reminders. Prepared entries/topics are explicit reads; the model also explicitly read both folder policies earlier. |
| Subdirectory launch | Root/mobile policies and mobile local import attach, but **neither prepared entry nor root local import attaches initially**. | Both policies are reported; root/mobile entries and topics read successfully. Initial-context evidence remains incomplete. |
| Subdirectory plus root access | `--add-dir` permits explicit entry/topic reads but **does not restore missing initial imports**. | Not needed for the observed local reads. |
| Resume | Same session resumes and reads succeed; no new folder attachments observed in retained transcript. | Same session resumes; read responses have empty `metadata.loaded`, retaining prior context rather than reattaching. |

The Claude subdirectory gap is established from actual attachment records, not
recall or generated files. The initial don't-ask subdirectory run also denied an
entry read outside its working directory; the explicit-root-access trial separates
that permission boundary from the persisting native-import gap. Do not describe
explicit reading as automatic first-turn imported-entry delivery.

Checks executed (exact interpreter, paths, arguments and outputs retained privately):

```sh
claude --version
claude --help
opencode --version
opencode --help
opencode debug --help
opencode run --help
opencode export --help
"$TOOLS315/bin/python" .git/t03_run.py claude root2
"$TOOLS315/bin/python" .git/t03_run.py opencode root2
"$TOOLS315/bin/python" .git/t03_run.py claude mobile
"$TOOLS315/bin/python" .git/t03_run.py opencode mobile
"$TOOLS315/bin/python" .git/t03_run.py claude resume
"$TOOLS315/bin/python" .git/t03_run.py opencode resume
"$TOOLS315/bin/python" .git/t03_run.py claude mobile-add-root
"$TOOLS315/bin/python" .git/t03_verify.py
"$TOOLS315/bin/python" -m unittest discover -s tests -p test_identity.py -v
git diff --check
```

- Python 3.15.0: **6 identity unittests passed**. Host verification confirms retained
  engine inputs, both roots joining the same task, unchanged policies/protected
  bytes and one owned block per native file. These checks do not certify loading.
- Seven corrected client invocations exited 0; the subdirectory permission denial
  is still a failed acceptance observation. Earlier setup attempts are retained and
  excluded: malformed empty Claude MCP configuration, and OpenCode inheriting the
  harness working-directory environment instead of the fixture. Corrected runs use
  explicit directory selection and matching process working-directory environment.
- Tool inventory is bounded: Claude was explicitly restricted to Read/Edit/Write;
  OpenCode exposed `apply_patch`. No edit-tool guard rejection was exercised. Native
  logs also flag Claude's redundant `Write(path)` deny syntax as unsupported; its
  `Edit(path)` deny rule is the relevant file-edit rule. This is fixture guard
  evidence, not a consumer guard regression or coverage claim.

Remaining gate / next handoff:

- Reproduce and resolve the Claude subdirectory initial-import gap with an
  installed-version-supported native arrangement, preserving local import chains.
  A narrow path-scoped-rule candidate remains untested; do not add a runtime fallback.
  Retain a new explicitly named candidate policy/overlay identity if changing bridges;
  keep the original failed expectations and exact source/engine selection.
- Obtain actual OpenCode initial-context evidence. Complete independent review,
  compaction, interactive TUI, edit-trigger timing/guard coverage, conflicting local
  precedence and nested-worktree checks. These are pending at this bounded stop,
  not unavailable-client passes or inferred support.
- T03 remains **blocked** and T04 **pending**. T05 remains independently ready.
  No consumer migration, staging, commit, push or publication was performed.

## Native approval and read-access correction — 2026-10-17

**The original Claude blocker is resolved; T03 is `in_progress`, not done.** The
cause was the client's documented external-import approval boundary, not incorrect
relative-path resolution. Imports outside the starting directory are external even
inside the same repository. `--add-dir` permits reads but does not approve imports.
The prior noninteractive runs never completed that separate native approval.

No engine or bridge changes were needed. An exact-byte disposable replica reproduced
the missing imports, then interactive native approval restored all six expected
root/folder instruction attachments before any tool call. Approval in `mobile/`
also applied to a new `web/` session in that repository. Both starts attached their
own short entry and the root entry, with both local imports and no detailed topics
or sibling entry. The TUI `/context` Memory files list corroborates these records.

A second, separately pinned native-policy candidate addresses unattended topic
access: one `Read` allow rule for the exact prepared selection in project-local
`.claude/settings.local.json`, without an edit allowance or `--add-dir`. Root/folder
sample and linked-topic reads succeeded from both scopes; an unrelated root-file
read remained denied. The original project guards and snapshot bytes are unchanged.
Local settings must be enabled; deny/ask policies retain their normal authority.
See [tested prerequisites and ownership limits](../native-loading.md).

Evidence and verification:

- Same installed Claude Code 2.1.302 / `claude-opus-5-5`, macOS arm64 / Python 3.15.0.
  Source, engine and selection remain exactly those retained before the original
  spike; no branch resolution or original expectation replacement occurred.
- `.git/T03-r2-evidence/` independently retains the original task, a new read-access
  policy/overlay task, before/after command outputs, full attachment transcripts,
  TUI approval/context/compaction logs and the prior public handoff bytes. Exact
  identities and command expansions are in `.git/T03-r2-results.md`. These are local
  evidence, not public consumer logs. Import approval used the native UI; no script
  edited global settings or client trust storage. The client persisted its decision.
- Read-only `.git/t03_r2_verify.py` verifies original artifact hashes (using archived
  historical handoff bytes), unchanged engine/helper/source/selection, corrected
  policy identity, six initial attachments per scope without topics, successful
  topic reads, bounded read rejection and an actual native `compact_boundary`.
- Resumed the corrected subdirectory session in the interactive TUI, ran `/context`
  and `/compact`, then resumed noninteractively. The transcript confirms applicable
  entries reattach after compaction. Independent review found that the original
  continuation restored sample/topic results without new reads; the supplemental
  turn below supplies fresh-read evidence. A model's report of extra policy
  reads is not by itself evidence of new model-initiated reads; inspect tool calls
  and restored-context records separately.
- An initial web topic test chose the root sample instead of the requested scoped
  sample, which was denied. The explicit web-path repeat passed. This was model
  path selection, not a broader read allowance or a loader change.

```sh
"$TOOLS315/bin/python" .git/t03_r2_run.py claude mobile-pre
"$TOOLS315/bin/python" .git/t03_tui.py approval --r2 --approve
"$TOOLS315/bin/python" .git/t03_r2_run.py claude mobile-post
"$TOOLS315/bin/python" .git/t03_r2_run.py claude web-after-mobile
"$TOOLS315/bin/python" .git/t03_r2_verify.py
git diff --check
```

The exclusively created arrangement/access/capture scripts are historical, not
commands to rerun for review. Expanded topic/boundary/TUI/resume commands and their
exact prompts are retained with their outputs; rerunning would create new evidence.
Original failing expectations and their diagnosis remain available for comparison.

Next handoff: independently review the corrected Claude candidate. Complete actual
OpenCode initial-context proof and its compaction/TUI checks, edit-trigger/guard
coverage, conflicting local authority and nested-worktree checks. Linux installed
client acceptance remains pending. The generic fixture's scoped-read timing is not
proof of coverage for every edit tool. **T04 remains pending**, and T05 independently
ready. This correction authorizes no consumer activation or publication.

## Independent review and supplemental matrix — 2026-10-17

**Verdict: T03 blocked; T04 pending until acceptance.** The Claude import/read-access
correction is independently verified, with a corrected post-compaction claim.
The OpenCode navigation candidate does not meet the agreed entry/scope contract.
These are feasibility findings, not a completed integration or consumer activation.

Review and retained identity:

- Ran the unchanged read-only `.git/t03_r2_verify.py` before public edits; it passed.
  Independently inspected initial attachments, native request records, tool results,
  permission rejections, TUI context and the real `compact_boundary`.
- Found no new `Read` calls after that retained compaction boundary: the client
  restored prior read results and the model described them as new reads. Initial
  reattachment and compaction remain proven. A new continuation of the **same**
  session now contains three actual successful `Read` calls: scoped sample and
  both linked topics, with no explicit policy/entry reads.
- Kept original/corrective seals, task expectations, engine, exact source commits,
  bundle snapshots and selection unchanged. New evidence is in `.git/T03-r3-evidence/`;
  corrective public handoff bytes were archived before documentation changes.
  `.git/t03_r3_verify.py` checks both historical seals against those archives and
  verifies all current task joins without recapturing expectations.
- Added `tests/native_matrix.py` for disposable exact-byte replicas and an explicitly
  conflicting local-policy variant. That variant has its own retained policy task;
  source/engine/selection match the original. A real nested, unborn Git worktree
  joins the original task; it required no staging or source commit. Diagnostic
  provider/telemetry settings and one exact-file CLI allowance were retained before
  their calls, independently of prepared files. No snapshot was edited.

Installed versions remain Claude Code **2.1.302** / `claude-opus-5-5`, OpenCode
**1.19.3** / `openai/gpt-6.1-sol`, on macOS **27.0.1 arm64**. No Linux client was available.

| Criterion | Claude Code | OpenCode |
| --- | --- | --- |
| Root and two subdirectory starts | Corrected root/folder entries and local imports attach initially after native approval; topics/sibling entry absent. | Installed-client loopback requests contain root/applicable-folder `AGENTS.md`, once each; prepared entry **content absent**. Configured OAuth request's full initial system context remains unobserved. |
| Relative entry/topic navigation | Existing imports and successful scoped sample/two-topic reads independently verified. | Configured-model root/mixed/mobile/web trials explicitly read the applicable entries and relative topics successfully. |
| Mixed-scope automatic loading | Existing read-triggered nested attachments retained; conflicting-policy trial attaches both folders and their local imports. | Fresh sample reads attach both folder reminders without explicit native-file reads. This is read-triggered loading. |
| First editing tool timing | With an exact-file native `Edit` allowance, first `Write` succeeds, then folder attachments arrive before the next `Read`. No before-write enforcement claim. | First `apply_patch` successfully adds files in both scopes with **no folder attachment**; only later reads attach scope policies. **Fail.** |
| Native authority / precedence | Root/mobile/web conflicting local values attach and the observed reply preserves each nearest exception. | Conflicting values delivered in native root/folder policies; observed reply applies nearest-folder exceptions. Behavioral evidence, not guaranteed enforcement. |
| Resume / compaction / TUI | Corrected TUI/context/boundary retained; new same-session continuation proves fresh topic reads. | Actual TUI `/compact` produces native compaction and summary records. Same-session sample reads reattach folder policies; ordinary prior resume deduplicates them. |
| Existing guards / editing inventory | Actual `Edit` and `Write` protected-file rejections; exposed tools restricted to Read/Edit/Write. Initial no-op Edit fails input validation, not a guard pass. | Actual `apply_patch` rejected by existing native `edit` deny rule; protected bytes unchanged. It is the exposed editing tool in these runs. |
| Import chains / duplicates | Existing local `@` chains and one owned block preserved. | `AGENTS.md` selected instead of stacking `CLAUDE.md`; prepared files are explicit reads, not `@` imports. Native blocks unchanged, no duplicate routes. |
| Nested-worktree boundary | Root imports attach inside the new worktree, excluding parent policies. Subdirectory start again needs external-import approval; that worktree's interactive approval/access trial remains pending. | Root/two subdirectory request captures exclude parent-worktree policies; configured-model mixed reads use policies inside the worktree. |
| Platform / independent acceptance | macOS observations reviewed as above; Linux client trial unavailable. | macOS supplemental evidence retained for review; Linux client trial unavailable. No complete two-client acceptance. |

Observation limits and exclusions:

- OpenCode's configured-auth telemetry omitted system instructions; `/context` was
  not an installed TUI command. Those exploratory attempts are retained, not counted
  as initial-context passes. Loopback request capture uses the real installed loader
  with a separately recorded local provider and fixed response: it proves request
  composition for that diagnostic arrangement, **not upstream inference or OAuth
  request equivalence**. Real configured-model trials establish the tool observations.
- Large CLI exports truncated stdout; retained native session API responses establish
  compaction/summary records. The partial exports remain available, not repaired or
  substituted in place. Post-compaction OpenCode made a topic-path typo; its explicit
  corrected read passed with the same selection.
- Claude's first default-policy scratch write was denied. A `Write(path)` allowance
  was also unsupported; the installed native `Edit(path)` permission family allowed
  the exact scratch write. These are permission-arrangement findings, separate from
  loader timing. No global settings, trust storage, hooks or delivery plugins were
  edited. Synthetic guard observations do not accept a consumer's guard correction;
  that independent consumer verification remains T06's responsibility.

Checks (full argv, prompts, cwd, results and identities retained privately):

```sh
"$TOOLS315/bin/python" .git/t03_r2_verify.py
"$TOOLS315/bin/python" .git/t03_r3_verify.py
"$TOOLS315/bin/python" -m unittest discover -s tests -p test_identity.py -v
git diff --check
```

The read-only supplemental verifier passes integrity, archived evidence and all
stated positive/negative observations; its final verdict is **not accepted**.
Targeted identity checks: **6 passed each** on available Python **3.11.14, 3.14.8
and 3.15.0** environments (18 executions); `git diff --check` passed.
Public changes: this record, task index, tested-prerequisite documentation and the
shared replica helper. Exact check outputs and supplemental artifact inventory stay
in local Git metadata. Source and native bridge bytes remain unchanged.

Next gate: independently review the supplemental matrix, then establish a native
OpenCode strategy that delivers initial authored entries and covers edit-first
directory work, or retain the bounded infeasibility decision. No advisory index,
hook/plugin injection or global all-topic glob substitutes for these criteria.
Exercise the pending worktree-specific Claude prerequisites and Linux clients before
claiming those cases supported. **T04 stays pending until T03 acceptance; T05 stays
independently ready.** No staging, commit, push, publication or consumer migration
was performed.
