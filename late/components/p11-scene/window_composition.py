"""Append P11 data to the exact accepted P10 window composition; no window widening."""
from pathlib import Path
H=Path(__file__).resolve().parent
import extend_dialogue as ext

def predecessor():
    return (H/'inputs/window-primitive/p10-window-module982.sc').read_text()

def generate():
    before=predecessor();after,contract=ext.apply_source(before)
    path=H/'generated/window-src';path.mkdir(exist_ok=True)
    for p in (H/'generated/src').glob('*.sc'):(path/p.name).write_bytes(p.read_bytes())
    (path/'module982.sc').write_text(after)
    (H/'generated/window-predecessor.sc').write_text(before)
    return before,after
if __name__=='__main__':generate()
