# T03 remaining checks — source objects and linked worktree

Status: historical trial record, 2026-10-19. Parent [T03](T03-native-loading.md) is done.
Current decision: [owner-accepted root-started strategy and T04 handoff](T03-acceptance.md).
Statuses below describe each trial's result before that closure, not today's board.
Extends the [root-started two-client trial](T03-root-startup.md). The owner requested
closing remaining tests unless they require disproportionate infrastructure/work.

## Exact source objects — checked

The original synthetic working-source directories are still absent. However, their
two exact recorded commits exist in an earlier retained Git object cache. Read-only
object identity checks, `git fsck`, complete bundle materialization and byte/hash
comparison confirm all three selected bundle snapshots against those commits.
No branch resolution, fetch, reconstructed source root or changed expectation was
needed. Independent review confirms this closes the missing Git-object comparison,
not recovery of the working directories or a new publisher-trust attestation.
The older reports accurately describe the evidence available at their dates.

## Claude linked-worktree import/access — checked with prerequisite

Tested installed Claude Code **2.1.303 / claude-opus-5-5**, macOS **27.0.1 arm64**, in
a new real nested linked worktree, without staging or creating any source commit.
Parent sentinel policies stay outside its attached instructions. Source, selection
and engine remain the exact prior task inputs; native policy/overlay candidates are
retained separately before calls and outside generated snapshot storage.

1. Before approval, a mobile-subdirectory start attaches its root/folder native
   policies and mobile local import, but omits external root-local/short-entry imports.
2. The native TUI presents worktree trust and the specific external imports. Approving
   the reviewed paths through that UI restores the six applicable memory files.
   No script edits native trust storage.
3. **The first topic-access trial fails:** despite those correct attachments, two
   linked topic reads are denied. Installed-client diagnostics show settings lookups
   for the current subdirectory/main checkout, not successful use of the worktree-root
   local read rule. Import approval does not grant topic access.
4. A separately retained native `--settings` candidate supplies the exact-selection
   `Read` allowance plus the unchanged existing deny rules. Fresh mobile and web starts
   each attach six applicable files and successfully read their sample, common topic
   and scoped topic. Parent policies, sibling entries and full topics are absent from
   initial attachments. No sibling-topic reads occur.
5. An unrelated root-sample `Read` is denied, and a protected-file `Write` is denied;
   original policies, snapshots and protected bytes remain unchanged.

This is a feasible **explicit-settings** worktree launch, not repaired automatic
worktree-root settings discovery. The allowance covers the exact selected snapshot,
not every root file; it does not make sibling topics confidential. Observed scope
selection is behavior, not a security boundary or system-level enforcement.
Ordinary project-root startup remains the selected workflow. T04 must preserve this
extra native prerequisite if it advertises subdirectory worktree support; no wrapper,
global configuration change or implicit broader access is justified by this trial.
Independent read-only review accepts these bounded source/worktree findings.

## Linux — pending infrastructure, not a pass

The Docker CLI is available, but its daemon socket is absent. No other authorized
Linux environment was identified. Running both installed Linux clients would require
an available Linux runtime, reviewed client installations and authorized model access.
No VM/service was started, remote host contacted or credentials transferred merely
to clear this test. Existing Linux package CI does not prove Linux client loading.
This is the remaining platform test requiring an owner infrastructure decision.

## Evidence, checks and handoff

Fresh private evidence: `.git/T03-finish-evidence/`; independent review:
`.git/T03-finish-independent-results.md`. Failed root-only worktree reads stay failed;
the new overlay does not replace their expectations. Earlier root-trial seals remain
unchanged, with pre-edit public handoffs archived for read-only review.

```sh
python3 .git/t03_finish_verify.py
```

The verifier checks the exact source objects, prior sealed evidence, both worktree
identities, actual attachments/read results and separate permission rejections.
Package/distribution checks use disposable copies and clean environments; they do
not execute a consumer or publish artifacts. Exact commands/results stay with the
private evidence. No package/engine implementation changed.

Python 3.15.0: the clean-distribution unittest passes, including sdist/wheel resource
checks, clean wheel installation and all **32** package unittests. An initial
source-only full-suite invocation failed CLI tests because isolated subprocesses
ignore `PYTHONPATH`; that failed invocation is retained, not a package regression or
a passing run. The installed-wheel repeat uses the intended test environment.

T03 remains in progress pending Linux disposition and owner acceptance of the bounded
strategy. T04 remains pending; T05 is independently ready with private access. No
staging, commits, pushes, registry/release publication or consumer activation.

## Linux factory-box trial — 2026-10-19 (review done; owner decision pending)

