#!/usr/bin/env python3
"""One focused real-host bytecode lifecycle under a declared nonzero work clock."""
from pathlib import Path
import copy,gc,hashlib,json,resource,time,traceback
from finite_vm import FiniteVM,RestoreTransfer,EndOfEvents,H

def check(value,message):
 if not value:raise AssertionError(message)
def tick(v,count=6,event=None):
 v.advance(count)
 v.pump([{} if event is None else event],tick=0)
def diag(v):
 if isinstance(v,dict):return v['observation']
 h=v.objects['cakood'];s=v.objects['responsiveSound'];p=v.parsers.get(s,{})
 return dict(now=v.now,card=h.p['creditCard'],tick=h.p['creditElapsed'],held=h.p['creditHeld'],opening=h.p['opening'],initialized=h.p['initialized'],initCount=h.p['initCount'],uiFailure=h.p['uiFailure'],host_unavailable=h.p['musicUnavailable'],director=[v.proc('psRead',i)for i in(0,1,2,3,4,6,7)],broker=[v.proc('rbStatus',i)for i in(0,1,2,3,4,5,7,8)],native_tick=p.get('tick'),native_pauses=p.get('pauses'),native_gain=p.get('volume'))
def observed(v):return v.proc('psOpeningPosition',v.objects['cakood'])
def restore(v,snapshot):
 v.load_snapshot=snapshot
 try:v.objects['cakood'].call('readSave')
 except RestoreTransfer as transfer:z=transfer.vm
 else:raise AssertionError(('Load did not reach native RestoreGame',diag(v)))
 try:z.objects['cakood'].call('replay')
 except EndOfEvents:pass
 z.event_queue=None;z.retiring_events=False;z.saves=[];z.load_snapshot=None
 return z

