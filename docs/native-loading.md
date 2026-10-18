# Native loading: tested prerequisites

Status: T03 in progress after owner clarification; no accepted two-client
connection or implemented install command. See the [task record](tasks/T03-native-loading.md).

## Current direction: selective reading, not an editing gate

The owner clarified that agents should choose relevant guidance before applicable
edits and reuse it while available in context. Loading every topic, rereading before
each patch or enforcing an absolute read-before-edit guarantee is not desired.
Native short-entry delivery and actual model-selected reads are separate checks.
The historical automatic-loader gaps below remain valid, but are not by themselves
a rejection of a simple root index with selective topic reading. See the
[new behavioral trial](tasks/T03-selective-reading.md); full T03 acceptance is pending.
The rationale is [ADR 0001](decisions/0001-selective-guidance-reading.md). Later
[lightweight observation](tasks/T08-lightweight-observation.md) uses authorized
existing traces, not an always-on monitor or a mandatory installation component.

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

## OpenCode 2.0.32 — bounded diagnostic trial

Tested on macOS 27.0.1 arm64. V2 is distributed separately from the V1 Homebrew
formula: upstream documents `anomalyco/tap/opencode-v2`. The trial used the official
versioned standalone binary, with its archive SHA-256 matched against the official
formula, isolated home/XDG directories and `run --standalone`.

The unchanged navigation-only bridge still omits prepared entry content initially.
A separately retained candidate adds exact short-entry paths to native `instructions`
arrays in root and selected-folder `opencode.json` files:

- Initial root requests contain the root entry; subdirectory starts contain the root
  and applicable-folder entries, byte-for-byte, without topics or sibling entries.
  Existing native policy files and prepared snapshots remain unchanged.
- This establishes a native first-turn entry route for those launch locations.
  It does not establish dynamic scope entry loading when working from the root.
- **The edit-first gap remains:** the real V2 `patch` tool successfully adds files
  in both scopes. Neither the initial request nor the request after the patch has
  their folder policies. Subsequent real reads deliver each folder's `AGENTS.md`.
- Those reads do **not** load the short entries declared in the folders' configuration
  files. Folder startup configuration is not an on-demand per-edit configuration.

Eight client invocations used a loopback diagnostic provider. Its fixed responses
and scripted tool calls observe the installed loader and real tool timing without
upstream inference or credentials. They do not prove configured-provider equivalence
or model compliance. V2 TUI, resume/compaction, native guard rejection and Linux
acceptance were not exercised. V1 observations are not inherited as V2 passes.

**T03 remains blocked; T04 remains pending.** Configured short entries improve startup
delivery but do not satisfy mixed-scope/edit-first acceptance. Use the retained
[V2 task record](tasks/T03-native-loading.md#opencode-2032-diagnostic-continuation--2026-10-18)
for review and next prerequisites.

### Installed-V2 recheck and inline-entry candidate

The currently installed Homebrew-linked executable was queried independently:
**2.0.32**, byte-identical to the earlier official standalone binary. Inspection of
its embedded implementation separates ambient/configured startup instructions from
the `read` tool's discovery of nested `AGENTS.md`. The GPT `patch` tool does not call
that discovery, even when it internally reads an existing target.

New fixtures retest configured entries and a native inline-entry candidate: keep
the root configured entry and add short entry bytes to the applicable folder's
`AGENTS.md`, without topics. Scoped file reads and directory listings then deliver
the folder policy and entry together. **A first root-started mixed-folder patch
still succeeds without them**, and they remain absent on the next request.
An explicit directory-read-first control loads them before a later patch, but does
not meet automatic edit-first acceptance. Inline relative topic links also require
a retained base-path transformation before that route could be used.

Three new diagnostic invocations pass their retained identity joins; an earlier
sample-edit attempt is preserved and excluded after its policy identity changed.
All use scripted loopback responses, not remote inference. No OAuth equivalence,
model compliance or complete V2/platform acceptance is claimed. See the
[installed-V2 record](tasks/T03-native-loading.md#installed-v2-mechanism-and-new-candidates--2026-10-18).
The missing prerequisite is native target-scoped policy/entry delivery before the
first mutation, not another startup index. **T03 stays blocked; T04 stays pending.**

## Upstream references

- [Claude instruction imports and loading](https://code.claude.com/docs/en/memory)
- [Claude file permission syntax](https://code.claude.com/docs/en/permissions)
- [OpenCode rule loading and file references](https://opencode.ai/docs/rules/)
- [OpenCode V2 installation](https://opencode.ai/v2/docs)
- [OpenCode V2 native instructions](https://opencode.ai/v2/docs/instructions)
- [Official V2 Homebrew formula](https://github.com/anomalyco/homebrew-tap/blob/master/opencode-v2.rb)

Upstream documentation explains the mechanism; the installed-version trial is the
evidence for observations above. Neither establishes model compliance or complete
edit-tool guard coverage.
