"""NEW fail-closed authored source/test entrypoint admission (not authentication)."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parents[2]
def verify():
 pins=json.loads((W/'provenance/working-source-pins.json').read_text())
 for relative,h in pins.items():
  p=W/relative
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise RuntimeError('Working source missing or changed: '+relative)
 return len(pins)
