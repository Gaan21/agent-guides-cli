# T04 — Lifecycle acceptance and next handoff

Status: done, independently accepted 2026-10-20. Parent: [T04](T04-lifecycle.md).
This record concerns neutral tooling and disposable root-started trials, not a
stable release, production-host change or consumer migration.

## Delivered contract

- One explicit install/update/connected-restore operation prepares immutable exact
  multi-source content, connects selected clients and verifies host integrity.
  Updates preserve selections; exact revision policies and offline restore never
  fall back to latest. Repeated install is a no-op, not an implicit update.
- Owned short entries, source-relative link rendition, scoped labels and local
  native authority remain separate from authored topic relevance/dependencies.
  No selector, delivery hook, daemon, mandatory reread or behavioral editing gate.
- Transaction journals retain before/after bytes and modes, recheck preimages and
  publish the portable lock last. Unknown bytes or permission edits stop mutation
  or recovery. Retained backup/lock copies are owner-only `0400`; active journals
  are `0600`. Individual renames are not multi-file atomicity.
- Remove touches verified owned integration only, preserving unrelated user bytes,
  source selections, prior versions and ignored storage. No automatic cache pruning,
  executable reinstall, legacy migration, permission widening or host repair.
- Task roles share independently retained source/selection/engine/policy/overlay
  and registration identities. Hashes prove integrity, not publisher trust or model
  compliance. Exact engine artifacts remain separate from content versions.

Usage and conflict handling: [lifecycle contract](../lifecycle.md).
Configuration ownership: [ADR 0002](../decisions/0002-native-config-ownership.md).

## Native routes and prerequisites

Start at the project/selected-worktree root. Claude imports the short entry, reusing
an existing shared `AGENTS.md` import when appropriate. Its native folder policies
need native `CLAUDE.md` imports where shared folder `AGENTS.md` is intended for it;
the package neither fabricates these policies nor promotes scoped rules globally.

OpenCode project discovery uses an empty native configuration slot, preserving all
existing JSONC bytes/comments. Both occupied slots or modified owned material require
explicit resolution, not an ad hoc parser, silent reserialization or ignored conflict.

Managed OpenCode uses an explicitly approved external read-only JSON configuration
with `{env:PWD}/AGENTS.md`, leaving discovery disabled. The operation checks actual
`cwd`, absolute `PWD` and `OPENCODE_CONFIG` against the selected root/configuration.
The package owns only the project entry; it never writes host settings or installs a
consumer launcher. Future production-launcher binding remains an operator prerequisite.

## Check matrix

| Environment | Exact-wheel and clean-distribution checks |
| --- | --- |
| macOS 27.0.1 arm64, Python 3.15.0 | 73 source tests and 73 clean installed-wheel tests pass. |
| Linux arm64 container, Python 3.11.17 | 73 installed-wheel tests and rebuilt-distribution suite pass; one filesystem-case alias test skipped. |
| Linux arm64 container, Python 3.15.0 | Same checks pass; the same filesystem-specific case skipped. |

Distribution builds the wheel **from sdist**, checks exact resources/licenses and
installs outside the checkout. Linux records contain completed inner checks, retained
artifacts and matching engine identities. Their outer Docker command acknowledgments
timed out after interruption; those transport failures remain recorded separately,
not silently turned into successful wrapper executions or repeated completed tests.

Installed macOS trials use Claude Code **2.1.304** / `claude-opus-5-5` and OpenCode
**2.1.0** / `openai/gpt-6.1-sol`. Four root-started cases cover both connection routes,
including a real OpenCode linked-worktree root. Each has four turns in one resumed
session: relevant topic/dependency reads before edits, reuse, repository/web layer
changes and guide-only rule application. No unrelated viewmodel reads are required.

Claude initial attachments establish short-entry delivery without duplicate imports.
OpenCode installed-loader request capture establishes one short index and no full
topics or parent-worktree sentinel at startup, using a **local diagnostic provider**.
Configured-model tool traces/output separately establish bounded reading/application;
the diagnostic is not real-provider/model evidence. No terminal-guard coverage follows
from zero terminal attempts. Consumer guards and interactive acceptance remain T06.
Inherited-stdin runner text and a native sleep/API interruption remain recorded.
Neither supplied the hidden guide rules, but the trials are not clean prompt-only
benchmarks or evidence of uninterrupted operation.

## Review, retention and setup

Independent review found and reproduced three preservation defects: a removal capture
race, recovery ignoring tightened modes, and overly readable retained preimages. All
three have regression coverage and independent corrective acceptance. Final closure
review also accepted the exact final artifacts and refreshed client/platform evidence,
with the recorded interruption/input caveats. No implementation blocker remains.

Original failed/prototype inputs, exact source objects, independently retained expected
identities and artifact bytes remain in local Git metadata. Final packet locations:
`.git/T04-retention-evidence/`, `.git/T04-retention-review-expected.json`,
`.git/T04-retention-artifacts/`, `.git/T04-linux-retention/`,
`.git/T04-client-retention/`, `.git/T04-independent-retention-review.md` and
`.git/T04-independent-closure-review.md`.
Detailed results stay private; they are **not included by a source push**. A fresh
checkout must obtain authorized evidence or retain a new trial, not claim local checks
from this summary. Earlier Claude trials lacking a native folder import remain recorded;
final fixtures provided it before identity capture and inference, not after grading.

Setup inventory: Python/Git were already available on macOS; a fresh reusable tools
environment and exact wheel installation were measured. Linux records measure Git,
environment/build-tool and exact wheel acquisition with pinned Python base images.
With these prerequisites, install/update/restore/remove are each one operation plus
at most one restart per selected client. Managed host provisioning is explicit, not
hidden in a wrapper. Synthetic timings are not a production or second-machine benchmark.

## Limits and next task

This is bounded root-start acceptance under [T03](T03-acceptance.md), not guaranteed
topic delivery before every edit or perfect future model compliance. Native clients
were not rerun on Linux, nor were TUI/compaction feasibility experiments repeated.
Those observations are not inferred from Linux engine tests; T03's accepted limits
remain intact. Production integration, another physical machine, current consumer
guards, migration and stable-release claims require their separate authorized checks.

Next ready work is [T05 — content split](T05-content-split.md), in an independently
owned workspace with private access. T06 remains pending T05; T07/T08 remain pending.
Do not delete the legacy runtime or activate a consumer as cleanup. Source commit/push
is owner-authorized for this task only; releases/registry publication and future
production actions still require their own authorization.
