"""Reads the saved NASA PSI FLEX table (data/raw) and writes data/derived/summary.json + site/data.js.
Run: python3 -I scripts/analyze.py   (from the project folder). Pure standard library."""
import csv, json, collections
RAW='data/raw/PSI-69_FLEX_experimental_table.csv'
PC='Ambient pressure; mmHg'; OC='O initial ambient composition; mole fraction'
MMHG_PER_PSI=51.7149   # 1 psi = 51.7149 mmHg
LIMIT_PSI=10.2; MIN_O2=0.30   # challenge text: ">=30% oxygen at <=10.2 psi" (Flame in Freefall page)
rows=[]; skipped=[]
for x in csv.DictReader(open(RAW,encoding='cp1252')):
    p=float(x[PC])
    if p<=0: skipped.append(x['FLEX Identifier']); continue   # 0 mmHg is a missing value
    rows.append(dict(id=x['FLEX Identifier'],test=int(x['FLEX Test #']),fuel=x['Fuel'],o2=float(x[OC]),
        mmhg=p,psi=round(p/MMHG_PER_PSI,3),end=x['Test end'],date=x['Test Date']))
hi=[r for r in rows if r['o2']>=MIN_O2]
inside=[r for r in hi if r['psi']<=LIMIT_PSI]
near=[r for r in hi if r['psi']<12]          # the cluster just above the limit
ends=lambda L:dict(collections.Counter(r['end'] for r in L))
summary=dict(total_rows=len(rows)+len(skipped),used=len(rows),skipped_missing_pressure=skipped,
  limit_psi=LIMIT_PSI,limit_mmhg=round(LIMIT_PSI*MMHG_PER_PSI,1),min_o2=MIN_O2,
  n_o2_ge_30=len(hi),n_inside_box=len(inside),
  n_near=len(near),near_psi_min=min(r['psi'] for r in near),near_psi_max=max(r['psi'] for r in near),
  near_o2_values=sorted(set(r['o2'] for r in near)),near_outcomes=ends(near),
  other_ge30_psi_range=[min(r['psi'] for r in hi if r['psi']>=12),max(r['psi'] for r in hi if r['psi']>=12)],
  all_outcomes=ends(rows),lt30_outcomes=ends([r for r in rows if r['o2']<MIN_O2]),
  ge30_outcomes=ends(hi),lowest_pressure_any_test_psi=min(r['psi'] for r in rows))
import os; os.makedirs('data/derived',exist_ok=True); os.makedirs('site',exist_ok=True)
json.dump(summary,open('data/derived/summary.json','w'),indent=1)
open('site/data.js','w').write('window.FLEX='+json.dumps(rows)+';\nwindow.SUMMARY='+json.dumps(summary)+';\n')
print(json.dumps(summary,indent=1))
