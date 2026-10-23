# T06 pilot 004 — model ladder findings (2026-10-23)

Status: evidence for owner/next-agent analysis, **not** T06 acceptance or a decision.
Read with the [T06 task](T06-migration.md), [ADR 0001](../decisions/0001-selective-guidance-reading.md)
and the [client-compatibility procedure](../client-compatibility.md). Exact traces,
diffs, identities, consumer rules and the blind-review key are private evidence in
the product catalog (`evidence/T06/pilot-004/`, start at its `HANDOFF.md`).

## What was authorized and run

- Independent review of the consumer guard port, a corrected guard candidate and a
  second review; read-only inventory of the managed factory VM (no sudo, no change).
- Real-model native TUI sessions in disposable consumer clones, driven by the agent
  in a PTY: first task, exit/resume + layer switch, native compaction, post-loss
  task, Supabase task. Owner login, project-only settings, client default effort,
  production MCP disabled, inert local `supabase` stand-in, no Git remote.
- Each model ran a **guided** arm (retained eight-bundle selection, exact native
  index) and a **control** arm (no guide delivery; the consumer's own local
  instructions and the same prompts). Expectations were sealed before traces
  (reused from pilot 002, plus a pilot-004 addendum).
- Not done: product test/lint execution or corrections (owner reserved T06 step 4),
  Flutter/dependency updates, live consumer/factory changes, release or activation.

## Versions and advisories (checked 2026-10-23)

| Item | Tested | Official channel |
| --- | --- | --- |
| Claude Code | 2.1.309 | npm `latest`/`next` 2.1.309; npm `stable` 2.1.308 (owner chose 2.1.309 for its sandbox/permission fixes) |
| OpenCode V2 | 2.1.4 | V2 update channel 2.1.4 |
| Node / isolated Python | 24.22.1 / 3.15.1 | current security releases |

Both clients exceed every patched version in their GitHub security advisories.
The managed factory VM (x86_64) ran one patch behind on both clients; Mac and
arm64 results do not transfer to it automatically.

## Reading behaviour (guided arms; distinct guide topics opened before first edit)

| Model (client) | A domain+test | B presentation | C after compaction | D Supabase |
| --- | --- | --- | --- | --- |
| Haiku 5.5 (Claude) | 0 | 0 | 0 | 0 |
| Sonnet 5.5 (Claude) | 0 | 0 | 0 | 0 |
| Opus 5.5 (Claude) | 0 | 0 | 0 | 0 |
| GPT-6 Luna (OpenCode) | 4 common Flutter | 5 incl. UI/time-copy | 4 (reread after loss) | 0 |
| GPT-6.1 Sol (OpenCode) | 0 | 2 (UI, time-copy) | 0 | 0 |

- Claude's client `/context` showed the full 12.8k-token index loaded once; models
  still opened no topic files and relied on the index entries plus local folder
  instructions. The pilot-002 Opus session (2.1.308, low effort) also opened none.
- Only Luna followed the intended pattern (relevant common topics before edits,
  layer switch, reread after native compaction). No model opened the product
  bundle's topics or the Supabase topics.
- Token use was similar between arms (1.5–5.1M cached input per session).

## Applied quality (blind static review of product diffs; max 8 = 4 tasks × 2)

| Model | Guided | Control |
| --- | --- | --- |
| Haiku 5.5 | 8 | 7 — localized plural used an invalid placeholder; number never shown |
| Sonnet 5.5 | 8 | 8 |
| Opus 5.5 | 8 | 8 |
| GPT-6 Luna | 8 | 6 — unrequested always-visible UI; migration named after an unrelated task |
| GPT-6.1 Sol | 8 | 8 |

The reviewer did not know arm or model; the key was revealed only afterwards.
Tasks A/C were correct everywhere; all deductions were in B (presentation and
localization) or D naming. No new lint ignores, structural SQL or remote commands.
The review was static: nothing was compiled, tested or linted.

## Guard and safety results

- Review 001 accepted the V2 guard port as a bounded diagnostic, with one HIGH
  finding: the OpenCode V2 `patch` grammar differs from the inspector it reused.
