"""Record answers: python3 record.py ID=CHOICE ... and/or --recs ID ID ... (takes the recommendation)."""
import json, pathlib, re, sys
p = pathlib.Path(__file__).with_name('answers.json'); a = json.loads(p.read_text())
qs = {q['id']: q for s in json.load(open(p.with_name('questions.json')))['sections'] for q in s['questions']}
args = sys.argv[1:]; recs = '--recs' in args
for x in args:
    if x == '--recs': continue
    if '=' in x:
        i, c = x.split('=', 1); a[i] = {"choice": c.split(',') if ',' in c else c, "note": ""}
    elif recs:
        q = qs[x]; r = [k for k in re.split(r'\s*,\s*', q['recommended']) if k]
        a[x] = {"choice": r if q['multi'] else r[0], "note": "took the recommendation (digest)"}
p.write_text(json.dumps(a, indent=1, ensure_ascii=False)); print(len([k for k in a if not k.startswith('_')]), "answered of", len(qs))
