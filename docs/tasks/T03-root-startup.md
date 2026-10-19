# T03 continuation — installed root-started clients

Status: historical trial record, 2026-10-19. Parent [T03](T03-native-loading.md) is done;
[owner acceptance and T04 handoff](T03-acceptance.md) supersede the pending gates below.
This extends the [selective-reading trial](T03-selective-reading.md), not T04.
Later [remaining checks](T03-remaining-checks.md) establish exact cached source-object
comparison and the explicit-settings Claude worktree route; Linux remains pending.

## Installed versions and arrangement

- Claude Code **2.1.303**, matching the newest entry in the official changelog at
  inspection; actual model **claude-opus-5-5**.
- OpenCode **V2 2.0.32**, actual model **openai/gpt-6.1-sol**. The installed command
  resolves to the separate Homebrew `opencode-v2` installation, not V1. A command
  name alone is not generation evidence; record its resolved binary and version.
- Platform: **macOS 27.0.1 arm64**, Python **3.15.0**. Linux remains untested.

Each client starts a fresh CLI process at a new disposable Git root, without a
subagent move or inherited conversation. One retained source/selection/engine/policy
identity covers both replicas, independently of their generated storage. Existing
prepared snapshots are copied unchanged; synthetic index/topics are a separately
retained policy candidate, not new upstream bundle content or a lifecycle install.
Original synthetic source Git roots remain unavailable: this verifies durable
prepared bytes and recorded commits, not a fresh comparison with original objects.

The small root index names four scoped topics. The screen topic links a required
text-consistency dependency that the ordinary task prompts do not identify.
Native folder exceptions and protected files remain separate from topic guidance.
No delivery hooks, skills, monitor, global configuration edits or live activation.

## Connection and observed behavior

Claude's root `CLAUDE.md` imports native root policy and the short index. Actual
transcript attachments show those three files before the first tool, without topic
or sibling-scope bodies. These are user-role project instructions, not system-level
enforcement. OpenCode uses native root `AGENTS.md` plus one configured
`instructions` path to the same index. A separately identified local diagnostic
captures that exact index once in the initial request, without topic/folder bodies.
This diagnostic establishes loader composition, **not** the remote OAuth request.
Configured remote-model traces separately establish the following behavior:

| Work in the same conversation | Claude Code | OpenCode V2 |
| --- | --- | --- |
| First screen title change | Screen and linked dependency read before edit; matching accessibility label updated. | Same. |
| Second screen subtitle change | No new topic reads; matching accessibility hint updated. | Same; code reread, topics reused. |
| Switch to repository demo data | Repository topic read before edit; immutable record tuples produced. | Same. |
| Switch to web presentation | Web topic read before edit; matching document title and nearest-folder exception applied. | Same. |
| Unrelated viewmodel topic | Not read. | Not read. |
| Native TUI `/compact`, then fresh mobile title work | Actual compaction boundary; new successful screen/dependency reads before edit. | Actual compaction/summary; new successful screen/dependency reads before patch. |
| Subsequent web heading change | Correct output with retained/restored web guidance, no fresh topic read. | Correct output with retained web guidance, no fresh topic read. |

Each client completed six ordinary work turns, resuming the same session between
processes. Compaction does not imply every topic disappeared: Claude restores some
read results, and OpenCode retains recent context beside its summary. The web turn
is reuse, not proof of a new read or recovery from complete guidance loss. Both
mobile continuations do contain new successful model-initiated dependency reads.
These are small synthetic cases, not a population compliance rate or a long-task,
simultaneous mixed-layer, changed-guidance or full context-erasure trial.

## Guards, failures and evidence boundaries

- Claude's actual `Write` to a protected file is denied by native permissions.
  Ordinary mutations use `Edit`; protected bytes and retained policies stay intact.
- OpenCode's remote model refuses the protected edit without calling a mutation
  tool. That is instruction compliance, **not** a native guard rejection. A separate
  scripted local diagnostic invokes actual V2 `patch`, receives `Permission denied:
  edit`, and leaves protected bytes unchanged. Neither accepts consumer guards.
- Claude initially guessed two nonexistent code paths before reading the correct
  file. Those failed reads are retained, not counted as successful access.
- The first Claude TUI attempt exited at the default negative trust choice. A new
  retained attempt approved only the reviewed disposable fixture through the native
  UI and completed `/compact`. OpenCode compacted on its first TUI attempt.
- Both first TUI wrappers reported an error when sending another key to a closed
  PTY. Native logs/session boundaries, not wrapper exit status, establish compaction.
- Initial Claude transcript-path lookup missed the client's normalized directory
  name; later captures preserve the actual full transcript. One OpenCode capture
  overlapped the first recovery turn and is not an exclusive pre-turn snapshot.
  A query-string API capture failed; the separately retained `--param` capture
  supplies the complete final messages. Failed outputs were not overwritten.

Full prompts, commands, binary identities, pre-call expectations, per-turn tool
results, native transcripts, TUI logs and durable replicas stay local in
`.git/T03-root-evidence/`. One-time arrangement/capture scripts must not be rerun to
review them. Historical seals and pre-edit handoffs remain unchanged/archived.
This is not an exhaustive hermetic-config audit: process overrides are retained
separately, the isolated update-disable config is not in the shared task identity,
and the local diagnostic provider has its own independently retained overlay hash.

Read-only check:

```sh
python3 .git/t03_root_verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -p test_identity.py -v
git diff --check
```

The bounded verifier passes identity joins, read-before-edit/dependency timing,
reuse, outputs, compaction records and the separate guard observations. Six identity
unittests pass on Python 3.15.0. Package/engine code is unchanged.
Independent read-only review supports bounded macOS feasibility, finding no blocking
behavioral defect in this sequence. Its retained record is
`.git/T03-root-independent-results.md`; hashes establish integrity, not trust.

## Remaining decision and next handoff

Owner acceptance remains required before marking T03 done or starting T04.
At this trial's completion, Linux, worktree-specific Claude import/access and source
comparison were pending. The [follow-up](T03-remaining-checks.md) closes the two local
gaps with explicit limits; Linux infrastructure remains unavailable. Earlier V1
checks are not V2 acceptance.
T05 remains independently ready with private
access; T08 does not start from this synthetic trial. No staging, commit, push,
release, registry publication or consumer activation was performed.

Version/mechanism references: [Claude changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md),
[Claude memory](https://code.claude.com/docs/en/memory),
[OpenCode V2 instructions](https://opencode.ai/v2/docs/instructions) and
[compaction](https://opencode.ai/v2/docs/compaction). Installed observations, not
documentation alone, support the findings above.
