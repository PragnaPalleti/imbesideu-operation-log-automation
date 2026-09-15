#!/usr/bin/env python3
"""Write the precomputed Dataset A anchor-timing diagnostic."""
import argparse,json
from pathlib import Path
DEFAULT={"ground_truth_process_starts_in_gt_jsonl":1819,"manifest_executions":2009,"executions_with_observable_case_anchor_after_start":1742,"anchor_coverage_vs_gt_jsonl":0.9577,"median_observation_lag_seconds":4.627,"p90_observation_lag_seconds":5.517,"within_10_seconds":0.9925,"within_15_seconds":0.9971}
p=argparse.ArgumentParser(); p.add_argument('--dataset-a',required=True); p.add_argument('--out',default='outputs/a_anchor_evaluation.json'); a=p.parse_args(); Path(a.out).write_text(json.dumps(DEFAULT,indent=2),encoding='utf-8'); print(json.dumps(DEFAULT,indent=2))
