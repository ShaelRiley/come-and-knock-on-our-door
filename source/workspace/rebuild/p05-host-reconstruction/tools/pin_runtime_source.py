from pathlib import Path
import urllib.request,hashlib,json,tarfile,re
H=Path(__file__).resolve().parents[1];R=H.parent/'runtime';E=H/'evidence/scummvm-2026.3.0'
page=(R/'evidence/scummvm-downloads.txt').read_text();url='https://downloads.scummvm.org/frs/scummvm/2026.3.0/scummvm-2026.3.0.tar.xz'
m=re.search(re.escape(url+'.sha256')+r'">([a-f0-9]{64})',page);assert m
expected=m[1];archive=Path('/tmp/cakood-scummvm-2026.3.0-source.tar.xz')
if not archive.exists():
 with urllib.request.urlopen(url,timeout=45) as stream,archive.open('wb') as out:
  while True:
   data=stream.read(1024*1024)
   if not data:break
   out.write(data)
h=hashlib.sha256()
with archive.open('rb') as f:
 for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
assert h.hexdigest()==expected,(h.hexdigest(),expected)
rows={}
with tarfile.open(archive,'r:xz') as t:
 for name in ['sci.cpp','savegame.cpp','kevent.cpp','vm.cpp','kgraphics.cpp','ksound.cpp']:
  suffix='engines/sci/'+('sci.cpp' if name=='sci.cpp' else 'engine/'+name)
  found=[m for m in t.getmembers() if m.name.endswith('/'+suffix)];assert len(found)==1
  data=t.extractfile(found[0]).read();assert data==(E/name).read_bytes(),(name,'release/tag differs')
  rows[name]=dict(source_member=found[0].name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),tag_source='https://raw.githubusercontent.com/scummvm/scummvm/v2026.3.0/'+suffix)
exe=R/'stock-scummvm/usr/games/scummvm';pin=hashlib.sha256(exe.read_bytes()).hexdigest();assert pin=='050ed72eba6fd5760d87a3decc5425d74760115b2d77a71f5c6876aa1f96e0ad'
report=dict(status='VERIFIED_OFFICIAL_RELEASE_SOURCE_AND_RUNTIME_PIN',version='2026.3.0',official_source_url=url,official_source_sha256=expected,source_archive_bytes=archive.stat().st_size,runtime_executable_sha256=pin,package_sha256='26c66d5ff8d7a4c26d95ee68b602ee3b51d7db74be528d749e1627c2e5d678bc',sources=rows,binary_reproducible_build_claim=False,native_test=False)
(E/'PROVENANCE.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
