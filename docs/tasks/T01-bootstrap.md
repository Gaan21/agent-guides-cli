# T01 — Bootstrap agent-guides

Status: done (independent review accepted, 2026-10-17). Depends on: none.
Executor: repository agent; independent review completed in a subsequent session.
Read [handoff](README.md), [scope](../delivery-scope.md), technical-plan sections 1/5.

## Goal

Establish a separate neutral Python package in a new public repository without
coupling it to the current Flutter runtime. This is scaffolding, not installation
of guidance into a consumer.

## Execution inputs

- Actual repository owner, approved local workspace and authorization for any
  repository creation. Do not infer an account, parent directory or remote URL.
- Read-only checks of `agent-guides` repository/PyPI name availability. If occupied
  incompatibly, report the conflict and ask for a name decision; do not substitute.
- A supported available Python/Git runtime and an identified Linux validation path.
  Publication credentials are not required for this task.

## Work

1. Create the authorized repository/package scaffold, with neutral CLI/module
   naming, Python compatibility declaration, license/notices and test/build setup.
2. Establish maintainer instructions preserving integrity, privacy, authorization
   and native-loading limits from this repository without Flutter-specific runtime
   assumptions. Reuse audited code only with its required license/provenance.
3. Provide a minimal CLI identity/help path. Do not implement command-shaped stubs
   that report success for install/update/verify before those operations exist.
4. Carry the canonical handoff to the new repository per the index; repair links
   to legacy reference code and leave a single authoritative task board.

## Acceptance

- Build sdist and wheel from sdist, inspect expected resources/notices, install
  into a clean tools environment, and exercise CLI help/version outside checkout.
- No Flutter payload/runtime dependency and no consumer changes/global settings.
- Record available Python/OS checks; Linux remains pending if not exercised.
- Record actual repository/handoff locations without placing private paths in
  public documentation. No publication implied by a working package build.

## Handoff

Mark T02 ready after review. Record package structure, exact check commands/results
and code-reuse decisions. Repository creation/publication permissions remain
separate from implementation permission. Completion evidence follows.

## Completion record — 2026-10-17

### Delivery and authorization

- Owner confirmed `Gaan21`, the sibling `agent-guides` workspace and creation of
  both local and public repositories. Created <https://github.com/Gaan21/agent-guides-cli>
  with local `origin`; public visibility confirmed by GitHub API. At bootstrap the
  remote was empty (size 0); staging, commits and pushes were not yet authorized.
  No releases, PyPI publication or consumer activation were performed. Default
  branch is `develop`. Subsequent source-upload authorization is recorded below.
- Before creation, `gh api repos/Gaan21/agent-guides` returned HTTP 404. Read-only
  `https://pypi.org/pypi/agent-guides/json` returned HTTP 404. These observations
  establish no published project was found, not reservation or registry approval.
- Package: `src/agent_guides/{__init__,__main__,cli}.py`; distribution/executable
  `agent-guides`, version `0.1.0.dev0`, Python `>=3.11`, no runtime dependencies.
  Help/no-argument usage and version work. Unsupported operations exit 2 rather
  than reporting successful preparation, verification or integration.
- Added `pyproject.toml`, `MANIFEST.in`, `.gitignore`, `README.md`, `AGENTS.md`,
  `LICENSE`, `NOTICE`, `tests/test_cli.py`, `tests/check_distribution.py`, and
  `.github/workflows/checks.yml`. CI defines macOS/Linux and Python 3.11/3.15 checks;
  its execution was pending until the subsequently authorized source upload.
- Moved scope, technical reference and all seven task files plus this index into
  `docs/`. Fixed legacy reference links. Replaced the old documents with pointers
  so there is one editable board. Exact local location is retained in execution
  evidence; public documentation uses repository-relative/sibling locations.
- Reuse decision: no legacy runtime primitives or Flutter payload copied/imported.
  Packaging/distribution patterns and the handoff were adapted, with attribution
  and modification notice in `NOTICE`; Apache-2.0 license included. Audit actual
  primitive reuse separately in T02. Existing runtime, consumers and snapshots
  were not modified.

