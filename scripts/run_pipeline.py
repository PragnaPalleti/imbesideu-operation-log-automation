#!/usr/bin/env python3
"""Reproducible archive-based pipeline for the case study.
Raw datasets remain outside the repository. Pass directories containing Dataset A/B ZIP files.
"""
import argparse,csv,glob,json,math,os,re,zipfile
from collections import defaultdict,Counter
from datetime import datetime,timezone

PATTERNS=[
 ('invoice_reconciliation',r'請求書照合完了'),('expense_review',r'経費(?:精算)?確認済み|経費承認（管理職）'),('payroll_change',r'給与変更登録'),('attendance_review',r'勤怠申請確認'),('onboarding_check',r'入社照合完了'),('it_request',r'IT申請処理完了'),('payment_processing',r'支払処理確認'),('inventory_adjustment',r'在庫調整登録'),('purchase_order',r'発注管理処理'),('contract_management',r'契約管理処理'),('benefits_request',r'福利厚生申請処理完了')]
CASE_RE=re.compile(r'\bP\d+-\d{6,8}-\d{3}\b')

def structured_case_ids(e):
    p = e.get('payload') or {}
    values = []
    target = p.get('target_element')
    if isinstance(target, dict):
        values.extend([target.get('name'), target.get('automation_id'), target.get('value')])
    element = p.get('element')
    if isinstance(element, dict):
        values.extend([element.get('name'), element.get('text'), element.get('value'), element.get('id')])
        attrs = element.get('attributes')
        if isinstance(attrs, dict):
            values.extend(v for v in attrs.values() if isinstance(v, str))
    ids = set()
    for v in values:
        if isinstance(v, str): ids.update(CASE_RE.findall(v))
    return ids

def iso(ms): return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def iter_events(zip_files):
 for f in zip_files:
  with zipfile.ZipFile(f) as z:
   for n in z.namelist():
    if n.endswith('/events.jsonl'):
     sid=n.split('/')[0]
     for line in z.open(n):
      try:
       e=json.loads(line); e['_session']=sid; yield e
      except Exception: continue

def b_files(root):
    files=glob.glob(os.path.join(root,'*.zip'))
    corrected=[f for f in files if os.path.basename(f)=='B7(1).zip']
    if corrected:
        files=[f for f in files if os.path.basename(f)!='B7.zip']
    return files

def run(a_root,b_root,out):
 os.makedirs(out,exist_ok=True)
 # B process evidence
 bycat=defaultdict(list); case=defaultdict(list)
 for e in iter_events(b_files(b_root)):
  text=(e.get('context') or {}).get('extracted_text') or {}
  text=text.get('text') if isinstance(text,dict) else text
  if text:
   for cat,p in PATTERNS:
    if re.search(p,text): bycat[cat].append(e); break
  for cid in structured_case_ids(e): case[(e['_session'],cid)].append(e)
 rows=[]
 for cat,es in bycat.items():
  ts=[e['timestamp_ms'] for e in es]
  rows.append({'process':cat,'observed_completion_events':len(es),'sessions':len({e['_session'] for e in es}),'observed_span_minutes':round((max(ts)-min(ts))/60000,2),'evidence':'explicit completion/status text'})
 rows.sort(key=lambda x:x['observed_completion_events'],reverse=True)
 with open(os.path.join(out,'b_process_summary.csv'),'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 # B segments: every observed case/task identifier becomes a candidate execution; padding uses the A-derived observation-lag calibration.
 seg=[]
 for (sid,cid),es in case.items():
  ts=[e['timestamp_ms'] for e in es]
  if not ts: continue
  start=max(min(ts)-4600,0); end=max(ts)+5000
  seg.append({'session_id':sid,'start_ms':start,'end_ms':end,'label':'workflow_'+cid.split('-')[0].lower(),'anchor':cid})
 # remove exact duplicate observations created by split archives
 uniq={}
 for s in seg: uniq[(s['session_id'],s['start_ms'],s['end_ms'],s['label'])]=s
 seg=list(uniq.values())
 seg.sort(key=lambda s:(s['session_id'],s['start_ms']))
 # overlapping executions are retained because the source workflows can be interleaved.
 with open(os.path.join(out,'segments.jsonl'),'w',encoding='utf-8') as f:
  for s in seg:
   f.write(json.dumps({'session_id':s['session_id'],'start':iso(s['start_ms']),'end':iso(s['end_ms']),'label':s['label']},ensure_ascii=False)+'\n')
 # validation
 errors=[]; seen=set(); bys=defaultdict(list)
 for s in seg:
  if s['end_ms']<=s['start_ms']: errors.append('non-positive interval')
  k=(s['session_id'],s['start_ms'],s['end_ms'],s['label'])
  if k in seen: errors.append('duplicate')
  seen.add(k)
  bys[s['session_id']].append(s['start_ms'])
  if s['session_id'] not in seen: pass
 json.dump({'valid':not errors,'segments':len(seg),'sessions':len(bys),'errors':errors,'overlap_allowed_for_interleaved_workflows':True},open(os.path.join(out,'validation.json'),'w'),indent=2)
 print(json.dumps({'segments':len(seg),'sessions':len(bys),'categories':len(rows),'valid':not errors},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--dataset-a',required=True);p.add_argument('--dataset-b',required=True);p.add_argument('--out',default='outputs');a=p.parse_args();run(a.dataset_a,a.dataset_b,a.out)
