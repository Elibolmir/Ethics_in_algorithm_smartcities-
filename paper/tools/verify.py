import csv,hashlib,sys,glob,os
h=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    rows=list(csv.DictReader(open(f,encoding='utf-8')))
    if not rows or 'sha256_quote' not in rows[0]: continue
    ok_q=ok_r=0; variants={}
    for r in rows:
        c,q=r['conv_id'],r['quote']
        cand={'conv||quote':h(c+q),'conv|quote':h(c+'|'+q),'quote':h(q),'conv,quote':h(c+','+q)}
        m=[k for k,v in cand.items() if v==r['sha256_quote']]
        if m: ok_q+=1; variants[m[0]]=variants.get(m[0],0)+1
        base=[r[k] for k in r if k not in('row_hash',)]
        rc={'|':h('|'.join(base)),',':h(','.join(base)),'':h(''.join(base))}
        if r['row_hash'] in rc.values(): ok_r+=1
    print(f"{os.path.basename(f)[9:]}: rows={len(rows)} quote_ok={ok_q} {variants} row_ok={ok_r}")
