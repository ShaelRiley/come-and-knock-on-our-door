"""Original CC7 remix, portable adaptation 2026-10-08."""
import midi as g
VOLUMES={0:(80,112),1:(55,77),5:(76,106),6:(50,70)}
VOICES={0:1,1:3,2:1,3:1,4:1,5:1,6:3,15:0}
def transform(message):
    ch = message[0] & 15
    if message[:2] == bytes((0xb0|ch,7)) and ch in VOLUMES:
        before, after = VOLUMES[ch]
        assert message[2] == before, (ch, message)
        return message[:2] + bytes((after,))
    return message

def remap_native(data, change=True):
    stream = g.decode_sound(data)
    return g.sound_resource({ch:[(t,transform(m) if change else m) for t,m in events]
                             for ch,events in stream.items()}, VOICES)
