# T05 — Lossless common/private content split

Status: done. Depends on: T01 + T02 (done). Executor: consumer agent with private access.
Bounded local acceptance: [completion record](T05-acceptance.md), 2026-10-21.
Read [handoff](README.md), scope architecture/preservation requirements and bundle
schema accepted in T02. May run alongside T03/T04 in separate owned workspaces.

## Goal

Prepare all existing common guidance in the public `agent-guides` catalog and the
private `worktracker-architecture-guides` bundle without losing, weakening or
accidentally publishing any existing guidance. Owner expanded T05 on 2026-10-21
from the initial Flutter extraction to every existing technology/topic.

## Inputs and boundaries

- Owner-selected Git account/workspace/access and explicit authorization before
  creating either repository or publishing anything to either source. Placement:
  [ADR 0003](../decisions/0003-tool-and-guides-repositories.md).
- Actual common payload, selected existing architecture profile, WorkTracker's
  root/folder instructions, exceptions and referenced contracts, at recorded inputs.
- Existing multi-stack and cross-cutting guidance at exact privately recorded
  inputs. Inventory stack documents, applicable skill detail and references before
  deciding coverage. Historical routers/runtime instructions are source evidence,
  not authorization to restore deprecated delivery or executable helpers.
- Keep originals and the current functioning connection. Do not change active
  instructions or reclassify the whole current profile by renaming it.

## Workspace, destinations and authorization

- Common bundles: top-level technology/topic directories in public `agent-guides`;
  initial inventory includes Flutter, Git, Supabase, Next.js, Astro, .NET and
  cross-cutting agent workflow. One self-contained declaration per selectable unit.
  Projects select their combination; no automatic all-topic activation or new
  cross-bundle dependency mechanism. Record any further discovered topics.
- Private product catalog: reuse `worktracker-architecture-guides` without renaming
  it yet; prepare independently selectable `worktracker/`, `contadores/` and further
  owner-selected product bundles. Private inventory/classification stays in
  `evidence/` (owner decision,
  2026-10-20). Exact inputs and pins are listed in that private README only.
- Both repositories exist, cloned as siblings; deferred-maintenance documentation
  is already retained. Guidance bundles are prepared and accepted locally; not uploaded.
- Owner authorized Apache-2.0 for the selected owner-controlled original material
  from the private catalog. This excludes private history, product-specific output
  and third-party relicensing; review every candidate's provenance/notices.
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

## Expanded-scope checkpoint — 2026-10-21

Owner authorized preparing all existing common technology/topic guidance, not just
Flutter. Inventory/classification now covers the multi-stack source and applicable
cross-cutting material as well as the original Flutter/private inputs. Missing
guidance is reported, not invented. Bundles remain independently selectable from
one common catalog. Third-party material with unresolved rights is not exported;
record its disposition privately and request a decision if it blocks preservation.
Deferred detector/base-class improvements remain separate. No consumer activation,
archive, live policy edit or new public bundle upload is authorized by preparation.

Owner-approved catalog policy clarification: omit universal task-size/time caps and
task-planning/kanban procedures (task format alone may remain). Factory workflows
own branch/tool/publication steps; common guidance must not create a second flow.
Manual work respects the agreed branch and performs scoped commit/push at validated
closure without repeated approval. Missing/failing mandatory checks block closure
and commit/push; report actual results and consult the owner/host mechanism. PR is
the default integration route, not a mandate to branch away from an agreed `develop`.
These content decisions do not activate or rewrite any existing host/consumer policy.

Further owner decisions after parallel research: permit narrowly justified technical
corrections with private source/rationale retention, not consumer upgrades; use
block/relevant-change feedback plus complete final validation for manual Astro work;
inspect exact approved auxiliary sources read-only for private reference closure;
and consolidate private rules by product in the existing private repository. Do not
mix product bundles or rename the remote implicitly. Escalate corrections that alter
policy or have materially ambiguous consequences before editing affected content.

Supervised private-contract differences were subsequently resolved in retained
private evidence: preserve the actual approved product language/typography setup
and bounded adapter-owned exceptions, without changing consumer code or importing
old examples as rollback instructions. Detailed product semantics stay private.

First candidate: the Git bundle now has a short mode-aware entry, action-specific
detail, declaration and notices. Ten macOS/Python 3.15.0 unittests pass, exercising
the existing engine's schema/link/inventory rejection, exact license retention,
targeted private-content checks and complete source-range accounting for the ten
Git documents/skills reviewed. The initial entry is 36 lines. Source-range coverage
and authored wording checks are not independent semantic review or observed factory
behavior. Other bundles and full T05 acceptance remain pending. No new bundle was
committed, uploaded or activated at this checkpoint.

## Review-candidate checkpoint — 2026-10-21

All ten common bundles (Git, Flutter, Astro, Next.js, Supabase, .NET, engineering,
guidance maintenance, agent workflow, UI design) and both private product bundles
are drafted. One explicit twelve-bundle selection passes the unchanged engine's
schema/link/inventory checks and the public-marker scan; all focused suites pass on
macOS/Python 3.15.0, and a disposable exact-Git test prepares, verifies and restores
offline the common catalog with one product bundle without the other, from the
retained clean-install wheel. The candidate bytes are sealed for independent review.
A whitespace-only license deviation in one common bundle was corrected first.

Not yet established: independent semantic/privacy/rights review, owner answers to
six recorded questions, Linux or other Python runs, native loading and model
behavior. T05 stays in progress; the review brief and open questions are in the
private evidence index. Nothing was committed, pushed, uploaded or activated.
The first independent review unit (private product bundle) returned accept with
corrections; owner decisions and corrections are applied in a second sealed
candidate awaiting corrective review. Remaining review units have not started.
Continue only from `evidence/T05/CONTINUE.md` in the private product-catalog
repository.

## Handoff

### Preparatory clarification — 2026-10-21

Read-only architecture/linter research was retained privately. The owner deferred
implementation of its improvement proposals; it is not a new T05 prerequisite.
Future-maintainer summaries are recorded in the maintained common-guidance and
linter repositories, with required bidirectional change-impact review. No legacy
source, consumer, installed snapshot or lint selection was modified. The owner
subsequently accepted Result for public domain operations and direct values for
infallible getters/internal calculations. Detector/consumer changes remain deferred.
At that preparatory checkpoint T05 remained ready; the expanded-scope record above
then governed its in-progress status. Extraction and acceptance were incomplete then;
the completion record below now governs readiness.
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
reports only readiness/coverage outcome, not product content.

## Completion record — 2026-10-21

[T05 acceptance](T05-acceptance.md) supersedes the historical pending queues above.
Independent R1–R5 correction reviews passed their bounded scopes; the coordinator
authorized local content acceptance, not publication, stable approval or migration.
Recorded final validation passed on macOS 27.0.1 arm64 / Python 3.15.0, including
offline byte-equal restore and independent product selection. No suites were rerun
for documentation closure. Detailed identities/dispositions and review sampling
limits remain private. Deferred improvements above remain non-gating.
Next is T06 under its own prerequisites and authorization; it remains pending.
