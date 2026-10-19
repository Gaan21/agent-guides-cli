# T03 — Native loading feasibility

Status: done, owner accepted 2026-10-19. Depends on: T02 (done).
Completion: [accepted routes, limitations, evidence and T04 handoff](T03-acceptance.md).
The experimental records below retain their original criteria and dates; their
historical queues/statuses do not override the accepted root-started workflow.
Read [handoff](README.md), scope context behavior and technical-plan section 4.
Current direction: [ADR 0001](../decisions/0001-selective-guidance-reading.md) and
[the selective-reading continuation](T03-selective-reading.md). Historical strict
automatic-loader verdicts below do not override that prospective decision.

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
- Root-started work across two folder bindings, relevant topic/dependency selection,
  reuse and layer changes, relative paths, native local authority and import chains.
  Retain earlier subdirectory-launch observations without requiring that daily workflow.
- Local exceptions remain authoritative. Resume, compaction and interactive TUI;
  record when folder documents reload and any limitations of the native mechanism.
- Preserve unrelated guards. Inventory actual editing tools, including
  `apply_patch`; identify pre-existing guard failures separately from delivery.

## Acceptance / stop condition

Owner clarification (2026-10-18): root-started work should use model-selected,
relevant guide reads before applicable edits, reusing content still in context.
Hard edit prevention, all-topic loading and repeated per-patch reads are not
requirements. The earlier strict automatic-loading trials remain historical
evidence, not a rejection of this newly authorized behavioral route. See the
[selective-reading continuation](T03-selective-reading.md) for the current trial.

Specify one tested connection strategy per client, ownership surface and exact
loading observations. Establish native short-entry delivery separately from
model-selected topic reading; do not label an index as automatic scoped loading.
If the tested connection cannot establish the agreed selective behavior, stop with
a bounded gap report before T04 promises support.
No fallback daemon, injection plugin, hooks or global all-Markdown glob.

Keep reusable fixture logic in the tool tests. Consumer evidence is a one-time
acceptance record, not another maintained per-project probe. Keep private logs
private and distinguish host integrity from observed loading and compliance.

## Handoff

