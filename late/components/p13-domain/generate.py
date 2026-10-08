"""Portable derivation of the exact accepted current P13 source and schema."""
from pathlib import Path
import subprocess,sys,shutil
H=Path(__file__).resolve().parent
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_inputs import verify
verify()
D=H/'reference/component/stock-sci/p13-domain-adapter'
for script in ['reference/component/tools/generate_fixture.py','reference/component/stock-sci/p13-domain-adapter/generate.py']:
 subprocess.run([sys.executable,'-B',str(H/script)],check=True,cwd=H)
for n in ['manifest.json','src/module995.sc']:shutil.copyfile(D/n,H/n)
from verify_source import verify
print(verify())
