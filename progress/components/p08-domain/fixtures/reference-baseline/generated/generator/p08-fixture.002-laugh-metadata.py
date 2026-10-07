# Preserve exact editorial reaction provenance without allocating laugh triggers.
p='tests/fixtures/p08/canonical-bindings.json'
u=json.load(open('inputs/authority/speech-units.json'))['units']
f['editorial_laugh_metadata']={x['line_id']:x['laugh_opportunity'] for x in u if x['record_id'].startswith('P08.') and x.get('laugh_opportunity')}
open(p,'w').write(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
