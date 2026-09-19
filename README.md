# From Operation Logs to an Automation Proposal

## Candidate Information

- **Full Name:** Palleti Pragna
- **University:** IIT (ISM) Dhanbad
- **Department/Major:** Mathematics and Computing
- **Email:** [REPLACE WITH EXACT ROUND-1 EMAIL]


A reproducible case-study implementation that turns desktop/browser telemetry into business-work evidence, evaluates an observable segmentation signal on Dataset A, applies the same inference principle to Dataset B, and prototypes a safe automation boundary.

## Executive summary

- **Dataset A:** 63 sessions, 162,768 raw events, 2,009 ground-truth execution records.
- **Dataset B:** 15 sessions, 20,477 raw events, no ground truth.
- **B discovery:** 11 recurring workflow families with explicit completion/status evidence.
- **B segmentation:** 86 observable-anchor candidate execution segments across all 15 sessions.
- **A anchor diagnostic:** 95.77% of de-duplicated GT process starts have an observable case anchor after the start; median observation lag 4.627 s; P90 5.517 s.
- **Top automation candidate:** expense review / compliance pre-check.

The project deliberately separates **observed evidence** from **engineering assumptions**. Dataset A ground truth is used only for evaluation; it is not used to infer Dataset B.

## Repository map

```text
.
├── ASSIGNMENT.md                 # case-study task statement
├── DATA_SCHEMA.md                # raw-data and GT schema reference
├── data/README.md                # data-handling notes
├── outputs/
│   ├── a_anchor_evaluation.json  # Dataset A anchor diagnostic
│   ├── a_process_summary.csv     # Dataset A process summary
│   ├── automation_candidates.csv # ranked B opportunities
│   ├── b_process_summary.csv     # observed B workflow evidence
│   ├── project_metrics.json      # headline metrics
│   ├── segments.jsonl            # required Dataset B deliverable
│   └── validation.json            # machine-readable validation result
├── prototype/
│   └── expense_checker.py        # deterministic HITL automation prototype
├── reports/final_report.md       # final analysis and proposal
├── scripts/
│   ├── run_pipeline.py           # archive → B segments/evidence
│   ├── evaluate_a.py             # A anchor evaluation
│   ├── generate_analysis.py      # analysis/visualization generation
│   └── validate_outputs.py       # output checks
├── src/segmentation.py           # reusable case-anchor logic
├── tests/                        # regression and prototype tests
├── visualizations/               # decision-support charts
└── worklog/worklog.md             # reasoning and failed approaches
```

Raw Dataset A/B archives are **not committed** to the repository. They are supplied separately and can be passed to the reproducible pipeline.

## Method

1. Audit session/chunk semantics and raw event types.
2. Reject inactivity-gap-only segmentation after testing it against Dataset A.
3. Identify recurring **structured interaction targets** containing case/task identifiers.
4. Calibrate observable-anchor timing on Dataset A ground truth.
5. Apply the same evidence-first inference path to Dataset B without ground truth.
6. Profile repetition, session reach, handling patterns and observable completion evidence.
7. Rank automation opportunities using an explainable screening score.
8. Build a deterministic expense-compliance pre-check with human escalation.

A key design choice is to avoid extracting case IDs from broad OCR/setup text: dashboard text can contain stale or unrelated workflow references. Structured interaction targets are treated as the stronger signal.

## Automation prototype

`prototype/expense_checker.py` implements a small, auditable decision layer:

- extracts expense category and amount from structured/Japanese text;
- applies a configurable policy threshold (default: ¥50,000);
- returns `AUTO_APPROVE` when the known rule is satisfied;
- routes over-threshold or ambiguous cases to `HUMAN_REVIEW` / `REVIEW`.

This is intentionally a **mock decision layer**, not a claim of production-system integration. Final approval, payment, authentication, API integration and exception ownership remain human/system responsibilities.

## Reproduce

Install dependencies:

```bash
pip install -r requirements.txt
```

Run validation and tests against the checked-in outputs:

```bash
python scripts/validate_outputs.py
pytest -q
python prototype/expense_checker.py
```

Regenerate the B analysis from supplied archives:

```bash
python scripts/run_pipeline.py \
  --dataset-a /path/to/dataset_a \
  --dataset-b /path/to/dataset_b \
  --out outputs
```

Evaluate Dataset A independently:

```bash
python scripts/evaluate_a.py \
  --dataset-a /path/to/dataset_a \
  --out outputs/a_anchor_evaluation.json
```

## What the results mean

`outputs/segments.jsonl` is a **candidate segmentation** for B, not a claim that every business boundary is perfectly recovered. Overlapping intervals are retained because the task explicitly allows workers to suspend one workflow and return to it later.

The 95.77% A result is an **anchor-timing diagnostic**, not an end-to-end segmentation F1 score. B has no ground truth, so B process counts and opportunity scores are explicitly labeled as observed evidence or engineering assumptions.

## Limitations and rollout posture

The supplied telemetry does not expose production APIs or authoritative business-system state. Therefore the repository does not claim production ROI, production timing, or production-ready automation. A production rollout should first validate API access, policy versioning, exception rates, actual handling time, auditability, retention, least-privilege permissions and manual fallback.

## Submission artifacts

The required submission artifacts are present as repository files: `outputs/segments.jsonl`, Git history, `reports/final_report.md`, and `worklog/worklog.md`. Supporting schema, analysis, validation, prototype and visualization artifacts are included so a reviewer can inspect the reasoning rather than only the final answer.

## Submission Requirements

This repository is prepared for the company's Round 2 submission. Before submission, verify that the repository is **Private**, the exact email used in the Round 1 application is entered above, and all seven reviewer accounts are invited as collaborators.

### Reviewer accounts
- yasuhironose@imbesideyou.world
- mamindla@imbesideyou.world
- jayeshahire@imbesideyou.world
- ashwingaikwad@imbesideyou.world
- namansolanki@imbesideyou.world
- kushakjafry@imbesideyou.world
- rajeevkumar@imbesideyou.world

### Required submission artifacts
- `outputs/segments.jsonl`
- Final report
- Work log

The repository should not contain the supplied raw case-study ZIP archives.