New Linux trial with its own identity; no macOS root or expectation was reconstructed.
Debian 13 x86_64, the VM that will run the factory. Both clients ran inside the factory's
own model sandbox, identities, root-managed policy and already-authorized credentials,
invoked as the factory roles invoke them. Claude Code **2.1.303** (newest changelog entry)
/ `claude-opus-5-5`; OpenCode V2 **2.0.32** (official binary matching the release lock;
latest endpoint) / `openai/gpt-6.1-sol`. New synthetic sources and selection; task identity
and expectations sealed seven minutes before the first call. Candidate: root `AGENTS.md`
carrying the short index, `CLAUDE.md` importing it, folder exceptions, ordinary topic links.

| Check | Claude Code | OpenCode V2 |
| --- | --- | --- |
| Native index at root start, no topics | PASS (transcript attachments) | FAIL in box: no native `AGENTS.md` |
| Dependency read before edit; reuse; new layer; no unrelated topic | PASS | PASS by model-initiated discovery |
| Resume across processes; compaction; fresh work | PASS; `/compact` in print mode | PASS; native TUI `/compact` |
| Factory-protected edit rejected natively | PASS | Diagnostic only; model stopped at a denied read |
| Linked worktree, root start, no parent instructions | PASS | PENDING (harness defect) |
| Worktree subdirectory start | FAIL: index import absent, rules missed | PENDING |

Findings and limits:

- The box sets `OPENCODE_DISABLE_PROJECT_CONFIG=1`. Outside-box local-provider
  attribution shows this flag alone suppresses V2's native root `AGENTS.md`; without it
  index and root policy arrive with no topic bodies. In the box the model found the index
  by its own glob/read. Factory integration needs an owner decision on delivery.
- OpenCode attempted the factory terminal tool four times despite the no-commands policy;
  it failed only because the tool socket was absent. This is a compliance miss.
- Claude's interactive first start fails its onboarding connectivity preflight in the box
  (`ECONNREFUSED`; missing IPv6 suspected, unverified). Owner chose the native `/compact`
  command in print mode; Claude TUI compaction on Linux and the worktree external-import
  approval UI remain pending. The later subdirectory run therefore had no approval.
- After compaction both clients still held the web guide verbatim. Fresh screen and
  dependency reads were observed; recovery after real loss of the web rule was not tested.
- Only managed policy applies in the box: project-level protection was ignored by both
  clients. Claude 2.1.303 warns that managed `Write(path)` denies are inert; `Edit` denies
  covered the rejection.
- OpenCode worktree runs are invalid: the sandbox sets `PWD` to its start directory and
  the harness changed only the working directory, so V2 used the parent checkout. An
  outside-box worktree diagnostic sent no provider request; inconclusive.
- Python 3.13.5: 32 unittests OK (one case-insensitive-filesystem skip) and the clean
  sdist/wheel distribution check OK. These are package checks, not client acceptance.
- The runner changed after sealing for the compaction route; the sealed copy is retained.

Independent read-only review confirmed these results and bounded Claude root-start
feasibility; it judged OpenCode in the box weakly supported. Private evidence, scripts,
manifest and review: `.git/T03-linux-evidence/`. T03 is not marked done; owner acceptance
and the OpenCode delivery decision remain. No staging, commits, pushes or activation.

### OpenCode V2 follow-up — index through factory-controlled `instructions`

Owner scope: factory agents always start at the project or worktree root; the Claude TUI and
subdirectory limits above stay documented and are not pursued. Operational box, wrapper,
root configuration and `OPENCODE_DISABLE_PROJECT_CONFIG=1` unchanged. Candidate C1:
`"instructions": ["{env:PWD}/AGENTS.md"]` in one root-owned, read-only config file passed
with `OPENCODE_CONFIG`; control C2 uses the absolute root path. Candidate bytes and
expectations sealed before any call; model turns gated on C1 diagnostics.

| Check | Project root | Real nested worktree root |
| --- | --- | --- |
| Index and root policy in initial request, no topics (local provider) | PASS | PASS, parent absent |
| Control C2 (absolute path) | loads root | loads parent instructions (rejected) |
| Guide and dependency before edit; reuse; repository and web layer changes | PASS | PASS |
| Native folder exception attached on entering `web/` | PASS | PASS (worktree file) |
| Parent checkout bytes and instructions untouched | — | PASS |
| Terminal attempts | 0 (not exercised) | 0 (not exercised) |

Limits: one configured-model run per case; delivery to the real provider is inferred from
behaviour (no read of the root `AGENTS.md`, guide chosen by exact name), while initial-request
content is captured with the local provider. C1 depends on `PWD` matching the start root;
the runner set it explicitly. Production requires changing root-owned factory configuration
or launcher environment, which needs separate owner authorization and its own verification.
Independent read-only review: PASS with these limits (`.git/T03-linux-evidence/`).
