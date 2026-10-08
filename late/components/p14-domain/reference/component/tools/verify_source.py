"""NEW exact retained-method, current-ABI and declared-delta source admission."""
from pathlib import Path
import hashlib,json,sys
C=Path(__file__).resolve().parents[1];W=C.parent;D=C/'stock-sci/p14-domain-adapter'
sys.path.insert(0,str(C))
from dependencies.source_tools import methods

def verify():
 original=W/'historical/literal-final/stock-sci/p14-domain-adapter'
 for name in ('codec.py','src/methods.sc.in'):
  if (D/name).read_bytes()!=(original/name).read_bytes():raise RuntimeError('Changed retained source: '+name)
 raw=(W/'historical/literal-read/cakood/p14_model.py').read_text()
 old="""        self.entry_flags=sorted(PREREQUISITES)
        self.winning_attempts={encounter:next(a.outcome.id for a in c.contests.attempts
            if a.encounter_id==encounter and a.outcome is not None and a.outcome.winner=='jack') for encounter in CONTEST_IDS}
"""
 new="""        # NEW current-owner ABI admission: collect every genuine observation
        # before mutating durable state; aggregate-only saves cannot supply it.
        winning_attempts={encounter:next(a.outcome.id for a in c.contests.attempts
            if a.encounter_id==encounter and a.outcome is not None and a.outcome.winner=='jack') for encounter in CONTEST_IDS}
        self.entry_flags=sorted(PREREQUISITES)
        self.winning_attempts=winning_attempts
"""
 if raw.count(old)!=1 or (C/'cakood/p14_model.py').read_text()!=raw.replace(old,new):raise RuntimeError('Unlabeled P14 model delta')
 m=json.loads((D/'manifest.json').read_text())
 for field,path in [('model_sha256',C/'cakood/p14_model.py'),('fixture_sha256',C/'tests/fixtures/p14/canonical-bindings.json'),('source_sha256',D/'src/module996.sc')]:
  if hashlib.sha256(path.read_bytes()).hexdigest()!=m[field]:raise RuntimeError('Stale generated source '+field)
 original_methods=methods((original/'src/methods.sc.in').read_text());generated=methods((D/'src/module996.sc').read_text())
 for name,text in original_methods.items():
  if generated.get(name)!=text:raise RuntimeError('Retained SCI method differs: '+name)
 if len(m['all_properties'])!=669 or len(m['persisted_properties'])!=642 or len(m['serials'])!=202:raise RuntimeError('P14 finite layout changed')
 for k,v in [('handcart',72),('folded_display',42),('completed_screen',81),('hotpot_pot',92),('pledge_board',433)]:
  if m['objects'][k]!=v:raise RuntimeError('Current host ABI mismatch '+k)
 return {'status':'PASS','retained_methods':len(original_methods),'properties':669,'persisted':642,'serials':202,'scope':'Exact retained SCI methods and codec, no compilation'}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
