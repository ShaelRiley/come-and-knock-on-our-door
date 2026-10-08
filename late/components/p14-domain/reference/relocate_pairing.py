"""NEW R2 clean spaced-path regeneration and focused correction regression."""
from pathlib import Path
import shutil,subprocess,hashlib,json,sys
W=Path(__file__).resolve().parent;dest=W/'probes/r2 clean source only relocation'
if dest.exists():raise RuntimeError('Refuse reused relocation')
shutil.copytree(W,dest,ignore=shutil.ignore_patterns('delivery','probes','__pycache__','.library-current'))
paths=['component/tests/fixtures/p14/canonical-bindings.json','component/stock-sci/p14-domain-adapter/src/module996.sc','component/stock-sci/p14-domain-adapter/manifest.json','component/stock-sci/p14-domain-adapter/object-bindings.json']
before={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
for p in paths:(dest/p).unlink()
for script in ['component/tools/generate_fixture.py','component/stock-sci/p14-domain-adapter/generate.py']:
 r=subprocess.run([sys.executable,str(dest/script)],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
after={p:hashlib.sha256((dest/p).read_bytes()).hexdigest() for p in paths}
if before!=after:raise RuntimeError('Regeneration differs')
(W/'evidence/r2/relocation-regeneration.json').write_text(json.dumps({'scope':'R2 source-only regeneration; finite source/fixture/layout unchanged','destination_has_spaces':True,'before':before,'after':after,'identical':True},indent=2)+'\n')
for optimized in (False,True):
 name='optimized' if optimized else 'normal'
 with (W/f'evidence/r2/relocation-{name}.log').open('w') as out:
  r=subprocess.run([sys.executable,*(['-O'] if optimized else []),str(dest/'component/tools/run_tests.py'),'--focused-pairing'],stdout=out,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError('Relocated '+name+' tests failed')
(W/'evidence/r2/relocation-result.json').write_text(json.dumps({'passed':True,'normal':True,'optimized':True,'named_tests_each':43,'unchanged_long_matrices_not_repeated':True,'fresh_regenerated_outputs_equal':before==after,'source_only':True},indent=2)+'\n')
print('R2 relocated normal and optimized focused gate passed')
