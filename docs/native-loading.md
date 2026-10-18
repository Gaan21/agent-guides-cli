# Native loading: tested prerequisites

Status: T03 candidate evidence, not an implemented install command or full client
acceptance. See the [task record](tasks/T03-native-loading.md) for remaining gates.

## Claude Code 2.1.302

The tested candidate keeps short owned `@` import blocks in root and selected-folder
`CLAUDE.md` files. Existing product instructions and import chains stay in place.
Imports resolve relative to their containing file. Topics remain ordinary local
links in the authored entries; they are not all imported into initial context.

### External-import approval is separate from file access

An import outside the session's starting directory counts as external, even when
the target belongs to the same repository. Starting in a selected subdirectory can
therefore require approval for a root-local policy and prepared entries under the
repository root. Without approval, the tested noninteractive client omitted these
imports while still attaching the containing `CLAUDE.md` files.

Use the client's normal interactive startup to review and approve the intended
external imports in an owner-trusted project. Do not write approval state yourself
or infer approval from successful preparation, hashes, or `--add-dir`. The tested
approval persisted across new sessions and a sibling subdirectory in the same
disposable repository. This does not establish behavior for another repository,
machine, client version or nested worktree.

Use `/context` to inspect **Memory files**, then retain actual instruction attachment
evidence for acceptance. Model recall alone is insufficient. Do not use `--bare`
or `--safe-mode` to test this connection: they disable native instruction discovery.

### Topic reads need their own permission

Approving imports does not approve arbitrary reads outside the working directory.
In `dontAsk`, such reads are denied when they would otherwise prompt. `--add-dir`
grants working-directory access but does not approve external instruction imports.

For unattended topic reads, the tested native-policy candidate adds one `Read`
allowance for the exact prepared selection to project-local
`.claude/settings.local.json`. Preserve existing configuration and every deny/ask
rule; authorization to connect guidance does not override an owner's read policy.
The client must load the local settings source for the allowance to apply.

The generated allowance has this shape, with a real canonical local path:

```text
Read(//absolute/project/.guidance/selections/EXACT_SNAPSHOT/**)
```

The double slash denotes an absolute filesystem path in Claude permission syntax.
An allowance anchored to the current directory does not cover the root selection
when starting below it. The tested rule grants no edit access, covers no other
selection, and leaves unrelated root-file reads denied. Do not broaden it to a
whole filesystem, home directory or repository merely to make acceptance pass.
Machine-local registration must be regenerated on another checkout; it is not part
of the portable source selection. Transactional ownership/update/removal belongs
to T04 and is not implemented by this spike.

After connection changes, use a new session or the required native reload/restart.
Do not assume an existing session retracts already delivered instructions. The
tested resumed, compacted subdirectory session reattached the applicable entries;
native attachment records and explicit topic reads were checked separately.

## OpenCode 1.19.3

The tested candidate uses short root/folder `AGENTS.md` navigation directives.
Scoped read responses visibly attach folder `AGENTS.md` files. Referenced prepared
entries and topics are explicit tool reads, not automatic `@` imports. Initial
context proof and the remaining OpenCode acceptance matrix are still pending;
these Claude results do not close them.

## Upstream references

- [Claude instruction imports and loading](https://code.claude.com/docs/en/memory)
- [Claude file permission syntax](https://code.claude.com/docs/en/permissions)
- [OpenCode rule loading and file references](https://opencode.ai/docs/rules/)

Upstream documentation explains the mechanism; the installed-version trial is the
evidence for observations above. Neither establishes model compliance or complete
edit-tool guard coverage.
