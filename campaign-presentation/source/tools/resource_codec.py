from pathlib import Path
import struct,hashlib

def encode(resources):
 volume=bytearray();groups={}
 for (kind,number),payload in sorted(resources.items()):
  if not(0<=kind<127 and 0<=number<=65535 and 0<len(payload)<=65535):raise RuntimeError('Resource identity/SCI16 bound')
  if len(volume)&1:volume.append(0)
  offset=len(volume);volume+=struct.pack('<BHHHH',kind|128,number,len(payload),len(payload),0)+payload;groups.setdefault(kind,[]).append((number,offset))
 if len(volume)&1:volume.append(0)
 directory=bytearray();entries=bytearray();start=3*(len(groups)+1)
 for kind,group in sorted(groups.items()):
  directory+=struct.pack('<BH',kind|128,start+len(entries))
  for number,offset in group:entries+=struct.pack('<H',number)+(offset//2).to_bytes(3,'little')
 directory+=struct.pack('<BH',255,start+len(entries));return bytes(directory+entries),bytes(volume)

def decode(mapping,volume):
 pos=0;dirs=[]
 while True:
  if pos+3>len(mapping):raise RuntimeError('Map directory truncated')
  kind,offset=struct.unpack_from('<BH',mapping,pos);pos+=3
  if kind<128 or (dirs and kind<=dirs[-1][0]):raise RuntimeError('Map ordering')
  dirs.append((kind,offset))
  if kind==255:break
 if len(dirs)<2 or dirs[0][1]!=pos or dirs[-1][1]!=len(mapping):raise RuntimeError('Map directory extent')
 result={}
 for (kind,first),(_,last) in zip(dirs,dirs[1:]):
  if not(pos<=first<last<=len(mapping)) or (last-first)%5:raise RuntimeError('Map group extent')
  for p in range(first,last,5):
   number=struct.unpack_from('<H',mapping,p)[0];at=int.from_bytes(mapping[p+2:p+5],'little')*2
   if at+9>len(volume):raise RuntimeError('Volume header extent')
   rk,rn,packed,raw,compression=struct.unpack_from('<BHHHH',volume,at)
   if (rk,rn)!=(kind,number) or packed!=raw or compression or not packed or at+9+packed>len(volume):raise RuntimeError('Volume payload mismatch')
   key=(kind&127,number)
   if key in result:raise RuntimeError('Duplicate resource')
   result[key]=volume[at+9:at+9+packed]
 if encode(result)!=(mapping,volume):raise RuntimeError('Hidden/noncanonical resource data')
 return result
