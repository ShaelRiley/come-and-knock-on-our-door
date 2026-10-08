#!/usr/bin/env python3
"""Compare a fresh relocated build, permitting only absolute ABI path labels."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    other=Path(sys.argv[1]).resolve()
    for p in ('src/module993.sc','manifest.json','build/isolated/compiled/0.scr.bin','build/isolated/compiled/0.scr.bin.hep','build/isolated/compiled/993.scr.bin','build/isolated/compiled/993.scr.bin.hep'):
        if (H/p).read_bytes()!=(other/p).read_bytes():raise ValueError('Relocated bytes differ: '+p)
    def abi(root):
        a=json.loads((root/'build/isolated/ABI-MAPPINGS.json').read_text())
        for module in a['modules'].values():
            layout=module['reference_layout']
            for f in ('script','heap'):layout[f]=str(Path(layout[f]).relative_to(root))
        return a
    if abi(H)!=abi(other):raise ValueError('Normalized relocated ABI differs')
    print('PASS_RELOCATED_SOURCE_MANIFEST_EMITTED_BYTES_ABI')
if __name__=='__main__':main()
