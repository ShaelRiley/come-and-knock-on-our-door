"""Lossless source spans with explicit character wrapping for URLs/bound dates.

All raw Unicode remains in provenance. Fixed-font output admits only supported
ASCII after the documented punctuation projection; URLs keep their exact case.
"""
import hashlib,re
TRANSLATE=str.maketrans({'‘':"'",'’':"'",'“':'"','”':'"','–':'-','—':' - ','…':'...','●':'.'})
sha=lambda value:hashlib.sha256(value).hexdigest()
def require(ok,why):
 if not ok:raise ValueError(why)
def display(text,preserve_case=False):
 value=text.translate(TRANSLATE)
 if not preserve_case:value=value.upper()
 try:value.encode('ascii')
 except UnicodeEncodeError:raise ValueError('Unsupported native glyph; exact source preserved')
 require(all(c in '\n\t\r' or 32<=ord(c)<127 for c in value) and '|' not in value,'Unsafe display text')
 return value

def admit_date(value):
 require(type(value) is str and 1<=len(value)<=80,'Exact selected 1..80-character date required')
 require(all(32<=ord(c)<127 and c!='|' for c in value),'Unsupported native date glyph; no rewritten fallback')
 return value

def paginate(text,preserve_case=False,allow_long=False):
 require(type(text) is str and bool(re.search(r'\S',text)),'Empty source')
 words=list(re.finditer(r'\S+',text));tokens=[];breaks=[]
 for wi,w in enumerate(words):
  raw=w.group();is_url=bool(re.fullmatch(r'https?://\S+',raw));norm=lambda v:display(v,preserve_case or is_url)
  shown=norm(raw)
  if len(shown)<=50:tokens.append((w.start(),w.end(),shown,wi))
  else:
   require(allow_long or is_url,'Unbreakable non-URL source token')
   start=w.start()
   while start<w.end():
    end=start
    while end<w.end() and len(norm(text[start:end+1]))<=50:end+=1
    require(end>start,'One source character exceeds width')
    tokens.append((start,end,norm(text[start:end]),wi))
    if end<w.end():breaks.append(end)
    start=end
 lines=[];line=[];width=0
 for ti,(start,end,shown,wi) in enumerate(tokens):
  previous=tokens[ti-1] if ti else None
  same_word=bool(previous and previous[3]==wi)
  hard_break=bool(previous and ('\n' in text[previous[1]:start] or same_word))
  if line and (hard_break or width+1+len(shown)>50):lines.append(line);line=[];width=0
  line.append((start,end,shown,wi));width+=len(shown)+(len(line)>1)
 if line:lines.append(line)
 pages=[]
 for li in range(0,len(lines),3):
  group=lines[li:li+3];start=0 if not pages else group[0][0][0];end=lines[li+3][0][0] if li+3<len(lines) else len(text)
  shown='\n'.join(' '.join(t[2] for t in line) for line in group);raw=text[start:end]
  pages.append(dict(text=shown,raw_text=raw,source_char_range=[start,end],source_utf8_byte_range=[len(text[:start].encode()),len(text[:end].encode())],raw_text_sha256=sha(raw.encode()),bytes_with_nul=len(shown.encode())+1,word_range=[group[0][0][3],group[-1][-1][3]+1],character_wraps=[i for i in breaks if start<i<=end],display_chunks=[dict(source_char_range=[t[0],t[1]],text=t[2],word_index=t[3]) for line in group for t in line]))
 require(''.join(p['raw_text'] for p in pages)==text,'Source span mismatch')
 require(all(p['bytes_with_nul']<=153 and len(p['text'].splitlines())<=3 and max(map(len,p['text'].splitlines()))<=50 for p in pages),'Geometry overflow')
 # Full URL bytes survive even when a URL crosses line or page boundaries.
 for url in re.finditer(r'https?://\S+',text):
  chunks=[c for p in pages for c in p['display_chunks'] if url.start()<=c['source_char_range'][0]<url.end()]
  require(''.join(c['text'] for c in chunks)==url.group(),'URL altered')
 return pages
