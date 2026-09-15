"""Observable-anchor segmentation for Dataset B.
Uses recurring Pn case/task identifiers from raw UI telemetry, not ground truth.
"""
import re
CASE_RE=re.compile(r"\bP\d+-\d{6,8}-\d{3}\b")
def label_for_case(case_id): return "workflow_"+case_id.split("-")[0].lower()
