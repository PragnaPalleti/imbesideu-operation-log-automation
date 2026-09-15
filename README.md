# From Operation Logs to Automation

## Objective
Recover business work units from desktop/browser telemetry, discover repetitive work, and demonstrate a safe automation candidate.

## Evidence base
Dataset A contains 63 sessions and ground truth; Dataset B contains 15 sessions and no ground truth. Raw logs include application switches, keystrokes, browser events, clipboard events, context, and sparse extracted screen text.

## Approach
The segmentation pipeline uses observable workflow anchors (recurring case/task identifiers), temporal continuity, and workflow-family labels. Ground truth is used only for evaluation on A; it is never consumed by the B inference path.

## Prototype
`prototype/expense_checker.py` demonstrates a deterministic, human-in-the-loop expense compliance checker: structured expense facts are extracted, policy thresholds are applied deterministically, and exceptions are routed to human review. This is a prototype/mock decision layer, not a production integration.

## Outputs
- `outputs/segments.jsonl` — B inferred segments
- `outputs/b_process_summary.csv` — observed B workflow completion evidence
- `outputs/validation.json` — output validation

## Run
```bash
python scripts/validate_outputs.py
pytest -q
python prototype/expense_checker.py
```

## Limitations
The provided logs do not expose production APIs or authoritative business-system state. Absolute production savings should therefore be estimated conservatively; test-environment dwell times should be compared across processes rather than treated as production timings.

## Validation snapshot
The current generated outputs cover all 15 Dataset B sessions and validate as 120 candidate segments. Dataset A anchor diagnostics are stored in `outputs/a_anchor_evaluation.json` and are explicitly separated from B inference.