### Verification and retained evidence

Commands below use `TOOLS315` / `TOOLS314` for the dedicated local tools
environments. Their exact paths and command expansions are retained in
`.git/T01-results.md`, not public source.

```sh
"$TOOLS315/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS315/bin/python" tests/check_distribution.py -v
"$TOOLS314/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS314/bin/python" tests/check_distribution.py -v
python3 .git/t01_review.py
git diff --check
```

- macOS 27.0.1 arm64: Python 3.15.0 and 3.14.8 each passed 2 CLI unittests,
  1 distribution unittest and the same 2 CLI tests against an installed wheel
  outside checkout using isolated Python. Git 2.54.0 available.
- Distribution check built sdist, built wheel from extracted sdist, checked all
  expected handoff/test/notices resources in sdist and exact wheel inventory,
  compared license/notice bytes, checked Python declaration/no dependencies, and
  exercised installed console help/version plus failure for unsupported operations.
  Backend observed: build 1.6.1, setuptools 84.0.0, wheel 0.48.0.
- Final Python 3.15 distribution run retains the exact wheel/sdist bytes and
  SHA-256 values in the approved local evidence area. Earlier trial artifacts were
  temporary; no stable release claim follows from any build.
- Task identity was retained before review in `.git/T01-identity.json`: exact
  legacy source revision/policy blob, SHA-256 inventory of engine, build/tests,
  license, maintainer policy, scope and technical reference; overlays empty;
  bundle/selection identities not applicable to this scaffold. This evidence is
  independent of generated distribution/metadata files. Do not recapture it when
  reviewing this execution. T02 prepares its own new task identity.
- Review result: retained identity matched; scope text preserved except its legacy
  documentation link; closed decisions and unchanged downstream task instructions
  compared to original Git bytes; local links, file-length/privacy checks passed.
  This was a separate in-session verification pass by the implementing agent,
  not an independent human or second-agent review. Evidence and the review script
  remain in local Git metadata for a subsequent reviewer.

### Limits and next handoff

- Independent review remains the T01 closure gate. At the local trial Linux
  execution was pending:
  `docker info --format '{{.OSType}}'` failed because the local daemon socket was
  unavailable. The checked-in Ubuntu CI job is the identified validation path,
  not evidence of a Linux pass. Python 3.11 was unavailable locally; minimum-version
  validation was also pending in CI. Subsequent CI results are recorded below.
  Windows is deferred.
- No installed-client versions or native-loading behavior tested; those belong to
  T03. No tamper/path/selection guarantees claimed before T02 implements them.
- Owner subsequently authorized commits and pushes for both the scaffold and
  legacy forwarding changes. Releases, registry publication and consumer activation
  remain separate actions requiring authorization. Preserve both checkouts and
  retain the local identity/artifacts for review; those are not in public source.
- Next assignment: **independent T01 review**, in this repository. No next
  implementation task is ready until that review passes. The reviewer records
  findings against the retained identity, marks T01 done only on acceptance, then
  changes T02 to ready. Preserve the closed scope; do not activate a consumer.

### Closure correction and source-publication handoff — 2026-10-17

The implementation agent initially marked T01 done and T02 ready after its own
checks. That was premature: the index requires independent implementation/review.
Both statuses are corrected above. Executed tests remain valid evidence; they are
not evidence of an independent reviewer. The owner's commit/push authorization
does not waive this gate. The next agent reviews T01 rather than starting T02.

Public source is to be uploaded on `develop`, matching the remote default branch.
Publication results and exact commits/check runs are retained in local execution
evidence and reported to the owner. Git history identifies source commits without
embedding internal execution pins in this public record.

### Source publication and CI result — 2026-10-17

- Authorized commits pushed to `origin/develop` in both `agent-guides` (scaffold,
  handoff and closure correction) and `flutter-agent-guidelines` (forwarding docs).
  Both working trees were clean and local heads matched remote-tracking heads.
