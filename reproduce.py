#!/usr/bin/env python3
from pathlib import Path
import argparse, subprocess, sys
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description="Reproduce the exact tested five-puzzle game without network or native launch")
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
check=subprocess.run([sys.executable,str(root/"source/verify_archive.py")])
if check.returncode: raise SystemExit(check.returncode)
raise SystemExit(subprocess.run([sys.executable,str(root/"source/rebuild.py"),"--out",str(a.out.resolve())]).returncode)
