# T02 — Exact multi-source preparation

Status: done (independent corrective review accepted; refreshed CI matrix passed).
Depends on: T01 (done; independent review accepted).
Executor: agent in the neutral tool repository.
Read [handoff](README.md), scope, technical-plan sections 1–3 and phase-1 tests.

## Goal

Deliver a non-activating vertical slice: prepare selected bundles from Git, record
one portable selection, restore the same bytes and verify against an independently
retained expected identity. No native connection in this task.

## Work

- Define/test the smallest versioned bundle schema: ID, entry, explicit files and
  notices. Whole self-contained bundles; ordinary local links; no nested modules,
  profiles, source dependency graph or cross-bundle reference protocol.
- Select multiple repositories and several bundles from one source. Directory
  bindings belong in the project selection, not duplicated in bundle metadata.
- Resolve approved channels once per source, then acquire exact commits. An
  explicit exact revision takes precedence. Restore never resolves a branch.
- Preserve source bytes and topology, validate local targets, and leave external
  documentation links untouched. No execution of commands supplied by sources.
- Prepare immutable content off to the side; one portable lock records source,
  bundles, bindings and integrity. Do not embed machine paths or credentials.
- Retain exact prepared bytes/cache for offline restoration. Missing required
  objects produce an actionable error without changing existing selection.
- Establish host task evidence including engine, selection, local policy and
  overlays shared by implementer/reviewer; no session lifecycle manager.

## Acceptance

Use `unittest` with controlled disposable Git fixtures:

- Two sources; multiple bundles sharing one resolved commit; moved branches after
  preparation do not alter restore or review. Count resolver invocations.
- Restore offline into another temporary project root from prepared data; same
  portable identity. Missing cache fails without an implicit network/latest fallback.
- Reject unsafe source/path/ref, link escapes, symlinks/submodules, case collisions,
  undeclared/missing/extra/tampered files, altered inventory/expected identity and
  unsupported schema. Bound inputs without inventing a content interpreter.
- Match role identities; changed engine/policy/overlay is visible as a mismatch.
- Build/install the neutral wheel/sdist cleanly and run relevant checks outside
  checkout. Report macOS/Linux evidence separately.

## Handoff

Document the now-tested CLI/schema and fixture layout, distinguish content from
engine version, and mark T03/T05 ready after review. Preserve expected identity for
review. No claim of installed-client delivery. Completion evidence follows.

## Implementation record — 2026-10-17

### Delivered behavior and reuse

- Development engine `0.1.0.dev1`; documented schema/CLI/bounds in
  [preparation contract](../preparation.md). Added `integrity.py`, `storage.py`,
  `git_source.py`, `bundles.py`, `preparation.py`, `task_identity.py`; extended CLI,
  README, NOTICE and distribution checks. Added synthetic Git fixtures and
  preparation/rejection/role-identity/command tests. No runtime dependencies added.
- `prepare` resolves each approved source once (explicit revision wins), then
  acquires exact commits and complete bundles. One portable lock records sources,
  bundles/scopes, snapshot identities and independently versioned engine identity.
  Binding one bundle to several scopes reuses its exact source/snapshot.
- `restore` uses recorded data offline, without resolution/network; complete
  snapshots or cached exact objects suffice. Missing/tampered data fails without
  switching the existing selection. `verify` checks prepared local bytes against
  a supplied independent expected selection digest, without an acquisition cache.
- Staged, content-addressed snapshots preserve source bytes/topology/notices.
  Validation rejects undeclared/missing/extra/tampered files, unsafe paths/links,
  encoded escapes, symlink/executable/submodule modes, case collisions, duplicate
  identities/bindings, unsupported schemas and bounded-input violations. Lock
  publication checks its preimage; conflicting files/edits are preserved.
- `task-pin` exclusively retains source/bundle/selection/engine/root-policy and
  explicit extra-policy/overlay identity outside generated storage; `task-join`
  compares the same evidence for both roles. No task registry/lease/rebaseline.
- Audited legacy `snapshots`, `runtime_io`, `git_source` primitives before adapting
  canonical hashes, path checks, snapshot inventories, atomic writes and safe Git
  invocation/tree-mode handling. Exact audit source retained locally; Apache-2.0
  attribution/modification notice updated. No legacy runtime or Flutter payload
  imported. Existing consumers, snapshots and global settings were not changed.

