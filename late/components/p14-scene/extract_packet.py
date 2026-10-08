"""Extract a SHA-pinned component into a fresh directory, preserving Unix modes.

Reject traversal, duplicate paths, non-regular members, unsafe modes, mismatched
manifest membership, bytes or modes. Never guess executable bits from filenames.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re,stat,zipfile
ROOT='p14-scene-reconstruction'
def require(ok,why):
 if not ok:raise ValueError(why)
def extract(archive,destination,expected_sha256):
 archive=Path(archive);destination=Path(destination)
 require(re.fullmatch('[0-9a-f]{64}',expected_sha256),'Exact archive SHA256 required')
 require(hashlib.sha256(archive.read_bytes()).hexdigest()==expected_sha256,'Archive SHA256 mismatch')
 require(not destination.exists(),'Fresh destination required')
 with zipfile.ZipFile(archive) as z:
  entries=z.infolist();names=[e.filename for e in entries];require(len(names)==len(set(names)),'Duplicate archive path')
  mname=ROOT+'/PACKAGE-MANIFEST.json';require(mname in names,'Package manifest missing');m=json.loads(z.read(mname));require(m.get('archive_root')==ROOT,'Archive root mismatch')
  hashes=m['files'];modes=m['member_modes'];require(set(hashes)==set(modes),'Mode/member inventory mismatch')
  require(set(names)=={ROOT+'/'+n for n in hashes}|{mname},'Archive member inventory mismatch')
  for e in entries:
   p=PurePosixPath(e.filename);require(not p.is_absolute() and '..' not in p.parts and '\\' not in e.filename and p.as_posix()==e.filename and p.parts[0]==ROOT,'Unsafe archive path')
   raw=e.external_attr>>16;mode=stat.S_IMODE(raw);require(e.create_system==3 and stat.S_IFMT(raw)==stat.S_IFREG and not mode&0o7022,'Unsafe archive mode/type')
   relative='/'.join(p.parts[1:]);expected_mode=m['manifest_mode'] if e.filename==mname else modes[relative]
   require(type(expected_mode) is int and mode==expected_mode,'Archive member mode mismatch '+relative)
   if e.filename!=mname:require(hashlib.sha256(z.read(e)).hexdigest()==hashes[relative],'Archive member hash mismatch '+relative)
  destination.mkdir(parents=True)
  for e in entries:
   target=destination/Path(*PurePosixPath(e.filename).parts);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(e));target.chmod(stat.S_IMODE(e.external_attr>>16))
   require(stat.S_IMODE(target.stat().st_mode)==stat.S_IMODE(e.external_attr>>16),'Extracted mode mismatch')
 return destination/ROOT
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('destination');p.add_argument('--sha256',required=True);a=p.parse_args();print(extract(a.archive,a.destination,a.sha256))
