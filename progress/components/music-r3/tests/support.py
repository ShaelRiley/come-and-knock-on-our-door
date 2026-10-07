from pathlib import Path
import sys,copy,json,unittest
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tools')]
from music_vm import MusicVM
from host_vm import VMError
class Scenario(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.base=MusicVM();v=cls.base
  if v.proc('rbInit',v.objects['responsiveSound'],v.objects['musicTransport'],0,17061)!=1:raise RuntimeError('Failed actual emitted startup')
  for _ in range(3):v.advance(2);v.poll()
  if v.objects['homeReadyTransport'].p['transportMode']!=2:raise RuntimeError('Startup guard did not open')
 def vm(self):
  v=copy.deepcopy(self.base);v.steps=0;return v
 def contest_vm(self):
  cls=type(self)
  if not hasattr(cls,'_contest_base'):
   v=self.vm();self.enter(v);v.proc('rbRetire');self.assertEqual(v.proc('rbStartBed',152),1)
   self.tick(v,6);cls._contest_base=v
  v=copy.deepcopy(cls._contest_base);v.steps=0;return v
 def enter(self,v,n=1,hi=0,lo=1):
  d=v.objects['contestState'];d.p['vcReady']=1;w=v.domain_words();w[90]=1;w[91]=n;w[2]=hi;w[3]=lo;w[92]=1;w[95]=0;w[99]=0
  self.assertEqual(v.proc('rbEvent',1,d,0),1);return d,w
 def tick(self,v,n):
  for _ in range(n//2):v.advance(2);v.poll()
 def arrive(self,v,target=152):
  for _ in range(2400):
   if v.status(0)==target:return
   v.advance(2);v.poll()
  self.fail('Target never arrived')
 def bridge(self,v):
  for _ in range(2400):
   if v.status(1)==2:return
   v.advance(2);v.poll()
  self.fail('Bridge never started')
 def staged_position(self,v,target,pos):
  # Explicit typed native-position fixture, never native proof. Controller/clock
  # anchors are made coherent; emitted rbPoll still performs both native reads.
  if v.status(0)!=target:
   self.assertEqual(v.proc('rbRetire'),1)
   self.assertEqual(v.proc('rbStartBed',target),1)
  p=v.parsers[v.objects['responsiveSound']];p['tick']=pos;p['keys']={}
  t=v.objects['homeReadyTransport'if target==151 else 'contestReadyTransport'];t.p.update(musicPosition=pos,previousPosition=pos,previousReadTick=v.now,lastPollTick=v.now,lastProgressTick=v.now,transportMode=2,positionUncertain=0,wholeGain=100,loopHasWrapped=1)
  t.call('anchorClock',v.now);t.call('anchorPosition',v.now)
  return t,p