### Checks and retained evidence

`TOOLS315` and `TOOLS314` below are new dedicated T02 environments; exact paths and
expansions are in `.git/T02-results.md`. `ARTIFACTS` is the separately created local
artifact directory, not the T01 directory.

```sh
"$TOOLS315/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS314/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
AGENT_GUIDES_ARTIFACT_DIR="$ARTIFACTS" "$TOOLS315/bin/python" tests/check_distribution.py -v
"$TOOLS314/bin/python" tests/check_distribution.py -v
"$TOOLS315/bin/python" .git/t02_review.py
git diff --check
```

- macOS 27.0.1 arm64, Python 3.15.0 and 3.14.8: **27 unittests passed per runtime**.
  Each runtime also passed 1 distribution unittest: sdist, wheel built from sdist,
  exact wheel resources/notices, clean installation, CLI help/version and all 27
  tests against the installed wheel outside checkout with isolated Python.
  Backend observed: build 1.6.1, setuptools 84.0.0, wheel 0.48.0; Git 2.54.0.
- Tests count source resolutions, move branches before acquisition/after prepare,
  restore to another root without network, reconstruct from exact cached objects,
  fail missing cache, compare both roles, and inject publication failure/concurrent
  edits. Cases cover altered inventory/expected identity, local policy/overlay and
  engine drift. Fixtures contain no product content or consumer commands.
- `.git/T02-identity.json` retains 26 engine/build/test/policy/document inputs plus
  exact audited source and the durable two-source trial's source, bundle, selection,
  policy and overlay identities. Created once before review, outside generated
  files. `.git/T02-results.md` identifies exact wheel/sdist bytes, hashes, trial
  roots and retained role record. Never recapture these expectations for review.
- The durable trial retains original selection/task evidence after both source
  branches moved; implementation/reviewer-role joins match on two temporary roots.
  This is an implementation self-check, **not independent T02 acceptance**.
  The retained sdist precedes this final completion-record update. The read-only
  review script checks source and artifact inputs against retained identity.
- T01 closure committed/pushed with explicit session authorization. T01 expected
  identity bytes/artifacts remain intact; its historical scaffold digests are not
  expected to match the new T02 engine. No T02 staging, commit or push performed.

### Limitations, blockers and next handoff

- **T02 remains open pending independent review and Linux/minimum-Python checks.**
  Python 3.11 is unavailable locally; Docker daemon connection failed. The existing
  CI matrix is the validation path after authorized T02 upload. Passing T01 CI
  does not establish new engine support. No installed-client or Windows checks.
- HTTPS-only credential-free locators; no SSH/local-folder import, tag selectors
  or automatic credential setup. Markdown validation is deliberately conservative,
  not a full HTML renderer; HTML navigation/unsupported inline syntax fail and
  fragment existence is not checked. Automatic native policy discovery is root-only;
  include nested/imported/configuration inputs explicitly. No exhaustive loader claim.
- Read-only files/host hashes do not establish publisher trust, a same-user sandbox,
  native loading, model compliance or stable-release approval. Full integration,
  journaled multi-file recovery and installed-client behavior remain later tasks.
- Next reviewer: inspect retained identity/results/artifacts before running checks;
  do not rerun `.git/t02_capture.py` or re-resolve sources. Record findings and the
  remaining matrix result. Only after acceptance mark T02 done and T03/T05 ready
  in both headers and board. T03/T05 remain pending now. Obtain authorization for
  source publication in future sessions; no release, PyPI publication or consumer activation.

### Source-upload authorization

After the local implementation record, the owner explicitly authorized T02 staging,
commit and push to `develop` to exercise CI. This authorizes source upload only;
the independent-review gate remains. Actual publication and CI results follow.

### Source publication and CI result — 2026-10-17

- Authorized T02 source committed and pushed to `origin/develop`; exact commit and
  publication checks are retained in `.git/T02-results.md`. Only the 20 intended
  implementation/test/contract/handoff files were staged; local identity/evidence
  and `.serena/` were excluded. Retained expected identity was not changed.
