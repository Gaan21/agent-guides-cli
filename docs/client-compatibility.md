# Current-client compatibility checks

Owner direction, 2026-10-23: validate against current stable Claude Code/OpenCode
clients and applicable security-patched runtimes, including frequent client updates.
This is an operator procedure under [T06](tasks/T06-migration.md), not a new board,
release gate, automatic updater, delivery hook or consumer-specific probe.

## Versions are evidence, not a permanent freeze

- Consult the official release/security sources immediately before a trial. Choose
  the latest stable client; use a supported runtime branch with current security
  fixes (LTS where appropriate), not an unreviewed major-version migration.
- Record timestamp, channel, actual executable/version and relevant runtime/plugin/
  linter versions independently of generated guidance. Recheck versions at the end.
- A changed client is a new compatibility observation. Keep the approved guide,
  engine and local-policy identities stable for comparison; never rewrite yesterday's
  evidence or independently resolve different sources for implementation/review.
- A daily client update does not implicitly update project dependencies, guidance,
  lint selections, permissions or production configuration.

## Bounded post-update checks

Use disposable roots with synthetic data and no production services or credentials.
Use native supported interfaces and the client's authenticated diagnostics; do not
inspect internal databases or invent an unauthenticated server route.

1. Verify the installed package and owned registrations against retained identity.
2. Observe the native short index exactly once, correct project/worktree root, scoped
   detail access and local-policy precedence. Generated files alone are insufficient.
3. Inspect the active native plugin list after location initialization. A successful
   helper smoke test or an initially empty/lazy list does not establish loading.
4. Exercise forbidden and allowed operations through actual native tools: patch,
   write/edit where offered, shell, and nested MCP/Code Mode where applicable. Test
   renamed tools and argument fields; a loading-only API port is insufficient.
5. Use inert executable/service fixtures for dangerous operations, with independent
   effect checks. Never send a real destructive command to production to test a guard.
6. Run the project's actual touched-file lint, type/compiler and focused test gates.
   Include a negative lint fixture where feasible. A warning or passing final gate
   does not waive a failing required intermediate checkpoint.
7. Separately exercise real-model selective reading, resume and native compaction/
   post-loss behavior in both clients. A local diagnostic provider proves execution
   mechanics/loading, not model compliance. Review the resulting edits.
8. Repeat relevant checks in the managed Linux/factory route before claiming factory
   readiness; macOS manual success is not production-launcher/host acceptance.

Record each failed attempt, prerequisite and unknown. Do not advertise compatibility
with an untested future daily update or automatic fail-closed enforcement from this
procedure. Existing product protections are independent of guidance delivery.

## If an update breaks protection

Stop the affected agent workflow; do not suppress the error, widen permissions or
continue without its required guards. Preserve the failure and explain options to
the owner. Adapt through the supported API in isolation, then repeat the checks.
Only use a previous version temporarily if it remains security-acceptable; a known
vulnerable version is not an acceptable automatic rollback destination.

No global installation, permanent service, factory configuration, live activation,
publication or automatic per-start check is authorized by this document.

## Official references

- [OpenCode V2 plugin migration](https://opencode.ai/v2/docs/build/plugins/migrate-v1)
  and [native tools](https://opencode.ai/v2/docs/tools).
- [Claude Code changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).
- [Node October 2026 security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases).
- [Python 3.15.1 security notes](https://www.python.org/downloads/release/python-3151/):
  existing virtual environments also need patched package-manager/certificate bundles.

The dated T06 continuation records what was actually checked, not this entire
procedure as completed. [T05 deferred improvements](tasks/T05-content-split.md#handoff)
remain separate and non-gating.
