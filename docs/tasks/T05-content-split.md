# T05 — Lossless common/private content split

Status: ready. Depends on: T01 + T02 (done). Executor: consumer agent with private access.
Read [handoff](README.md), scope architecture/preservation requirements and bundle
schema accepted in T02. May run alongside T03/T04 in separate owned workspaces.

## Goal

Prepare the common Flutter bundle in the public `agent-guides` guides repository
and the private `worktracker-architecture-guides` bundle without losing, weakening or accidentally publishing any existing guidance.

## Inputs and boundaries

- Owner-selected Git account/workspace/access and explicit authorization before
  creating either repository or publishing anything to either source. Placement:
  [ADR 0003](../decisions/0003-tool-and-guides-repositories.md).
- Actual common payload, selected existing architecture profile, WorkTracker's
  root/folder instructions, exceptions and referenced contracts, at recorded inputs.
- Keep originals and the current functioning connection. Do not change active
  instructions or reclassify the whole current profile by renaming it.

## Workspace, destinations and authorization

- Common Flutter bundle: top-level `flutter/` in the public `agent-guides` repository.
- WorkTracker bundle: `bundle/` in the private `worktracker-architecture-guides`
  repository; private inventory/classification in its `evidence/` (owner decision,
  2026-10-20). Exact inputs and pins are listed in that private README only.
- Both repositories exist, empty apart from README/AGENTS.md, cloned as siblings.
- Authorized: pushing the private repository's T05 content when T05 is complete.
  Pushing content to the public `agent-guides` needs explicit owner authorization;
  run the public-output check (step 4) first and report it with the request.
- Not in T05: editing WorkTracker, installed snapshots or legacy repositories, and
  deprecating legacy delivery; see [T06 legacy retirement](T06-migration.md#legacy-retirement).

## Work

1. In private evidence, inventory every rule, exception, topic and required link.
   Record its source, destination, retained meaning and verification method.
2. Classify clearly reusable guidance as common. **If uncertain, place it in
   WorkTracker.** Resolve contradictory/overlapping prose explicitly; do not drop
   requirements during deduplication, summarization or formatting.
3. Prepare complete bundles with short entries, authored reading conditions,
   preserved detail links/notices and explicit inventory. No extra profile
   activation or custom dependency machinery.
   State when each topic applies, its scope and required dependencies, and useful
   non-applicability boundaries. Keep the initial entry concise: no full-topic
   duplication or instruction to read every topic/per-patch. Preserve always-on
   requirements and dependency modality; selection is not permission to weaken rules.
4. Check public output for private paths, product APIs and product-specific rules.
   Publish no private classification report or logs in the common/tool repositories.
5. Verify every inventoried requirement has a destination and every required local
   reference is present. Compare meaning as well as file hashes where text moved.

## Acceptance

Private source-to-destination coverage has no unassigned or discarded requirements;
uncertain cases are retained privately. Common and WorkTracker bundles pass T02's
schema/link/inventory verification. Review confirms conditions/modality, exceptions,
offline durable-local acceptance and attribution remain intact. Changing delivery
does not install/change executable lints or refactor the product.
Review a few representative tasks against authored applicability: relevant topics
and required dependencies should be discoverable without unrelated blanket reads.
Use [ADR 0001](../decisions/0001-selective-guidance-reading.md); this task prepares
content, not a runtime selector or a guarantee of future model behavior.

The old payload is not deleted or the live consumer switched here. Agree any later
retirement with T06 after validated migration; preserve rollback source/evidence.

## Handoff

### Preparatory clarification — 2026-10-21

Read-only architecture/linter research was retained privately. The owner deferred
implementation of its improvement proposals; it is not a new T05 prerequisite.
Future-maintainer summaries are recorded in the maintained common-guidance and
linter repositories, with required bidirectional change-impact review. No legacy
source, consumer, installed snapshot or lint selection was modified. The owner
subsequently accepted Result for public domain operations and direct values for
infallible getters/internal calculations. Detector/consumer changes remain deferred.
T05 remains ready: inventory, content extraction and acceptance are not complete.
Documentation checks and authorization limits are recorded in the private evidence
index. The owner subsequently authorized documentation commit/push in the CLI,
common-guidance, private-guidance and linter repositories. Consumer activation,
releases and implementation of deferred improvements remain unauthorized.

Future-maintainer follow-up (low urgency; not new T05 gates):

- [Common guidance](https://github.com/Gaan21/agent-guides/blob/develop/docs/deferred-improvements.md).
- [Dart linter](https://github.com/Gaan21/dart-architecture-lints/blob/main/docs/deferred-guidance-alignment.md).
- Detailed product findings and research remain in the private repository's
  evidence index; never copy them into either public follow-up.

Privately record exact candidate sources and selections for T06. Propose (do not
apply without authorization) a legacy README note that common content now lives
in `agent-guides` while the legacy runtime stays in use. Public handoff
reports only readiness/coverage outcome, not product content. Completion evidence: pending.
