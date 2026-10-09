#!/usr/bin/env python3
"""Run each bounded case in a new Python process; stop at first failure."""
from pathlib import Path
import os,subprocess,sys
H=Path(__file__).resolve().parent
cases=sys.argv[1:]or['transports','guards','startup','held','running','finite']
for case in cases:
 p=subprocess.run([sys.executable,'-u',str(H/'run_emitted.py'),case],env=os.environ.copy())
 if p.returncode:raise SystemExit(p.returncode)
