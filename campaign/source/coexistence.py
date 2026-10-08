"""Guarded coexistence of independently accepted P09 and P10 host additions.

P09 owns final-room drawing. Route P10's completed-world marker through that
owner rather than replacing it. Both post-flush callbacks remain after dirty=0.
"""
from pathlib import Path
from source_tools import methods
from source_derivation import merge,replace
import p10_activation

def apply(output,selectors):
 # The accepted P10 patch requires the pre-P09 drawWorld text. Present that
 # one method to its guarded transformer, then restore the accepted P09 method
 # and compose its successful draw callback explicitly.
 before=output.copy()
 p09draw=methods(output['main.sc'])['drawWorld']
 old='(if (and p08 (>= (p08 h8V: 1 0) 5)) (p08 h8VD:) (return 1))'
 new='(if (and p08 (>= (p08 h8V: 1 0) 5)) (if p09 (return (p09 h9Draw:)) else (p08 h8VD:) (return 1)))'
 output['main.sc']=merge(output['main.sc'],{'drawWorld':replace(p09draw,new,old)})
 output,selectors=p10_activation.apply(output,selectors)
 output['main.sc']=merge(output['main.sc'],{'drawWorld':p09draw})
 draw=methods(output['module990.sc'])['h9Draw']
 draw=replace(draw,'(= result ((h9Host p08?) h8VD:))','(= result ((h9Host p08?) h8VD:))\n (if result ((ScriptID 992 0) h10Frame: 2))')
 output['module990.sc']=merge(output['module990.sc'],{'h9Draw':draw})
 for name,source in before.items():
  if name not in ('main.sc','module990.sc','module992.sc'):assert output[name]==source,('unexpected coexistence change',name)
 for name,body in methods(before['module990.sc']).items():
  if name!='h9Draw':assert methods(output['module990.sc'])[name]==body,('P09 drift',name)
 return output,selectors
