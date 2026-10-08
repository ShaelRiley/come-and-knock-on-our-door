"""Original provisional credit cue, portable adaptation 2026-10-08."""
import midi as g
def credits():
    events=[]
    def emit(t,msg,priority=1):events.append((t*16,priority,bytes(msg)))
    def note(t,length,ch,pitch,vel):
        emit(t,[0x90|ch,pitch,vel],2);emit(t+length,[0x80|ch,pitch,0],0)
    for ch,program,vol,pan in ((5,11,76,52),(6,0,50,76)):
        for msg in ((0xc0|ch,program),(0xb0|ch,7,vol),(0xb0|ch,10,pan),
                    (0xb0|ch,64,0),(0xe0|ch,0,64)):emit(0,msg)
    motif=(67,72,74,76,72,69,67,64)
    roots=(48,53,55,48,57,53,55,48,53,48)
    for card in range(10):
        start=card*360+6;root=roots[card]
        for n in range(8 if card==9 else 12):
            note(start+n*30,20,5,motif[(card+n)%len(motif)],56)
        for beat in range(4 if card==9 else 6):
            for interval in (0,3 if root==57 else 4,7):
                note(start+beat*60,44,6,root+interval,39)
        if card==9:
            # Gentle final tonic ends at3516, leaving84ticks (1.4seconds)
            # for native instrument release before the3600-tick visual cut.
            note(start+240,30,5,72,44)
            for interval in (0,4,7):note(start+240,30,6,48+interval,33)
    smf=g.write_smf(events,3600*16);midi,timing=g.convert_smf(smf)
    channels={}
    for tick,msg in midi:channels.setdefault(msg[0]&15,[]).append((tick,msg))
    channels[15]=[(0,b'\xcf\0'),(0,b'\xbf\x50\0'),(3600,b'\xbf\x50\0')]
    payload=g.sound_resource(channels,{5:1,6:3,15:0})
    return smf,payload,timing
