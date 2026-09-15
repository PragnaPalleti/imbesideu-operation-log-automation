# Final Report — From Operation Logs to an Automation Proposal

## 1. Executive Summary
The project converts low-level desktop/browser telemetry into business-work evidence, validates an observable workflow-anchor signal on Dataset A, applies the same inference principle to Dataset B, and selects a safe automation target. The strongest observed B signal is repetitive **expense review**: explicit expense-review/compliance evidence appears 177 times across all 15 B sessions. A deterministic prototype pre-checks expense category/amount against a configurable policy threshold and routes ambiguous or over-threshold cases to a human.

The key engineering choice is **confidence-aware, evidence-first automation**: use raw UI/workflow anchors when available, use temporal/application context as supporting signals, and never claim that a mock integration is production-ready.

## 2. Business Problem
The client has operation logs but no direct business-process labels in the raw stream. The assignment asks us to recover coherent units of work, understand what consumes effort, identify the best automation opportunity, and demonstrate something that actually works.

## 3. Data Understanding
Dataset A contains 63 sessions and approximately 162,000 events with ground truth; Dataset B contains 15 sessions and approximately 20,000 events without ground truth. Chunks are fixed recording buckets rather than business boundaries. Raw events include application switches, keystrokes, mouse/clipboard activity, browser operations, context and sparse extracted screen text.

Observed in this run:
- Dataset A: **63 sessions / 162,768 events**.
- Dataset A ground-truth manifests: **2,009 execution records**.
- Dataset A `gt.jsonl`: **1,819 distinct process-start records after case/session de-duplication**.
- Dataset B: **15 sessions / 20,477 events**.
- B discovery: **11 recurring workflow families with explicit completion/status text**.

## 4. Process Reconstruction and Segmentation
A single inactivity threshold performs poorly because office work contains pauses, app switching and interleaving. The selected observable signal is a recurring case/task identifier visible in UI automation telemetry, combined with temporal continuity. For Dataset B, the inference path does not read ground truth because none exists.

### Dataset A validation
This validation measures whether an observable case anchor appears soon after a ground-truth process start; it is deliberately reported as an **anchor-timing diagnostic**, not as a fabricated end-to-end F1 score.

| Metric | Result |
|---|---:|
| GT process starts inspected | 1,819 |
| Starts with observable anchor after start | 1,742 |
| Anchor coverage | **95.77%** |
| Median observation lag | **4.627 s** |
| P90 observation lag | **5.517 s** |
| Within 10 s | **99.25%** |
| Within 15 s | **99.71%** |

## 5. Dataset B Process Discovery
The following counts are explicit completion/status evidence extracted from B. They are not claimed to be complete execution counts because B has no ground truth.

| Workflow evidence | Completion/status events | Sessions |
|---|---:|---:|
| Expense review | **177** | **15** |
| Inventory adjustment | 31 | 8 |
| Invoice reconciliation | 29 | 8 |
| Contract management | 28 | 7 |
| Purchase order | 26 | 8 |
| Attendance review | 23 | 6 |
| Onboarding check | 22 | 9 |
| Payment processing | 21 | 5 |
| IT request | 21 | 5 |
| Payroll change | 16 | 6 |
| Benefits request | 12 | 4 |

## 6. Automation Opportunity Ranking
The screening score is explainable rather than frequency-only. It combines observed repetition/session reach with a standardization proxy and explicit feasibility/risk assumptions. The last two are **engineering assumptions**, not measured production facts.

Top screening results:
1. **Expense review — 95.7**
2. Inventory adjustment — 54.2
3. Attendance review — 52.1
4. Purchase order — 51.7
5. Onboarding check — 50.7
6. Invoice reconciliation — 49.6

## 7. Selected Automation Candidate
### Expense Compliance Pre-check
The prototype targets the **pre-approval compliance check**, not final approval or payment.

Observed workflow pattern:
1. Open/read policy material.
2. Inspect expense category and amount.
3. Determine whether the expense is within the configured threshold.
4. Record/approve or escalate.

The scope has high repetition, visible rule structure and a clean automation boundary. A production version could integrate with the expense system through an API if available; the current prototype deliberately avoids claiming access to internal systems.

## 8. Prototype Architecture
```text
Expense text / structured record
          |
          v
   Fact extraction
   (category, amount)
          |
          v
 Versioned policy rules
          |
     +----+----+
     |         |
 within     exceeds / unknown
     |         |
     v         v
pre-check   HUMAN REVIEW
```

The prototype is deterministic. No LLM is required for arithmetic or policy comparison. AI could later help interpret unstructured policy documents, but final approval logic should remain deterministic and auditable.

## 9. Human-in-the-Loop
- **Automated:** extraction and deterministic pre-check when required fields and policy are known.
- **Human:** ambiguous policy, missing fields, exceptional categories and final approval.
- **Escalation:** any amount above the configured threshold or an unrecognized category.

## 10. Impact
Observed data establishes repetition, not production savings. Test-environment dwell time may differ from production, so absolute time savings should not be claimed from these logs alone. A production ROI study should measure actual handling time, exception rate, approval rate and API/integration feasibility before deployment.

## 11. Risks → Evidence → Impact → Mitigation
**Incorrect policy rule →** repeated policy-document consultation and threshold-sensitive examples → false approval risk → version rules, attach policy version to each decision, require human review for exceptions.

**Telemetry incompleteness →** screen text is sparse and `text_input_complete` is unreliable → missing facts can lower confidence → use multiple event sources and escalate low-confidence cases.

**UI/system change →** workflows cross browser and desktop applications → brittle UI automation can fail → prefer APIs, monitor selectors, test representative variants, retain manual fallback.

**Process variants →** B shows multiple categories and handling patterns → one rigid path can mis-handle cases → parameterize rules and route exceptions to humans.

**Governance/privacy →** logs contain operational and potentially sensitive employee/business information → inappropriate automation can create compliance risk → least-privilege access, audit logs, retention controls and explicit approval ownership.

## 12. Limitations
- Dataset B has no ground truth, so process discovery is evidence-based rather than formally scored.
- The current B segment output is an **observable-anchor candidate segmentation**, not a claim of perfect business-boundary recovery.
- Production APIs, authentication and authoritative system state were not provided.
- Production waiting times may differ from the test environment.

## 13. Reproducibility
```bash
python scripts/run_pipeline.py --dataset-a /path/to/dataset_a --dataset-b /path/to/dataset_b --out outputs
python scripts/evaluate_a.py --dataset-a /path/to/dataset_a --out outputs/a_anchor_evaluation.json
python scripts/validate_outputs.py
pytest -q
python prototype/expense_checker.py
```

## 14. Development Allocation
The repository worklog records the actual investigation and validation sequence. The implementation intentionally separates observed evidence from assumptions and documents the remaining segmentation limitations rather than overstating accuracy.

## 15. Differentiator
The project is not just “cluster the logs and automate the most frequent task.” The differentiator is a **confidence-aware bridge from telemetry to automation readiness**: use observable workflow fingerprints to identify repeated work, separate observed evidence from engineering assumptions, and automate only the deterministic portion while routing exceptions to humans.
