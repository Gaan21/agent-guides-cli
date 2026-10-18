# agent-guides

Neutral Python tooling for preparing owner-selected, self-contained Markdown
guidance from multiple Git repositories. Development commands `prepare`, `restore`
and `verify` prepare exact local bytes without native integration. `task-pin` and
`task-join` share independently retained host evidence between roles. See the
[preparation contract](docs/preparation.md) for inputs, bounds and examples.
Native connection and install/update/remove lifecycle operations are future tasks.

Start with the [canonical task handoff](docs/tasks/README.md),
[agreed scope](docs/delivery-scope.md) and
[technical reference](docs/delivery-implementation-plan.md).
The executable has no dependency on the legacy Flutter runtime or its payload.

## Development and local trial

Prerequisites: Python 3.11+, Git, and Python build tooling for source builds.
macOS and Linux are targets; consult T01 evidence for platforms actually tested.
Windows support is deferred. The scaffold itself does not invoke Git.

From the checkout, in a dedicated environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install build
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
.venv/bin/python tests/check_distribution.py -v
```

The distribution check builds an sdist, builds a wheel **from that sdist**,
inspects inventories and notices, installs the wheel without dependencies in a
fresh temporary tools environment, and exercises CLI and tests outside checkout.
Build dependencies may require network access. Tests use synthetic Git/CLI fixtures;
they do not execute consumer commands or alter global configuration.

For a retained local trial, build and inspect the wheel with the same procedure,
retain its bytes and SHA-256, then install that exact wheel into an owner-selected
environment with `python -m pip install --no-deps /path/to/exact-wheel.whl`.
Do not infer a stable published release from this development version.

## Boundaries and attribution

Content versions will be independent of executable releases. Native loading must
be demonstrated in installed clients before it is claimed; host integrity checks
do not establish model compliance. No guidance is installed by this scaffold.

Licensed under [Apache-2.0](LICENSE); see [NOTICE](NOTICE).
The handoff and packaging approach originate in
[flutter-agent-guidelines](https://github.com/Gaan21/flutter-agent-guidelines).
Small audited Apache-2.0 identity/path/snapshot/Git primitives are adapted with
provenance in `NOTICE`; the old runtime is not a dependency. Third-party tutorials,
configurations and lint sources are not imported.
