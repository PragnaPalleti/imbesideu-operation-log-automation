import json
from pathlib import Path

def test_segments_schema():
    rows=[json.loads(x) for x in Path('outputs/segments.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    assert rows
    assert all({'session_id','start','end','label'} <= set(r) for r in rows)

def test_all_b_sessions_present():
    rows=[json.loads(x) for x in Path('outputs/segments.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    assert len({r['session_id'] for r in rows})==15
