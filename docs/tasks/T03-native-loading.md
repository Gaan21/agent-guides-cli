# T03 — Native loading feasibility

Status: in_progress. Depends on: T02 (done). Executor: authorized installed-client agent.
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
The original subdirectory-start gap is resolved by native approval and bounded read
access; remaining matrix checks and independent acceptance are pending. See the
[tested prerequisites](../native-loading.md) and the corrective record below.

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
  entries reattach after compaction; subsequent scoped sample/topic reads succeed.
  Compaction also restores prior read context. A model's report of extra policy
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
