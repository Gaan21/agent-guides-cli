# Native loading: tested prerequisites

Status: T03 blocked on the current OpenCode candidate; no accepted two-client
connection or implemented install command. See the [task record](tasks/T03-native-loading.md).

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
tested resumed, compacted subdirectory session reattached the applicable entries.
Its original continuation restored earlier read results without fresh tool calls;
the independent review caught that distinction. A supplemental continuation of the
same session issued three new successful sample/topic `Read` calls.

### Write timing and worktree limits

A first-write trial with a narrowly retained native `Edit` allowance for one scratch
file delivered folder instructions **after** `Write` completed and before the next
`Read`. This is native loading, not prevention of a first edit without folder rules.
`Edit(path)` is the relevant file-mutation permission family, including `Write`;
the fixture's redundant `Write(path)` rule was diagnosed as unsupported syntax.
Actual protected-file `Edit` and `Write` calls were rejected by native settings.

A real nested Git worktree loaded its own root imports and excluded parent-worktree
policies. Starting in its subdirectory again omitted external imports before native
approval. Approval from the earlier disposable repository is not evidence of approval
for this worktree; its interactive approval/access acceptance remains pending.

## OpenCode 1.19.3

The current root/folder `AGENTS.md` navigation candidate **fails T03 acceptance**:

- Loopback capture of requests produced by the installed client shows root-only
  native instructions at a root start and root plus applicable-folder instructions
  at subdirectory starts. These contain the owned navigation directive, **not the
  prepared entry's contents**. Topics and sibling scope rules stay out initially.
- This capture uses an explicitly retained local diagnostic provider and a fixed
  response, without upstream inference. It establishes loader/request composition
  for that arrangement, not model compliance or the exact OAuth request. Configured
  model sessions independently exercise explicit entry/topic reads and scoped loading.
  OAuth telemetry/export alone did not expose the full initial system instructions.
- Scoped `Read` responses attach the folder `AGENTS.md`; prepared entries/topics
  are later explicit reads. Existing `CLAUDE.md` imports are not a second OpenCode
  delivery route when `AGENTS.md` is present. Preserve the files and local authority.
- **Edit-first gap:** an initial `apply_patch` adding files in both scopes succeeded
  without folder reminders. Only subsequent `Read` calls attached those policies.
  A root index or a model-directed read-before-edit convention is not proof of
  automatic native edit-triggered scope delivery.
- Actual TUI `/compact` and same-session continuation were exercised. Folder policies
  reattached on subsequent sample reads; ordinary pre-compaction resume had deduplicated
  them. A model path typo was corrected without modifying the selection.
- Conflicting root/folder local exceptions remained effective in observed replies.
  Native `edit` denial rejected an actual `apply_patch` call against a protected file.
  The exposed editing tool was `apply_patch`; this is synthetic tool coverage, not
  acceptance of a consumer's pre-existing guards or every patch operation.
- Root/two subdirectory request captures and configured-model scoped reads respected
  a real nested-worktree boundary. No parent-worktree policy was attached in captures.

The client owns discovery, read reminders and permissions; the candidate owns one
short marked block per native file. No delivery plugin, hook or global Markdown
glob was added. T04 remains pending until a native strategy meets the contract and
is accepted. Linux installed-client checks remain unavailable in this session.

## Upstream references

- [Claude instruction imports and loading](https://code.claude.com/docs/en/memory)
- [Claude file permission syntax](https://code.claude.com/docs/en/permissions)
- [OpenCode rule loading and file references](https://opencode.ai/docs/rules/)

Upstream documentation explains the mechanism; the installed-version trial is the
evidence for observations above. Neither establishes model compliance or complete
edit-tool guard coverage.
