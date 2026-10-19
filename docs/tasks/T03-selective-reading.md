# T03 continuation — selective reading

Status: historical trial record. Parent [T03](T03-native-loading.md) accepted 2026-10-19.
See [closure and T04 handoff](T03-acceptance.md); this is not a released integration.
Update 2026-10-19: [fresh root-started two-client trial](T03-root-startup.md)
extends the subagent evidence below; the later closure records owner acceptance.

## Owner-confirmed target

- Start work at the project root.
- Deliver a short entry that explains which local guides apply to which work.
- Let the model select and read applicable topics before editing that kind of code,
  including dependencies explicitly required by those topics.
- Reuse content still available in the conversation; do not require per-patch reads.
- Read newly applicable guidance when the task changes area or layer. After context
  loss or a guidance change, another read may be appropriate.
- Prefer high observed compliance with little unnecessary reading, not absolute
  enforcement purchased through global topic loading or extra runtime machinery.

This is consistent with the [scope's indexed, on-demand reading](../delivery-scope.md#context-behavior).
The rationale and reconsideration criteria are recorded in
[ADR 0001](../decisions/0001-selective-guidance-reading.md).
It prospectively replaces the strict edit-gate criterion, not the original failed
observations or their independently retained expectations. A root index is not
claimed to be automatic folder-policy delivery.

## Smallest candidate first

Use one concise root-native index, ordinary Markdown topic links and existing
read/edit tools. The index tells the agent to select relevant topics and reuse
already visible guidance. No new skills, hooks, injection plugins, wrappers, daemon,
global configuration or model credential changes are needed for this experiment.
Native skills remain an option to compare only if the simpler route proves weak.

## Disposable subagent experiment

OpenCode **2.0.32**, macOS arm64; four fresh `general` subagents using the actual
configured **openai/gpt-6.1-sol** model, not programmed loopback responses. Each
conversation receives three ordinary code-change requests, with no topic-file name
or hidden guide rule supplied in the task prompts:

1. A screen title change.
2. A second text change to the same screen, in the same conversation.
3. A repository demo-data change, without touching presentation or viewmodels.

The fixture has separate screen, viewmodel and repository guides. Guide-only rules
have observable code consequences, allowing review of both successful reads and
application without relying on the model's final claim. Code edits are outside the
retained policy inventory; all guidance/native policy and prepared source bytes
remain integrity-checked before and after the trial.

Two initial replicas preserve the historical fixture's folder-navigation block.
Both agents select the intended layer topics and avoid repeated topic reads, but
also read a prepared entry and a generic topic required by that inherited block.
These extra reads are retained, not reported as an unnecessary-reading pass.

Two separately retained simpler replicas keep native local exceptions but replace
that redundant navigation with the single root-index route. No original fixture
or snapshot is changed. These are a new policy candidate, not repaired expectations.

| Observed behavior | Initial pair | Simplified pair |
| --- | --- | --- |
| Screen guide read before first screen patch | 2/2 | 2/2 |
| Same screen guide reused, not reread on second turn | 2/2 | 2/2 |
| Repository guide first read on repository turn, before its patch | 2/2 | 2/2 |
| Viewmodel guide not read | 2/2 | 2/2 |
| No extra prepared entry/generic topic reads | 0/2 | 2/2 |
| Requested changes and guide-only rules applied | 2/2 | 2/2 |

The simplified pair uses exactly one screen-topic read and one repository-topic
read per three-turn conversation, with no viewmodel-topic read. Reading local
native policy or code to inspect it is not counted as an unrelated topic read.
The second screen edit may occur directly without another code read; this is not
a failure when the necessary guidance and file text remain available in context.

## Evidence and limits

Pre-call source/selection/engine/policy identities, synthetic entry/topic bytes,
original handoff bytes, exact task prompts, actual session/model metadata, full
tool results and before/after records stay in `.git/T03-selective-evidence/`.
Original V2 and installed-V2 seals are preserved. Independent review and read-only
verification must inspect actual calls/results, not final replies or a percentage
derived from two successful conversations.

Independent read-only review confirmed the four local retained-identity joins,
actual native index updates, topic selection, read-before-edit order, reuse and
file results, including the initial pair's extra reads. Original source Git fixture
directories are absent: recorded source identities and durable snapshot bytes are
checked locally, but fresh comparison against those original Git objects is
unavailable. No missing historical root was reconstructed to make a check pass.

```sh
python3 .git/t03_selective_verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -p test_identity.py -v
git diff --check
```

The read-only verifier passes archived old seals, all four local task joins,
observed model/tool timing, unchanged guidance and code outcomes. Python 3.15.0:
six identity tests passed; diff hygiene and public line/link/path checks passed.
Exact commands, limits, review and the independent new artifact inventory are
recorded in `.git/T03-selective-results.md`. Capture scripts are one-time evidence,
not commands to rerun for review. Engine/package code is unchanged. No staging,
commit, push, release, global-setting change or consumer activation was performed.

This is a small, easy synthetic test with one configured model. Subagents begin
with the harness bootstrap, then move their own session to the fixture root before
any project action. Native instruction updates are observed at that boundary;
this is not a new clean-CLI-startup or provider-request capture trial. Previously
proven startup loading remains separate evidence. No compaction, long task,
ambiguous dependency, mixed simultaneous layers, Claude Code or Linux behavioral
trial is included. Do not claim a population success rate or complete T03 acceptance.

## Next-agent execution order

Historical T03 trial order only. **Continue T04** using the
[accepted handoff](T03-acceptance.md#next-agent-execution-order), not this queue.

Steps 3–4 now have fresh bounded macOS results in the
[installed-client continuation](T03-root-startup.md). Review those before rerunning
trials. The [remaining-check continuation](T03-remaining-checks.md) subsequently
checks cached source objects and worktree prerequisites; Linux and final acceptance
remain pending.

1. Read ADR 0001, the task board and the independently reviewed records above. Check
   actual installed client versions again; do not assume prior versions are current.
2. Review the retained local evidence without rerunning capture scripts. The sealed
   historical verifier expects its original handoff bytes; after documentation
   alignment, use the archived-handoff review linked from the board. Evidence in
   local Git metadata does not travel with a clone/push. If absent, obtain authorized
   evidence or explicitly retain a fresh small trial; do not reconstruct old roots,
   replace expectations or claim old checks passed on that machine.
3. Keep the minimal entry. In new disposable fixtures, check actual root startup
   (not only a subagent move), a less-obvious explicit dependency, unrelated-guide
   avoidance, reuse and a new-layer task in both installed clients. Do not supply
   the expected guide paths/rules in the ordinary model task prompt.
4. Exercise resume/context loss/compaction with fresh applicable work. Distinguish
   legitimate recovery reads from unnecessary repetition; retain misses/unknowns
   and local-authority/guard observations separately. Complete required TUI and
   supported-platform checks or report their missing prerequisites honestly.
5. Present the bounded two-client strategy and remaining limits for independent
   review/owner acceptance. Do not infer full feasibility from the two clean runs,
   invent a percentage threshold or require an absolute edit gate. T04 starts only
   after T03 acceptance; T05 remains independently ready with private access.

[T08](T08-lightweight-observation.md) plans later observation alongside an authorized
T06 clone pilot and ordinary use. It does not block this feasibility decision or
authorize a monitoring implementation. No second delivery system is justified yet.
