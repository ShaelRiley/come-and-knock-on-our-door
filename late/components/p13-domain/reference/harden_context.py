"""NEW proven current-owner admission correction; historical bytes stay exact."""
from pathlib import Path
W=Path(__file__).resolve().parent;C=W/'component';D=C/'stock-sci/p13-domain-adapter'
p=C/'cakood/p13_model.py';s=p.read_text();old='or g.peg_available and not g.tested or g.peg_engaged and not (g.peg_available and g.gate_open)):'
new='or g.peg_available and not g.tested or g.peg_engaged and not (g.peg_available and g.gate_open)\n                    # NEW current P04 owner invariant, independently contrasted.\n                    or g.wedge_in_gate and (g.peg_engaged or not g.gate_open)):'
if s.count(old)!=1:raise RuntimeError('Expected exact literal gate anchor')
p.write_text(s.replace(old,new))
p=D/'generate.py';s=p.read_text();old='(and pegEngaged (not (and pegAvailable gateOpen)))) (= p13Code CODE_INVALID_CONTEXT)';new='(and pegEngaged (not (and pegAvailable gateOpen))) (and wedgeInGate (or pegEngaged (not gateOpen)))) (= p13Code CODE_INVALID_CONTEXT)'
if s.count(old)!=1:raise RuntimeError('Expected exact source gate anchor')
p.write_text(s.replace(old,new))
p=D/'tests/test_domain.py';s=p.read_text();old="h.v.call('p13Handoff',103,2,1,8,1,1,42,66,3,1,1,1,1,1,0,0,13)";new="h.v.call('p13Handoff',oid('hotpot_pot'),M['rooms'][KITCHEN],1,8,1,1,oid('folded_display'),oid('handcart'),M['rooms'][SIDE],1,1,1,1,1,0,0,13)"
if s.count(old)!=1:raise RuntimeError('Expected historical cart66 test anchor')
p.write_text(s.replace(old,new))
print('Current P04 context guard and current ABI exhaustion fixture applied')