- Candidate 002 fixed four shapes and non-object inputs. Review 002 rejected it as
  a complete `patch` guard: nine crafted shapes still pass under static emulation
  of the 2.1.4 parser. None is ordinary model output; none was run natively.
- Owner decision: keep blocking new ignores with candidate 002, stop emulating the
  client grammar, and add a **review-time check over resulting files** that lists
  new ignore directives relative to the base for explicit approval. Adding it to
  the consumer is a separate authorization.
- No guard fired in any model session; no session called Supabase. The guards were
  not exercised by real models, only shown not to obstruct normal work.
- Factory inventory: the role PATH lacked `jq`, and the consumer's shell guard
  helpers allow everything without `jq` (inherited finding). Plausible, not confirmed
  for role users. The factory also had admission stopped and no engine installed.

## Harness lessons (retained as failed attempts privately)

- macOS `$TMPDIR` is a symlink; the engine correctly rejects it. Resolve paths first.
- The selection identity includes the client set; install the same clients.
- A completion marker in the prompt must not be detectable in the echoed prompt;
  a comma-tolerant screen match ended turns early and interrupted two sessions,
  which were repeated from fresh clones. Use the client's own turn-end record
  (OpenCode `idle` message) rather than screen text.
- `opencode api ... --param` ignores query parameters on raw paths; in-run exports
  held only the newest 50 messages (also true of earlier pilots' OpenCode exports).
  Page with the URL query (`limit` ≤ 200, `cursor`) afterwards.
- Native compaction completion should be confirmed from session records, not
  screen wording.

## External context: Anthropic on harnesses

Official posts argue that harness parts encode assumptions about what a model
cannot do and should be removed one at a time when measurements show they are
dead weight ([harness design](https://www.anthropic.com/research/harness-design-long-running-apps),
[Managed Agents](https://www.anthropic.com/research/managed-agents)); single prompt
lines can measurably hurt quality ([postmortem](https://www.anthropic.com/research/april-23-postmortem));
start minimal and load context just in time ([context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)).
Deterministic boundaries stay required for high-impact actions
([containment](https://www.anthropic.com/research/how-we-contain-claude)). A staff
post on [Claude 5 context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/)
reports removing most of Claude Code's system prompt without measured loss and
recommends lightweight entries with files loaded when needed (domain ownership not
independently verified; one quantitative claim, no published method).

## Open question for the next agent: keep, shrink or remove the guides?

Not decided. One session per arm/model is an observation, not a rate; the review
was static. Options to analyse with the owner:

1. **Keep index + detail topics (current).** For: both cheap-model controls lost
   points while their guided arms did not; Luna used topics as designed. Against:
   Claude never opened topics, so detail files cost maintenance without observed use.
2. **Index/summary only.** For: Claude's guided arms matched the best scores while
   reading only the index; simpler. Against: untested for OpenCode and cheap models;
   rules absent from entries would disappear in practice; T05 coverage must be kept.
3. **Remove guide delivery (local instructions only).** For: mid/high models scored
   the same without guides. Against: cheap-model controls regressed; loses common
   rules for the factory's mixed model roster.

Owner direction for the next measurement (2026-10-23; needs its own authorization):
keep this pilot's approach — sealed expectations, guided/control arms, blind review,
**one pass per model tier** — and run it as a **complete factory cycle** on the
managed factory, adding an "index entries only, no topic files" arm. Measure the
factory's deterministic lint/test/build/i18n results on the first candidate, rounds
to green, reviewer findings and consumption per arm. Linters cannot see every rule
(behaviour, naming conventions), so keep the blind review alongside them; the result
also shows which guide rules the linters already enforce. Prerequisites are tracked
in the factory repository. Do not count a read as compliance, and keep guard and
coverage checks separate from reading results.

## Pending for T06

Step 4 (product tests/lint, effective T05 coverage) reserved by the owner; factory
controlled trial (x86_64, current clients, `jq`, mirrors/deploy key) needs specific
authorization; consumer adoption of the review-time ignore check; live migration
with rollback only after acceptance. T07/T08 order and T05 deferred follow-ups are
unchanged.