- The [bootstrap CI run](https://github.com/Gaan21/agent-guides-cli/actions/runs/39082879572)
  passed all four jobs: Ubuntu/macOS runners, each with Python 3.11 and 3.15.
  Each job installed the package, ran CLI unittests, built sdist then wheel from
  sdist, inspected resources/notices and exercised a clean wheel installation.
  This supplies the previously pending Linux/minimum-Python scaffold checks;
  it does not establish client loading or later lifecycle support.
- Observed with `gh run watch 39082879572 --repo Gaan21/agent-guides-cli --exit-status
  --interval 10` (exit 0). The linked run retains exact tested commit, runtime
  versions and logs; local execution evidence retains publication commit IDs.
- Next agent still performs independent T01 review against the retained identity.
  CI success is test evidence, not that review. T01 remains `in_progress` and T02
  remains `pending` until the reviewer records acceptance.

### Independent review and acceptance — 2026-10-17

**Verdict: accepted for T01's scaffold scope. No closure blockers found.** This
subsequent review inspected the implementation and retained evidence independently
of the implementing agent's self-checks. T01 is `done`; T02 is `ready`, not started.
Earlier pending statuses above describe the historical execution sequence.

Acceptance / Handoff findings:

- All 14 file digests in `.git/T01-identity.json` match current bytes, committed
  HEAD and the CI-tested implementation. Source revision/policy, empty overlays
  and non-applicable bundle/selection fields agree with the scaffold scope. The
  expected identity was read unchanged, never regenerated or replaced.
- Both retained artifact hashes match `.git/T01-results.md`. Independently checked
  sdist engine/build/test/policy/scope bytes, task-document presence, safe member
  paths, exact wheel inventory, Python declaration, no dependencies, entry point
  and license/notice bytes. The retained sdist predates later handoff-only records;
  it is historical build evidence, not a copy of the current task board.
- Installed the exact retained wheel with `--no-index --no-deps` in a fresh tools
  environment outside checkout. Both isolated CLI tests passed; console help,
  no-argument usage and version succeeded; all six unavailable operations exited 2.
- Independently reran 2 CLI tests and the distribution unittest: built sdist, built
  wheel from sdist, inspected resources/notices, installed cleanly and passed 2
  installed-wheel CLI tests. Local runtime: macOS 27.0.1 arm64, Python 3.15.0;
  backend setuptools 84.0.0 / wheel 0.48.0. Temporary rebuilds did not replace the
  original retained artifacts. Manifest exclusion warnings were non-fatal.
- Reviewed the neutral package/CLI, maintainer policy and Apache-2.0 attribution;
  no legacy runtime primitives or Flutter payload are included. The legacy Git
  diff changes only the ten handoff/forwarding documents, with a clean working
  tree; the canonical editable board is here. Scope, closed decisions and T03–T07
  instructions match retained source evidence. Locations remain recorded locally.
- Rechecked the linked CI run through GitHub: all four macOS/Ubuntu × Python
  3.11/3.15 jobs succeeded against the same engine/build/policy bytes. These are
  prior CI results, not new independent Linux or minimum-Python executions.

Commands (`TOOLS315` retains its meaning above; expanded commands, artifact
digests and exact reviewed commits are in `.git/T01-results.md`):

```sh
python3 .git/t01_review.py
"$TOOLS315/bin/python" .git/t01_independent_review.py
"$TOOLS315/bin/python" -m unittest discover -s tests -p 'test_*.py' -v
"$TOOLS315/bin/python" tests/check_distribution.py -v
gh run view 39082879572 --repo Gaan21/agent-guides-cli --json conclusion,headSha,jobs,url
git diff --check
```

Limitations: hashes establish integrity, not trust. Repository creation/earlier
upload authorization is historical retained evidence, not new session permission.
No independent local Linux/3.11 rerun, installed-client/native-loading, behavioral
compliance, tamper/selection lifecycle or Windows claim follows from this review.
Those later-task/deferred checks do not block the scaffold acceptance. This session
changed only review/handoff records and left consumers/global settings untouched.

Next handoff: execute T02 using its acceptance fixtures and a separately retained
T02 identity. Preserve T01 evidence. No staging, commit, push, release, PyPI upload
or consumer activation was performed or authorized by this review.
