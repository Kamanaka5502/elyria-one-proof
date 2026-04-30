<p align="center">
  <img src="./elyria.png" alt="Elyria AI" width="700"/>
</p>

# Elyria One Proof

> BOT proposes. Boundary decides. Only admitted consequence becomes real.

This is not a model demo.  
This is a minimal proof surface for BOT/AI execution-boundary enforcement.

The bot proposes.  
The boundary resolves.  
Consequence only binds if admitted under current governing state.

---

## Core Condition

A transition either satisfies admissibility at execution and binds,  
or it does not occur.

---

## What This Demonstrates

- decision resolved at the execution boundary (before effect)  
- fail-closed enforcement when admissibility does not hold  
- deterministic receipt bound to decision + context  
- replay under the same governing state yielding the same decision class  

---

## What This Is Not

- not a workflow  
- not a monitoring system  
- not post-hoc validation  
- not a model output demo  

---

## Run

```bash
python runner.py demo/valid_case.json
python runner.py demo/invalid_case.json
python replay/replay_test.py
```

---

# Expected Results

**Valid Case**
decision: EXECUTE
side_effect_allowed: true

**Invalid Case**
decision: REFUSE
side_effect_allowed: false

---

## Boundary Rule

The receipt proves the **decision**, not just the outcome.

## Architecture

Proposed Transition → Governing State → Execution Boundary → Admissibility Evaluation → Decision Class → Effect Control → Receipt → Replay → Protected Custody

## Definitions

**Proposed Transition** — AI/BOT-generated action before it becomes real  
**Governing State** — current state, authority, capacity, constraints  
**Execution Boundary** — point where the system decides if transition may bind  
**Admissibility Evaluation** — resolution of whether conditions are satisfied  
**Decision Class** — EXECUTE / REFUSE / ESCALATE / HALT  
**Effect Control** — EXECUTE allows effect, REFUSE prevents effect, no partial execution  
**Receipt** — proof artifact binding input, state, decision, reason  
**Replay** — same input + same governing state → same decision class  

## Invariant

If admissibility does not hold at execution, the transition does not bind.

## Statement

Validity is not inferred. It is resolved at execution.

## Protected Scope

Public surface only. Core BOT/AI runtime remains protected.  
No internal enforcement logic, authority model, custody chain, or production corridors exposed.

## Purpose

Demonstrate the minimum mechanism required to evaluate execution-boundary enforcement:  
**boundary decision → receipt → replay**

## Access

Full implementation available under NDA.

---

<<<<<<< HEAD
**Run it. Verify it. Replay it.**
=======
Run it. Verify it. Replay it.

## Evaluation & NDA

This repository is a minimal public proof surface.

For full evaluation (production corridors, authority model, custody chain, and internal enforcement logic), access is provided under NDA.

Request access:
- Samantha Revita · Terry Snyder
- Email: SamanthaGreenwellRevita@gmail.com
- Subject: "Elyria One Proof – NDA Request"

Include:
- Organization
- Evaluation scope (what you want to test)
- Environment (sandbox / API / on-prem)

What you’ll receive under NDA:
- Controlled runnable bundle (one corridor)
- Deterministic receipt schema + verifier
- Replay harness
- Audit-ready logs
- Fail-closed test suite (negative cases)

We evaluate on mechanism:
decision at boundary → receipt → replay.
>>>>>>> 79d5899 (Add NDA evaluation path with Samantha Revita and Terry Snyder authorship)



## Visible Effect Proof

EXECUTE creates a real artifact:
python runner.py demo/valid_case.json && ls
You will see: effect_result.txt

REFUSE blocks consequence:
python runner.py demo/invalid_case.json && ls
effect_result.txt is not present.

This demonstrates control at the execution boundary, not post-hoc logging.


## Receipt Verification

Verify a receipt hash locally:
python - << 'PY'
import json,hashlib,sys
p="receipts/demo-valid-001_receipt.json"
r=json.load(open(p))
h=r["receipt_hash"]
c=hashlib.sha256(json.dumps({k:v for k,v in r.items() if k!="receipt_hash"},sort_keys=True,separators=(",",":")).encode()).hexdigest()
print("OK" if h==c else "MISMATCH", h)
PY