- [T02 CI run](https://github.com/Gaan21/agent-guides-cli/actions/runs/39087489115)
  passed all four macOS/Ubuntu × Python 3.11/3.15 jobs. Each ran 27 source tests,
  the distribution unittest (sdist then wheel from sdist, resources/notices,
  clean install), CLI help/version and 27 installed-wheel tests outside checkout.
  This supplies the previously pending Linux/minimum-Python implementation checks,
  distinct from T01 CI and local macOS checks.
- Observed with `gh run watch 39087489115 --repo Gaan21/agent-guides-cli --exit-status
  --interval 10` (exit 0). The run retains exact source/runtime details and logs.
  A documentation-only follow-up records results without changing tested engine,
  build, tests, policy or retained artifact identity.
- **Remaining closure gate: independent T02 review.** T02 stays `in_progress`;
  T03/T05 stay `pending`. The next reviewer compares the same expected identity,
  artifacts and actual implementation against Acceptance / Handoff, then records
  acceptance or exact findings. No new source resolution or expectation capture.
  Earlier local/pending-publication statements above are historical, superseded
  by this result. No releases, registry publication or consumer activation.

### Independent review — 2026-10-17

**Verdict: changes required; T02 remains open.** This subsequent reviewer inspected
the source, tests, preparation contract and retained evidence independently of the
implementation self-checks. T03/T05 remain `pending`.

Closure blockers (reproduced with disposable synthetic Git fixtures):

1. **Nested Markdown labels bypass local-target validation.** In
   `src/agent_guides/bundles.py:77–80`, both the extraction and unsupported-syntax
   checks assume labels contain no closing bracket. A link with label
   `[outer [inner]]` and destination `../../outside.md` is accepted unchecked.
   Full `prepare` accepts and publishes this changed bundle rather than rejecting
   it and preserving the prior lock. Direct validation also accepts the nested
   image label `![outer [inner]]` targeting `/absolute.png` and the nested link
   label targeting a `file:` URL. Validate these targets or explicitly
   reject unsupported nested-label syntax, with regression coverage for links and
   images and for preservation of the existing selection on rejection.
2. **Case aliases bypass independent-evidence placement.** In
   `src/agent_guides/task_identity.py:44–46`, the generated-storage exclusion uses
   lexical, case-sensitive path comparison. On the tested case-insensitive macOS
   filesystem, `.GUIDANCE` and `.guidance` identify the same directory, yet
   `retain(PROJECT/.GUIDANCE/review-task.json, ...)` succeeds inside generated
   storage. Reject filesystem-equivalent reserved paths and test case aliases on
   applicable filesystems, preserving exclusive creation and symlink rejection.

Checks and evidence:

```sh
"$TOOLS315/bin/python" .git/t02_review.py
"$TOOLS315/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS315/bin/python" .git/t02_independent_review.py
gh run view 39087489115 --repo Gaan21/agent-guides-cli --json conclusion,headSha,jobs,url
git diff --check
```

- Original 26 retained inputs match working source, HEAD and the CI-tested source;
  exact wheel/sdist hashes and archived input bytes match. Both retained synthetic
  project roots verify and join the same task; original T01 expected bytes match.
  The read-only script also passed 28 local-link and length/privacy checks.
- macOS 27.0.1 arm64 / Python 3.15.0: all **27 existing tests passed**. The two new
  independent acceptance probes **both failed** because the required rejections
  did not occur. Probes live in local Git metadata, leaving reviewed source/tests
  and retained artifacts unchanged. Expanded commands/results are in
  `.git/T02-independent-results.md`; original identity/results remain intact.
- Rechecked GitHub: all four original macOS/Ubuntu × Python 3.11/3.15 CI jobs
  succeeded on the retained implementation. Existing tests omit both reproduced
  cases; passing CI therefore does not close these findings. No new distribution
  rebuild or local Linux/3.11 run was needed to establish the blockers.
- Changed public files: this completion record and `docs/tasks/README.md`. No
  engine, source selection, expected identity, artifact or consumer changes.
  No installed-client/model-compliance or stable-release approval claim follows.

Next handoff: remediate both findings, including regression tests. Preserve original
T01/T02 evidence; retain a separate corrective-task identity before implementation
and new build artifacts for a subsequent independent review. Do not refresh the
original expectations to match fixes. Original CI covers only the reviewed engine.
Keep T02 `in_progress` and T03/T05 `pending` until independent acceptance. No staging,
commit, push, release, registry publication or consumer activation was performed
or authorized by this review.

### Corrective implementation for independent re-review — 2026-10-17

Both reported defects are corrected locally; **independent acceptance remains
pending**. Earlier review findings above describe the original engine. T02 stays
`in_progress`; T03/T05 stay `pending`.

Changed files and behavior:

- `src/agent_guides/bundles.py`: every inline destination opener must belong to a
  recognized link/image. Unsupported nested/escaped-bracket labels fail explicitly
  rather than hiding their targets from both extraction and rejection. Source
  bytes remain untransformed; a rejected candidate leaves the prior selection intact.
- `src/agent_guides/task_identity.py`: generated-storage names are reserved without
  case distinctions, using filesystem project identity to handle aliased project
  spelling. The same check protects retained records and policy/overlay inputs.
  Exclusive output creation and ancestor/leaf symlink rejection remain in place.
- `tests/test_rejection.py`, `tests/test_identity.py`: five new tests cover nested
  and escaped labels, links/images, escaping/absolute/unsupported/safe targets under
  unsupported labels, failed preparation preserving the lock/snapshot, reserved-name
  case variants, project-root aliases, and symlink preservation of unowned evidence.
  The filesystem-alias test skips on case-sensitive hosts; portable reserved-name
  rejection is exercised everywhere. Existing shared-role/exclusive-output tests pass.
- `docs/preparation.md` documents conservative syntax rejection and reserved case
  variants. This record and the task board carry the revised handoff.

Checks (`TOOLS315`/`TOOLS314` retain their earlier meanings):

```sh
"$TOOLS315/bin/python" -m unittest discover -s tests -p test_rejection.py -v
"$TOOLS315/bin/python" -m unittest discover -s tests -p test_identity.py -v
"$TOOLS315/bin/python" .git/t02_independent_review.py
"$TOOLS315/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS314/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
AGENT_GUIDES_ARTIFACT_DIR="$FIX_ARTIFACTS" "$TOOLS315/bin/python" tests/check_distribution.py -v
"$TOOLS314/bin/python" tests/check_distribution.py -v
"$TOOLS315/bin/python" .git/t02_fix_review.py
git diff --check
```

- macOS 27.0.1 arm64 / Python 3.15.0 and 3.14.8: **32 source tests passed per
  runtime**, plus 1 distribution unittest per runtime covering sdist, wheel from
  sdist, exact resources/notices, clean installation, CLI help/version and all 32
  installed-wheel tests outside checkout. The alias test ran, without skipping.
  Targeted suites passed 12 rejection and 6 identity tests; the two original review
  probes now pass. Backend: setuptools 84.0.0 / wheel 0.48.0.
- Before edits, exclusively retained `.git/T02-fix-start.json` over the initial
  source, policy, original exact source/bundle/selection/engine identity and empty
  corrective overlays. After checks, exclusively retained the corrected candidate
  in `.git/T02-fix-identity.json` and new exact artifacts in `.git/T02-fix-artifacts/`.
  Expanded commands/hashes/locations are in `.git/T02-fix-results.md`.
- A separate durable synthetic trial uses the original exact source commits and
  bundle snapshots, with a new engine/selection identity. No branch tip was queried.
  Both roles join one retained corrected task record on two roots offline. The
  read-only verifier checks 26 corrected inputs, archived bytes, original evidence/
  artifact integrity, shared roles, local links and length/privacy. Original
  T01/T02 expectations, records, artifacts and trial snapshots were not replaced.
- Development label remains `0.1.0.dev1`; engine byte identity changed. Old task
  selections require their original engine. This is no stable-release approval.
  Retained sdists precede this handoff-only update, with engine/tests/contract bytes
  matching the corrected candidate. No consumer/native-loading checks were performed.

Next handoff: independently inspect the corrected candidate against the retained
identity and exact artifacts; never recapture expectations to fit drift. Refreshed
Linux/Python 3.11 CI remains pending: original CI tests the old engine, and source
upload needs explicit authorization. Close T02 only after independent acceptance
and the refreshed matrix; then make T03/T05 ready. No staging, commit, push, release,
registry publication, global configuration change or consumer activation performed.

### Independent corrective review — 2026-10-17

**Verdict: corrective candidate accepted; refreshed CI remains the closure gate.**
The subsequent reviewer inspected both fixes, regression coverage, path primitives,
the preparation contract and retained verifier before running checks. Both original
findings are resolved: unsupported label destinations cannot evade the opener check;
reserved storage names use case-independent names and actual project identity for
retained evidence and policy/overlay inputs. No further blocking finding was found
in the corrective diff. Exclusive creation, symlink rejection and preservation of
the previous selection remain covered.

Independent checks:

```sh
"$TOOLS315/bin/python" .git/t02_fix_review.py
"$TOOLS315/bin/python" .git/t02_independent_review.py
"$TOOLS315/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$REVIEW311/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS315/bin/python" tests/check_distribution.py -v
TMPDIR="$REAL_TMP" DYLD_LIBRARY_PATH="$PY311_LIB" "$REVIEW311/bin/python" tests/check_distribution.py -v
git diff --check
```

- Read-only verification passed: 26 corrected inputs, exact retained wheel/sdist
  bytes, original evidence/artifact integrity, unchanged exact source/bundle commits,
  two offline roots joining one retained task, 28 local links and length/privacy.
  Neither capture script was rerun and no expected identity was replaced.
- macOS arm64 / Python 3.15.0 and 3.11.14: 32 source tests passed per runtime;
  both original independent probes passed. Each runtime passed the distribution
  unittest, including clean installation and 32 installed-wheel tests outside the
  checkout. Case-alias tests ran without skips. Prior 3.14 evidence is preserved.
- Initial 3.11 attempts exposed local environment setup issues: the uninstalled
  interpreter could not import the package; its copied venv executable could not
  locate libpython; the default temporary spelling traversed a system symlink.
  A dedicated editable environment, process-local library path and canonical
  temporary directory produced the passing result above, without source changes
  or relaxing symlink validation. Exact expansions/results are retained in
  `.git/T02-fix-independent-results.md`.
- Docker daemon was unavailable. GitHub's latest existing successful run still
  covered pre-fix source; Linux support for this candidate awaits refreshed CI.
- Owner explicitly authorized staging/commit/push of T02 to `origin/develop`,
  plus a documentation-only closure commit/push after passing CI. Upload results
  follow. T02 remains open and T03/T05 pending until the refreshed matrix passes.

### Final closure — 2026-10-17

**T02 accepted and done.** This result supersedes the historical pending gates
above. Independent corrective acceptance and the refreshed platform/runtime matrix
both cover the retained corrective engine, tests and preparation contract.

- Authorized corrective-source commit uploaded to `origin/develop`; exact execution
  revision is retained in `.git/T02-fix-independent-results.md`. The seven intended
  corrective/test/contract/handoff files were included; Git-local evidence and
  `.serena/` were excluded. Retained candidate/original identities remain unchanged.
- [Corrective CI run](https://github.com/Gaan21/agent-guides-cli/actions/runs/39097112478)
  **passed all four jobs**: macOS Python 3.11.9/3.15.0 and Ubuntu Python
  3.11.17/3.15.0. Each ran the 32-test source suite and the distribution unittest
  (sdist, wheel from sdist, exact resources/notices, clean install, CLI help/version
  and the 32-test installed-wheel suite outside checkout). Ubuntu appropriately
  skipped the one case-insensitive-filesystem alias test in each suite; macOS ran
  it. Portable reserved-name rejection passed on both platforms.
- Observed with `gh run watch 39097112478 --repo Gaan21/agent-guides-cli --exit-status
  --interval 10`, followed after the local watch timeout by `gh run view 39097112478
  --repo Gaan21/agent-guides-cli --json conclusion,headSha,jobs,url` and log inspection.
  Final conclusion and every job/required step were `success`.
- Closure changes only task documentation: this record, board and T03/T05 headers.
  Engine/build/tests/contract bytes remain those independently reviewed and tested.
  `git diff --check` and retained-candidate/local-link/length/privacy checks pass.
- **Next ready tasks: T03 and T05**, with their task-specific access prerequisites.
  T04 remains pending T03. Native client loading, behavioral compliance, real private
  content migration and stable release approval remain later task acceptance work.
