#!/usr/bin/env python3
"""Explicit P11 emitted lifecycle fixture; modeled ancestors/clock/PCM, no native proof."""
from pathlib import Path
import json
import sys
sys.dont_write_bytecode=True

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE / 'tests'))
from presentation_vm import PresentationVM


class Probe(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.pay_events = []
        self.h.p.update(location=3, motionX=100*64, motionY=138*64,
                        uiPanel=0, onApron=0, paused=0, menuOpen=0, opening=0)
        p = self.instance(993)
        p.p.update(p11Epoch=1, p11FoldLo=1, p11FoldStartLo=2,
                   p11Code=32, p11ResultLo=1, p11EventCount=1, p11LineCount=1)
        a = self.arrays(993)
        a['p11Events'][0] = 8
        a['p11EventLo'][0] = 1
        self.h.p['p08'] = self.instance(989)
        self.instance(989).p.update(h8Host=self.h, h8Lease=1)
        a['h11OwnerState'][:] = [1, 0, 0, 1]

    def procedure(self, module, index, args):
        m = self.modules[module]
        return self.execute(self.h, m, 'export'+str(index), m.layout['exports'][index], args)

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key in {(993, 'h11ContextMatch'), (993, 'h11Active'),
                   (993, 'h11OwnerReady'), (993, 'h11OwnerPrerequisites'),
                   (993, 'h11OwnerValid')}:
            return 1
        if key == (989, 'h8ActionBarrier'):
            return 0
        if key == (0, 'drawWorld'):
            result = self.call(self.instance(993), 'h11OwnerPaint')
            self.call(self.instance(993), 'h11OwnerFrame', (2,))
            self.call(self.instance(993), 'h11Frame', (2,))
            return result
        tracked = ((obj.module.number == 993 and (name.startswith('h11Pay') or name.startswith('h11Read') or name == 'h11OwnerFrame')) or key in {(0, 'render'), (989, 'h8VF'), (0, 'uiRender')})
        if not tracked:
            return super().call(obj, name, args)
        before = list(self.arrays(993)['h11Pay'])
        result = super().call(obj, name, args)
        after = list(self.arrays(993)['h11Pay'])
        if (obj.module.number == 993 and (name.startswith('h11Pay') or name.startswith('h11Read') or name == 'h11OwnerFrame')) or key in {(0, 'render'), (989, 'h8VF'), (0, 'uiRender')}:
            self.pay_events.append({'method': name, 'args': list(args), 'result': result,
                               'mode': after[0], 'heard': after[20], 'pose': after[1],
                               'drop_from': before[0] if before[0] and not after[0] else None})
        return result

    def snap(self, label):
        p = self.arrays(993)['h11Pay']
        d = self.h.p['dialogue']
        print(json.dumps({'label': label, 'identity': self.call(self.h, 'scenePageIdentity'), 'hostfields': {k:self.h.p[k] for k in ['opening','paused','menuOpen','uiFailure','bridgeFailure','uiDocument','uiPage','uiPageCount']}, 'mode': p[0], 'heard': p[20],
                          'pose': p[1], 'painted_pose': p[14],
                          'page': d.p['sdPage'], 'voice': d.p['sdVoice'],
                          'pending': d.p['sdPendingStart'], 'armed': d.p['sdArmed'],
                          'suppressed': d.p['sdSuppressed'], 'audio_token': d.p['sdAudioToken'],
                          'token': self.a.p['token'], 'lane': self.a.p['lane'],
                          'generation': d.p['sdGeneration'], 'paint_generation': d.p['sdPaintGeneration']}))

