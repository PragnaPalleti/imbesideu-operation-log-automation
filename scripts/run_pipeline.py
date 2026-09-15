#!/usr/bin/env python3
"""Reproducible archive-based pipeline for the case study.
Raw datasets remain outside the repository. Pass directories containing Dataset A/B ZIP files.
"""
import argparse,csv,glob,json,os,re,zipfile
from collections import defaultdict
from datetime import datetime,timezone
PATTERNS=[('invoice_reconciliation',r'請求書照合完了'),('expense_review',r'経費(?:精算)?確認済み|経費承認（管理職）'),('payroll_change',r'給与変更登録'),('attendance_review',r'勤怠申請確認'),('onboarding_check',r'入社照合完了'),('it_request',r'IT申請処理完了'),('payment_processing',r'支払処理確認'),('inventory_adjustment',r'在庫調整登録'),('purchase_order',r'発注管理処理'),('contract_management',r'契約管理処理'),('benefits_request',r'福利厚生申請処理完了')]
CASE_RE=re.compile(r'\bP\d+-\d{6,8}-\d{3}\b')
def iso(ms): return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def iter_events(zip_files):
 for f in zip_files:
  with zipfile.ZipFile(f) as z:
   for n in z.namelist():
    if n.endswith('/events.jsonl'):
     sid=n.split('/')[0]
     for line in z.open(n):
      try: e=json.loads(line); e['_session']=sid; yield e
      except Exception: continue
def b_files(root): return [f for f in glob.glob(os.path.join(root,'*.zip'))]
def run(a_root,b_root,out):
 os.makedirs(out,exist_ok=True); bycat=defaultdict(list); case=defaultdict(list)
 for e in iter_events(b_files(b_root)):
  text=(e.get('context') or {}).get('extracted_text') or {}; text=text.get('text') if isinstance(text,dict) else text
  if text:
   for cat,p in PATTERNS:
    if re.search(p,text): bycat[cat].append(e); break
  for cid in set(CASE_RE.findall(json.dumps(e,ensure_ascii=False))): case[(e['_session'],cid)].append(e)
 rows=[]
 for cat,es in bycat.items():
  ts=[e['timestamp_ms'] for e in es]; rows.append({'process':cat,'observed_completion_events':len(es),'sessions':len({e['_session'] for e in es}),'observed_span_minutes':round((max(ts)-min(ts))/60000,2),'evidence':'explicit completion/status text'})
 rows.sort(key=lambda x:x['observed_completion_events'],reverse=True)
 with open(os.path.join(out,'b_process_summary.csv'),'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
 seg=[]
 for (sid,cid),es in case.items():
  ts=[e['timestamp_ms'] for e in es]
  if ts: seg.append({'session_id':sid,'start_ms':max(min(ts)-4600,0),'end_ms':max(ts)+13400,'label':'workflow_'+cid.split('-')[0].lower(),'anchor':cid})
 uniq={ (s['session_id'],s['start_ms'],s['end_ms'],s['label']):s for s in seg }; seg=sorted(uniq.values(),key=lambda s:(s['session_id'],s['start_ms']))
 with open(os.path.join(out,'segments.jsonl'),'w',encoding='utf-8') as f:
  for s in seg: f.write(json.dumps({'session_id':s['session_id'],'start':iso(s['start_ms']),'end':iso(s['end_ms']),'label':s['label']},ensure_ascii=False)+'\n')
 errors=[]; seen=set(); bys=defaultdict(list)
 for s in seg:
  if s['end_ms']<=s['start_ms']: errors.append('non-positive interval')
  k=(s['session_id'],s['start_ms'],s['end_ms'],s['label'])
  if k in seen: errors.append('duplicate')
  seen.add(k); bys[s['session_id']].append(s['start_ms'])
 json.dump({'valid':not errors,'segments':len(seg),'sessions':len(bys),'errors':errors,'overlap_allowed_for_interleaved_workflows':True},open(os.path.join(out,'validation.json'),'w'),indent=2)
 print(json.dumps({'segments':len(seg),'sessions':len(bys),'categories':len(rows),'valid':not errors},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--dataset-a',required=True); p.add_argument('--dataset-b',required=True); p.add_argument('--out',default='outputs'); a=p.parse_args(); run(a.dataset_a,a.dataset_b,a.out)
