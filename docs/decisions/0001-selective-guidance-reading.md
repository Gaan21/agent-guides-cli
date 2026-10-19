# ADR 0001 — Selective guidance reading before stronger enforcement

Date: 2026-10-18. Status: accepted direction; bounded T03 feasibility accepted 2026-10-19.
Owner authorized this approach and lightweight observation. See the
[task board](../tasks/README.md) and [trial](../tasks/T03-selective-reading.md).

## Problem

Agents need the guidance relevant to their current work before editing that kind
of code. Having files installed does not prove they were delivered, read or applied.
Loading every guide wastes context; repeatedly reading the same guide before every
patch adds cost without necessarily improving decisions.

Earlier trials pursued automatic folder-instruction delivery even when the first
tool edits files. Installed-client observations found gaps. That strict gate was
not the owner's intended requirement: agents should choose relevant guides and
reuse what remains in context, with high practical compliance rather than absolute
enforcement at any cost. These are distinct goals; the old failures remain valid.

## Alternatives considered

| Alternative | Assessment |
| --- | --- |
| Load all scoped guides/topics at startup | Rejected: unnecessary context and unrelated scope rules. |
| Require reads before every patch | Rejected: avoidable repetition; patch count is not a relevance boundary. |
| Automatic nested native instructions alone | Useful when delivered, but observed timing does not ensure pre-edit topic reading. |
| Short native root entry plus ordinary topic links | Smallest current candidate; content authors define relevance and dependencies. |
| Native skills for topic discovery | Possible comparison if the simpler route proves insufficient; not needed yet. |
| Delivery hooks, injection plugins, daemon or custom guards | Not introduced; outside the selected delivery scope. Existing product guards remain independent. |

## Decision

Start sessions at the project root. Natively deliver a concise entry that describes
which selected local guides apply to which work. The model reads relevant topics
and their explicit dependencies before applicable edits. It consults new topics
when work changes scope/layer, and reuses guidance still available in context.
Context loss or changed guidance can justify another read; no per-patch reread is
required. Do not weaken a guide's rules or dependencies to improve reading counts.

The engine prepares, pins and verifies availability/integrity/owned registration;
authors maintain reading conditions. Root/folder product instructions and local
exceptions retain authority. Selection scope is not promoted by listing a bundle
at root. No new runtime, automatic consumer migration or global configuration is
authorized by this decision.

## Evidence and confidence

The following is the initial decision's evidence, not the final acceptance matrix.
Later macOS/Linux checks and owner acceptance are recorded in [T03 closure](../tasks/T03-acceptance.md).

Four small OpenCode subagent conversations used a real configured model. Each read
the screen guide before screen edits, reused it on a second turn, consulted the
repository guide when work changed layer, and did not read the viewmodel guide.
The first pair also followed redundant inherited navigation. A separately retained
single-index variant removed those extra topic reads in both repetitions.
Independent review inspected tool calls, timing, code outcomes and local identities.

This supports a candidate, not a population success rate or two-client acceptance.
The sample uses one model and a shared harness bootstrap followed by a fixture-root
move; clean startup, longer/dependent work, compaction and Claude behavior remain
to be checked. Original source Git objects were unavailable for a fresh comparison;
retained local identity/snapshot checks are not that missing source check.

## Observation and reconsideration

[T08](../tasks/T08-lightweight-observation.md) samples existing authorized client
traces, without a monitor or mandatory consumer probe. Distinguish relevant reads
before edits, late/omitted reads, irrelevant reads, useful reuse, justified rereads
and unknowns due to incomplete traces. A read shows content access, not comprehension
or correct application; review output separately.

Recurring material omissions, excessive reading or context-loss failures justify
reviewing entry wording and authored applicability first. Consider native skills
or a stricter mechanism only for an evidenced gap, with owner approval and a fresh
candidate identity. No arbitrary percentage or new enforcement system is approved.

## Consequences and public narrative

T03 is owner-accepted for project/worktree-root starts; [T04 is ready](../tasks/T04-lifecycle.md).
See [connection acceptance and retained limits](../tasks/T03-acceptance.md). Lifecycle integrity,
source pinning, content preservation, security guards and publication permissions
are unchanged. Observation can begin with an authorized T06 clone pilot and later
ordinary use; it is not a new prerequisite blocking lifecycle work or publication.
Concrete regressions still need explicit disposition before affected claims.

This record can support a later public post about the problem, alternatives,
experiments and simpler direction. Do not describe a prototype as a released or
guaranteed solution, or publish private paths, consumer traces/rules or credentials.
Drafting/posting on an external service is a separate action, not authorized here.
