#!/usr/bin/env python3
import json
from pathlib import Path
p=Path('outputs/segments.jsonl')
rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
errors=[]; keys=set()
for r in rows:
    if not {'session_id','start','end','label'} <= set(r): errors.append('schema')
    k=(r.get('session_id'),r.get('start'),r.get('end'),r.get('label'))
    if k in keys: errors.append('duplicate')
    keys.add(k)
if not rows: errors.append('empty')
print(f"valid: {len(rows)} segments across {len({r['session_id'] for r in rows})} sessions")
if errors: raise SystemExit('; '.join(errors))
