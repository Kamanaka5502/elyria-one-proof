# Elyria Systems — One Proof Walkthrough

A single public-safe proof path showing how Elyria Systems frames consequence-bound execution.

This is not the engine. It is a deterministic walkthrough surface.

## Scenario

A high-consequence action is requested using stale evidence.

## Input

- actor: redacted
- action: privileged action request
- evidence status: stale
- authority status: present but evidence-dependent
- boundary: consequence commit point

## Boundary question

May this action bind consequence under current evidence, authority, and governing conditions?

## Evaluation

The public proof surface checks:

1. Is the evidence current enough to support consequence?
2. Does authority still apply under stale evidence?
3. Can an intent receipt be emitted?
4. Can the result replay under the same input and law?

## Decision

REFUSE

## Reason

EVIDENCE_STALE

## Consequence

No consequence binds.

## Receipt surface

A public receipt surface may expose:

- decision: REFUSE
- reason: EVIDENCE_STALE
- effect_receipt: none
- intent_receipt: emitted
- replay_status: MATCH

## Replay

Replay must reproduce the same refusal when law, state, and input remain identical.

## Proof claim

The proof is not that the system produced an answer.

The proof is that the system refused consequence when admissibility failed, emitted a receipt, and replay reproduced the refusal.

## Private layer not exposed

- evaluator internals
- stale evidence thresholds
- production receipt signing
- runtime enforcement adapter
- private policy graph
