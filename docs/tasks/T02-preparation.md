# T02 — Exact multi-source preparation

Status: in_progress (implemented; CI passed; independent review pending).
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
- [T02 CI run](https://github.com/Gaan21/agent-guides/actions/runs/39087489115)
  passed all four macOS/Ubuntu × Python 3.11/3.15 jobs. Each ran 27 source tests,
  the distribution unittest (sdist then wheel from sdist, resources/notices,
  clean install), CLI help/version and 27 installed-wheel tests outside checkout.
  This supplies the previously pending Linux/minimum-Python implementation checks,
  distinct from T01 CI and local macOS checks.
- Observed with `gh run watch 39087489115 --repo Gaan21/agent-guides --exit-status
  --interval 10` (exit 0). The run retains exact source/runtime details and logs.
  A documentation-only follow-up records results without changing tested engine,
  build, tests, policy or retained artifact identity.
- **Remaining closure gate: independent T02 review.** T02 stays `in_progress`;
  T03/T05 stay `pending`. The next reviewer compares the same expected identity,
  artifacts and actual implementation against Acceptance / Handoff, then records
  acceptance or exact findings. No new source resolution or expectation capture.
  Earlier local/pending-publication statements above are historical, superseded
  by this result. No releases, registry publication or consumer activation.
