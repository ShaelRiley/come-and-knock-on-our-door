"""Deterministic source and generated-output review bundle, no runtime deployment."""
from pathlib import Path
import json
import zipfile
import hashlib
import sys
sys.dont_write_bytecode=True
from build import check_inputs,dump,sha
H=Path(__file__).resolve().parent

def bank():
    check_inputs()
    source=[H/n for n in ['audience.py','audience-profile.json','build.py','verify.py','bank.py','README.md','tests/runtime_checks.py','INPUT-SEAL.json']]
    dump(H/'SOURCE-SEAL.json',{str(p.relative_to(H)):sha(p.read_bytes()) for p in source})
    dump(H/'OUTPUT-SEAL.json',{str(p.relative_to(H)):sha(p.read_bytes()) for root in ['generated','evidence'] for p in sorted((H/root).rglob('*')) if p.is_file()})
    members={str(p.relative_to(H)):sha(p.read_bytes()) for p in sorted(H.rglob('*')) if p.is_file() and not any(x in p.relative_to(H).parts for x in ['delivery','portability','__pycache__'])}
    out=H/'delivery/Audience-Original-Review-Component-20261007.zip';out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for name,digest in members.items():
            raw=(H/name).read_bytes()
            if sha(raw)!=digest:raise ValueError('Concurrent source change')
            info=zipfile.ZipInfo('audience-reply-audio/'+name,date_time=(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,raw)
        info=zipfile.ZipInfo('audience-reply-audio/PACKAGE-MEMBERS.json',date_time=(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
        z.writestr(info,json.dumps(members,indent=2)+'\n')
    with zipfile.ZipFile(out) as z:
        if z.testzip() is not None:raise ValueError('Invalid archive')
        for name,digest in members.items():
            if sha(z.read('audience-reply-audio/'+name))!=digest:raise ValueError('Archive roundtrip')
    receipt=dict(path=str(out.relative_to(H)),bytes=out.stat().st_size,sha256=sha(out.read_bytes()),members=len(members),status='NEW_ORIGINAL_REVIEW_CANDIDATE',native_acceptance=False,listening_performed=False)
    dump(H/'delivery/package-receipt.json',receipt);return receipt
if __name__=='__main__':print(json.dumps(bank(),indent=2))