T04 is ready only when a feasible strategy and its limits are reviewed. Unavailable
TUI/client checks remain pending where not exercised, not simulated as passes.
The historical Claude approval correction and OpenCode automatic-loading gaps are
retained below; no complete two-client strategy is accepted. Follow the current
[selective-reading execution order](T03-selective-reading.md#next-agent-execution-order)
and [tested prerequisites](../native-loading.md). T04 remains pending until acceptance.

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

## OpenCode 2.0.32 diagnostic continuation — 2026-10-18

**Verdict: T03 blocked; T04 pending.** Owner requested continuation and testing the
new OpenCode generation. The official changelog and V2 installation documentation
identify **2.0.32**; V1's GitHub latest release and installed Homebrew formula still
identify **1.19.3**. V2 uses the separate `anomalyco/tap/opencode-v2` formula.

Installed-client arrangement:

- Downloaded the official versioned macOS arm64 standalone archive and matched its
  SHA-256 against the official formula before execution. The binary reports
  `opencode v2.0.32`. Platform: macOS **27.0.1 arm64**, Python **3.15.0**.
- Used disposable exact-byte replicas of the original archived fixture, isolated
  home/config/data/cache/state directories and `run --standalone`. Original source,
  engine, selection, policy expectations and all three historical seals are retained.
- The historical full verifier cannot rerun successfully: its original temporary
  roots no longer exist. Its failure is recorded, not repaired by replacing old
  paths or expectations. A new read-only review verifies all historical artifact
  inventories against archived handoffs, joins the original archived task and
  rechecks the key retained entry/edit-first, fresh-Claude-read and compaction records.
  This is bounded archival review, not a successful rerun of all historical joins.
- The new native candidate adds only exact short-entry `instructions` arrays in
  root/mobile/web configuration files. Its changed policy identity was retained
  independently before calls; source/engine/selection remain the original ones.
  Native files, source snapshots and protected bytes remain unchanged.

Observed request/tool matrix, separate from inference:

| Criterion | Navigation-only baseline | Native configured-entry candidate |
| --- | --- | --- |
| Root initial context | Root native directive, no entry content. | Root native policy plus exact root entry content. |
| Two subdirectory starts | Root/applicable-folder directives, no entry content. | Root/applicable-folder policies plus both exact entries; no topics or sibling entry. |
| First root-started mixed-scope edit | Actual `patch` succeeds before either folder policy is delivered. | Same failure; only the root entry was initially loaded. |
| Subsequent scoped reads | Each real `read` delivers the corresponding folder policy. | Same; folder configuration does not dynamically deliver its configured short entry. |

Eight invocations exited 0. A separately retained loopback provider supplied fixed
responses; the edit trials programmatically requested `patch`, then two `read`
calls. Captured requests show no folder policy even on the model request **after**
the successful patch; policies first appear after their corresponding reads.
This establishes actual installed-client composition and tool timing for the local
diagnostic arrangement, not configured OAuth equivalence, upstream inference or
model compliance. V2 native guard rejection, TUI, resume/compaction and Linux trials
remain unexercised; earlier V1 passes do not certify V2.

Evidence and checks:

- `.git/T03-v2-evidence/` retains original handoff bytes, source references, schema,
  binary identity, original/candidate task joins, pre-call diagnostic identities,
  commands, complete requests, outputs and durable replicas outside temporary storage.
- Read-only `.git/t03_v2_verify.py` checks the archived historical inventories,
  bounded historical observations, exact native startup entries, negative timing
  observations and both archived task identities. Capture/arrangement scripts are
  one-time evidence, not review commands. Exact invocations stay in
  `.git/T03-v2-results.md`; the new artifact inventory is retained independently.

```sh
python3 .git/t03_v2_verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -p test_identity.py -v
git diff --check
```

The read-only V2 verifier passes its bounded positive/negative observations and
retained identities, with final verdict **not accepted**. Python 3.15.0: **6 identity
tests passed**; `git diff --check` passed. Public changes are this record, the task
index and tested-prerequisite documentation; engine/package code is unchanged.

Next gate: review this V2 evidence and either establish a native strategy covering
root-started mixed-scope/edit-first delivery or retain the bounded infeasibility
decision. The tested configured-entry route resolves launch-time content only.
Pending Claude worktree approval/access and Linux prerequisites remain as above.
T05 is independently ready with private access; T04 still awaits T03 acceptance.

## Installed V2 mechanism and new candidates — 2026-10-18

**Verdict: bounded infeasibility remains; T03 blocked, T04 pending.** Queried the
actual executable rather than assuming the previous trial's version. The current
Homebrew-linked installation reports **2.0.32** and its binary SHA-256 equals the
previous official standalone binary. Exact path, resolved path, digest and commands
are retained privately. This is installed-version evidence, not release approval.

Review and mechanism:

- Ran the unchanged `.git/t03_v2_verify.py` before public edits: all bounded checks
  and its sealed inventory passed, final verdict **not accepted**. Historical missing
  temporary roots were not rebuilt; capture scripts were not rerun.
- Retained offset/digest-checked extracts from the actual executable. Its native
  config-instruction mechanism assembles ambient `AGENTS.md` and configured paths
  using the session Location. The read tool separately discovers `AGENTS.md` between
  a file/directory target and that Location; session history deduplicates these files.
  That discovery does not evaluate descendant configuration or parse Markdown imports.
- The exposed GPT editing tool is `patch`. Its implementation resolves targets,
  checks native edit permissions and mutates files without invoking that instruction
  discovery. Internal filesystem reads during patch preparation are not `read` tool
  discovery. Current V2 instruction/config/permission documentation corroborates the
  separate mechanisms; executable inspection and requests establish this version's
  bounded behavior, not universal impossibility in future clients.

New native candidates, separate from all original fixtures and identities:

| Candidate / control | Actual request and tool result |
| --- | --- |
| Exact configured entries, root-started first patch | Both scratch files created. Root entry only before/after patch; folder policies arrive after respective sample reads, without configured folder entries. |
| Root configured entry plus short entry bytes inline in each folder `AGENTS.md` | Same successful first patch without either folder policy/entry. Later scoped reads deliver policy and inline short entry together, without explicit instruction reads. |
| Same inline candidate, directory-read-first control | Each directory listing delivers its applicable policy/entry, before the later patch; no sibling entry before that sibling's listing. This is a diagnostic control, **not** automatic edit-first acceptance. |

Three accepted diagnostic invocations exited 0. Source/engine/selection are the
original ones. Each candidate has an independently retained pre-call task, binary,
observer, overlay, environment and exact planned calls. Native product instructions,
snapshots and protected bytes remain unchanged in the passing integrity joins.
The inline candidate adds short entry bytes only, not topics. Its relative topic
links would still require an explicit, separately recorded base-path transformation;
that was not implemented or accepted, because the edit-first blocker already persists.

An earlier exploratory invocation also edited a sample included in retained policy.
Its post-call identity join failed as expected for that mutation. The full attempt,
original identity and observer remain retained and **excluded** from the three
passing joins; no expectation was rewritten. Subsequent new fixtures only add
scratch files outside the retained policy inventory.

```sh
command -v opencode
opencode --version
opencode run --help
python3 .git/t03_v2_verify.py
python3 .git/t03_installed_verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -p test_identity.py -v
git diff --check
```

The new verifier passes archived original V2 seals, binary extracts, all three
candidate joins and positive/negative request observations. Python **3.15.0**:
**6 identity tests passed**; `git diff --check` passed. Commands, original handoff
bytes and new evidence are in `.git/T03-v2-installed-evidence/`; exact orchestration
and the independent new inventory are recorded in `.git/T03-v2-installed-results.md`.
After these public edits, review the old seal against its archived handoff using
the new verifier; the original verifier is unchanged and still expects old live docs.

All four client calls used scripted loopback responses: real native tool execution
and model-request composition only, **not OAuth equivalence or remote-model
compliance**. No configured remote model trial was needed to reject these routes.
V2 TUI/resume/compaction, permission rejection, Linux and Claude worktree-specific
acceptance remain pending. No enforcement claim follows from a loader observation.

What is missing: native target-scoped delivery of the applicable product policy and
short entry before a first root-started mutation, including multi-folder patches.
Startup paths, inline text discovered only by reads, advisory indexes and static
permissions do not supply that mechanism. Reopen with a concrete native client
capability/version and retain a new candidate identity; do not begin T04 or replace
the contract with model-directed reads, hooks/plugins or globally loaded scopes.
T05 remains independently ready. No staging, commits, pushes, publication, global
configuration/credential changes or consumer activation occurred.

## Selective-reading continuation — 2026-10-18

The owner explicitly accepts less than absolute model compliance and prioritizes
relevant, non-repeated reading over a hard editing gate. A root index with ordinary
topic links is being tested before introducing native skills or other machinery.
See [the trial and limits](T03-selective-reading.md). T03 returns to **in_progress**;
this does not accept the whole matrix or start T04. Original failures/seals remain.

Fresh root-started Claude Code 2.1.303/OpenCode V2 2.0.32 results, native TUI
compaction and remaining acceptance limits: [2026-10-19 continuation](T03-root-startup.md).
Subsequent [remaining checks](T03-remaining-checks.md) close exact-source-object and
explicit-settings worktree gaps; Linux infrastructure and owner acceptance remain.
