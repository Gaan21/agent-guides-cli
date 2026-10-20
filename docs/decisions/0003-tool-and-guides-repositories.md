# ADR 0003 — Separate tool and guides repositories

Date: 2026-10-20. Status: owner decision; supersedes the executable name in the
[agreed scope](../delivery-scope.md) and places common guidance. All other scope
decisions are unchanged.

## Decision

- **Tool:** `agent-guides-cli`, this repository. Distribution and command are
  `agent-guides-cli`; the import package is `agent_guides_cli`. It contains no
  authored guidance.
- **Common guides:** a new public repository named `agent-guides`. It holds all
  common authored guidance in one catalog, one self-contained bundle per stack or
  topic (for example a Flutter bundle). The current common Flutter payload in
  [flutter-agent-guidelines](https://github.com/Gaan21/flutter-agent-guidelines)
  is the input for that bundle.
- **WorkTracker architecture:** unchanged, the separate private
  `worktracker-architecture-guides` repository. Product-specific and uncertain
  content never goes into the public guides repository.

## Why

The owner wants names that tell the tool from the content, and one guides catalog
like the deprecated private predecessor instead of a repository per stack. The
name `agent-guides` describes the content better than the executable.

## Consequences

- One source has one recorded commit. Bundles selected from `agent-guides` move
  together on update; per-bundle snapshot digests still show which bundle changed.
  Independently versioned stacks would need separate repositories; not selected.
- The existing GitHub repository is renamed to `agent-guides-cli`. Creating the new
  `agent-guides` repository ends GitHub's redirect from the old name, so links use
  the new name. Historical task records keep the module, command and variable names
  they executed; only their repository links were updated.
- The owned native block marker is now `<!-- agent-guides-cli:begin -->`. Only
  disposable trials used the previous marker; no consumer was connected.
- T03/T04 client and platform evidence remains tied to the pre-rename engine
  identity. The rename is mechanical and re-verified by package and distribution
  tests; installed-client trials were not repeated for it.
- Legacy delivery in flutter-agent-guidelines stays intact until authorized T06
  migration. Its forwarding pointers need a separate authorized update.
