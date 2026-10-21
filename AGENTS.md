# Maintainer instructions

- Scope: this repository's neutral Python tooling and its public handoff. English;
  concise; files below 500 lines. Keep authored guidance separate from the engine.
- Preserve the agreed scope and task order in `docs/tasks/README.md`. Inspect Git
  status/diff before work; retain existing work. No legacy runtime deletion or
  automatic consumer migration. Record checks, limitations and handoff results.
- When asked about pending work, start with `docs/tasks/README.md`; include T05's
  deferred follow-up links without changing task order or creating a competing board.
- Multiple owner-selected Git sources; resolve approved selections once during
  install/update; restore exact recorded commits. No independent latest resolution
  for implementation and review. Never edit live snapshots.
- Retain source, selection, engine, policy and overlay identity once per task and
  independently of generated files for review. Hashes prove integrity, not trust.
  Owner-approved development Git trials do not establish stable-release approval.
  Release attestations stay outside source.
- No private paths, consumer logs, product APIs, architecture rules, source-report
  dumps or internal revision pins in public documentation. Detailed classification
  and migration evidence stay in the private owner's repository. Uncertain content
  classification belongs in the private WorkTracker bundle; preserve every rule.
- No automatic staging, commits, pushes, releases, registry publishing or consumer
  activation. Each needs explicit authorization. Repository creation is separate
  from source upload/publication. No implicit hooks, global configuration,
  credentials or product-command execution.
- Native loading needs installed-version evidence. Verify host integrity, observed
  client loading and model compliance separately. Do not claim native enforcement
  from generated files or passing host tests. Preserve offline durable-local
  acceptance versus remote acknowledgment and upstream instruction modality.
- Use unittest for wheel/sdist resources, clean installation, and (as implemented)
  tamper/path rejection and shared task identity. Test supported available runtimes;
  report unavailable platform/client checks pending. Run targeted checks first.
- Keep authored entries short with local detail/inventory/notices. Link third
  parties rather than importing tutorials, configurations or lint sources. Reuse
  only audited primitives with required license/provenance. No Flutter runtime
  dependency, hooks/daemon, leases, mandatory end/rebaseline, AI retrieval,
  per-content executable environments or consumer wrappers/probes.
