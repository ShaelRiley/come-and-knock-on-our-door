#!/usr/bin/env python3
"""Actual emitted pause-menu hit/keyboard dispatch; chooser effects are unit sinks.

No ScummVM, save, replay, progression or native acceptance is performed. Main's
compiled input and h14Input run. The date bank is initially inactive; p08 and
presentation references are absent. Only menuChoice and the same three terminal
chooser/replay effects (writeSave/readSave/startReplay, called directly by keys)
are intercepted. Keyboard4..6 execute their real local toggles.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

sys.dont_write_bytecode = True
from presentation_vm import PresentationVM, S

ROWS = ((69, '1 SAVE 2 LOAD 3 REPLAY OPENING', ('1 SAVE','2 LOAD','3 REPLAY OPENING')),
        (83, '4 RESUME 5 QUIT 6 AUDIENCE ON/OFF', ('4 RESUME','5 QUIT','6 AUDIENCE ON/OFF')))


class PauseMenuFixture(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.dispatches = []

    def call(self, obj, name, args=()):
        if obj is self.h and name == 'menuChoice':
            self.dispatches.append(args[0])
            return 0
        effects = {'writeSave':1, 'readSave':2, 'startReplay':3}
        if obj is self.h and name in effects:
            self.dispatches.append(effects[name])
            return 0
        return super().call(obj, name, args)

    def event(self, kind, x=0, y=0, message=0, paused=1, menu=1):
        self.dispatches.clear()
        self.h.p.update(opening=0, menuOpen=menu, paused=paused, presentation=0,
                        p08=0, type=kind, message=message, x=x, y=y,
                        quitRequested=0, audienceMuted=0, dirty=0)
        self.call(self.h, 'input')
        if self.dispatches:
            assert len(self.dispatches) == 1, self.dispatches
            return self.dispatches[0]
        if not self.h.p['menuOpen'] and not self.h.p['paused']:
            return 4
        if self.h.p['quitRequested']:
            return 5
        if self.h.p['audienceMuted']:
            return 6
        return 0


def run(build=None):
    start = time.monotonic()
    v = PauseMenuFixture(build)
    font = v.resources[7,0]
    assert struct.unpack_from('<H',font,4)[0] == 8
    count = struct.unpack_from('<H',font,2)[0]
    widths = {}
    for _,text,_ in ROWS:
        assert text.encode()+b'\0' in v.modules[0].heap, 'Actual compiled menu label changed'
        for char in set(text):
            assert ord(char) < count
            offset = struct.unpack_from('<H',font,6+2*ord(char))[0]
            width,height = font[offset:offset+2]
            assert (width,height) == (6,8), (char,width,height)
            widths[char] = width
    results = []
    def check(label, expected, **event):
        actual = v.event(**event)
        results.append({'case':label,'expected':expected,'actual':actual,'event':event,'passed':actual==expected})
    spans = []
    for y,text,labels in ROWS:
        for label in labels:
            lo=text.index(label)
            left=30+sum(widths[c] for c in text[:lo])
            right=left+sum(widths[c] for c in label)
            spans.append({'label':label,'left':left,'right':right,'top':y,'bottom':y+8})
            for index,char in enumerate(label):
                if char==' ':continue
                x=left+sum(widths[c] for c in label[:index])+2
                check('glyph '+label+' #'+str(index),int(label[0]),kind=1,x=x,y=y+3)
    assert len([r for r in results if r['case'].startswith('glyph ')]) == 51
    # Boundaries are derived from the actual full label strings and font.
    for row,ys in ((spans[:3],(68,72,81)),(spans[3:],(82,86,96))):
        for left,right in zip(row,row[1:]):
            cut=right['left']
            for y in ys:
                for x,expected in ((cut-1,int(left['label'][0])),(cut,int(right['label'][0])),(cut+1,int(right['label'][0]))):
                    check('horizontal boundary '+str((x,y)),expected,kind=1,x=x,y=y)
    for y,expected in ((67,0),(68,1),(81,1),(82,4),(96,4),(97,0)):
        check('vertical boundary '+str(y),expected,kind=1,x=32,y=y)
    # Existing keyboard paths do not use the mouse thresholds; test both forms
    # of the existing paused/menuOpen admission, not just the combined state.
    for paused,menu in ((1,1),(0,1),(1,0)):
        for choice in range(1,7):
            check('keyboard '+str(choice)+' pause/menu'+str((paused,menu)),choice,
                  kind=4,message=ord(str(choice)),paused=paused,menu=menu)
    # The reported native click:640x480 window maps to320x200 SCI coordinates.
    check('native184,173=>SCI92,72',2,kind=1,x=92,y=72)
    failures=[r for r in results if not r['passed']]
    receipt=(Path(build) if build else S/'build/coherent')/'compile-receipt.json'
    return {'status':'PASS_EMITTED_PAUSE_MENU_HITS_NOT_NATIVE' if not failures else 'FAIL_EMITTED_PAUSE_MENU_HITS_NOT_NATIVE',
            'native_acceptance':False,'case_count':len(results),'glyph_cases':51,
            'boundary_cases':42,'keyboard_cases':18,'observed_click_case':1,
            'failed_cases':failures,'font0_sha256':hashlib.sha256(font).hexdigest(),
            'compile_receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),
            'label_spans':spans,'seconds':time.monotonic()-start,
            'scope':__doc__,'cases':results}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',type=Path)
    args=parser.parse_args()
    result=run(args.build)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if not result['failed_cases'] else 1)
