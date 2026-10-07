#!/usr/bin/env python3
"""Spoiler-neutral listening delivery plus separate clearly flagged production ZIP."""
import json,subprocess,zipfile,hashlib,wave,shutil
from pathlib import Path
import score_v4_core as c
O=c.OUT;D=c.ROOT/'deliverables/approved-direction-score-v4-2026-10-05';A=D/'Neutral Tracks';D.mkdir(exist_ok=True);A.mkdir(exist_ok=True)
rs=sorted([json.loads(p.read_text())for p in(O/'analysis').glob('*-manifest.json')],key=lambda r:r['resource_id'])
run=lambda args:subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
rows=[];ids={r['resource_id']:r for r in rs};tracks={r['resource_id']:i+1 for i,r in enumerate(rs)}
for i,r in enumerate(rs,1):
 src=O/'renders'/f"{r['cue_id']}-FluidR3-v161.wav";dst=A/f'Track {i:02d}.mp3'
 if not dst.exists()or dst.stat().st_mtime<src.stat().st_mtime:
  run(['ffmpeg','-v','error','-y','-i',str(src),'-map_metadata','-1','-map_chapters','-1','-c:a','libmp3lame','-q:a','2','-metadata',f'title=Track {i:02d}','-metadata','artist=Come and Knock on Our Door','-metadata','comment=Instrumental soundtrack candidate. Offline fixed-SoundFont render. Six-second release after scored ending. No loudness normalization.',str(dst)])
 meta=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:format_tags','-of','json',str(dst)]).stdout)
 forbidden=['MUS0','MUS1','P11','P12','P13','RESCUE','MICROPHONE','PROMISES','ROUTING','CONFETTI','MIL0','STRINGER']
 assert not any(x in json.dumps(meta).upper()for x in forbidden)
 rows.append({'track':i,'file':dst.name,'scored_seconds':r['duration_seconds'],'preview_seconds':float(meta['format']['duration']),'sha256':c.sha(dst.read_bytes()),'lossy_preview':True})
# A short sampler; all excerpts are disclosed, with fades only at sampler edges.
# Whole cues retain the original unnormalized WAV level and natural releases.
selections=[(102,0,32),(106,64,32),(108,64,32),(114,0,32),(117,0,32),(140,0,32)]
clips=[];tour=[];elapsed=0
for i,(rid,beat,length)in enumerate(selections,1):
 r=ids[rid];start=.2+beat*60/r['bpm'];duration=length*60/r['bpm'];src=O/'renders'/f"{r['cue_id']}-FluidR3-v161.wav";clip=D/f'_sampler_{i:02d}.wav'
 run(['ffmpeg','-v','error','-y','-ss',str(start),'-t',str(duration),'-i',str(src),'-af',f'afade=t=in:st=0:d=0.08,afade=t=out:st={duration-.35}:d=0.35,apad=pad_dur=0.6','-ar','44100','-ac','2','-c:a','pcm_s16le',str(clip)])
 clips.append(clip);tour.append({'section':i,'start_seconds':elapsed,'full_track':tracks[rid],'excerpt_seconds':duration});elapsed+=duration+.6
listfile=D/'_concat.txt';listfile.write_text(''.join(f"file '{p}'\n"for p in clips))
tourfile=D/'Come and Knock - New Score Sampler v4.mp3'
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listfile),'-map_metadata','-1','-map_chapters','-1','-c:a','libmp3lame','-q:a','2','-metadata','title=New Score Sampler v4','-metadata','artist=Come and Knock on Our Door','-metadata','comment=Six instrumental excerpts with sampler-only edge fades and short gaps. Full tracks retain authored level.',str(tourfile)])
lines=['COME AND KNOCK ON OUR DOOR — NEW SCORE LISTENING GUIDE','', 'The relaxed swing, space and phrase dynamics you approved in the short V3 test now guide this full set of instrumental candidates. Your original V3 audition is preserved unchanged. The complete new cues still need your ears and native-game testing.','', 'The score returns to recognizable phrases from all five of your authorized MIDI bundles. Each theme keeps its own source rhythm and harmony while changing instrumental voice, register, density, and emotional shape. There are eleven cue families, including a distinct taut, clipped action-comedy color. The main musical language stays relaxed and sparse. Paired instrumental voices suggest duet phrasing; these previews contain no recorded singing.','', 'The 38 complete previews include principal cues, related variations and shorter links/punctuations. Together they contain about 34 minutes of scored music across variations. Each complete file adds six seconds for instrument/reverb release. This is a recurring game score, not 90 minutes of unrelated new themes.','', 'All track names and audio metadata are neutral. This guide and listening ZIP contain no story or puzzle details. The separately labeled production archive does contain story bindings and is for integration work.','', 'The MP3 files are high-quality lossy previews; editable MIDI and stereo WAV masters are retained. All use offline FluidSynth 2.4.4 / FluidR3 GM synthesis at the same modeled 161 music setting used for the approved reference, with no loudness normalization. Actual in-game balance with voices, laughter and foley remains a separate check.','', 'The sampler has six excerpts, with small gaps and fades only at sampler edges. It is not a continuous in-game sequence.','', 'SAMPLER TIMES']
for x in tour:
 t=x['start_seconds'];lines.append(f"{int(t//60)}:{t%60:04.1f} — Section {x['section']:02d}, from Track {x['full_track']:02d}")
lines+=['','FULL TRACKS — SCORED DURATION BEFORE THE SIX-SECOND RELEASE']
for x in rows:
 t=x['scored_seconds'];lines.append(f"Track {x['track']:02d}: {int(t//60)}:{t%60:04.1f}")
lines+=['','Engineering checks: 16 structural tests and 106 offline component profiles passed. No clipped samples; all instrument voices cleared by the end of each release capture. These checks do not substitute for musical listening or native-game acceptance.','', 'Useful listening feedback: whether the phrases feel connected, how the space and dynamics breathe, which instrumental colors you like, and whether the separate sharper color still leaves room for dialogue.']
guide=D/'Come and Knock - Spoiler-Free Listening Guide v4.txt';guide.write_text('\n'.join(lines)+'\n')
(A/'Listening Guide.txt').write_bytes(guide.read_bytes())
public={'status':'Full-score instrumental candidates under the accepted short V3 direction; individual and native acceptance pending','tracks':rows,'sampler_sections':tour,'story_details':False}
(A/'Audio Details.json').write_text(json.dumps(public,indent=2))
listen=D/'Come and Knock - Complete Listening Set v4 - Spoiler-Free.zip'
with zipfile.ZipFile(listen,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(A.iterdir()):z.write(p,p.name)
tech=D/'Come and Knock - Production Score v4 - Contains Story Details.zip'
with zipfile.ZipFile(tech,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for sub in ['analysis','midi','native','licenses']:
  for p in sorted((O/sub).rglob('*')):
   if p.is_file()and not p.name.endswith('.log'):z.write(p,str(p.relative_to(c.ROOT)))
 z.write(O/'README.md','README.md')
 z.write(c.V3/'analysis/RELAXED_SWING_FEEL_V3-manifest.json',str((c.V3/'analysis/RELAXED_SWING_FEEL_V3-manifest.json').relative_to(c.ROOT)))
 for item in json.loads((O/'analysis/accepted-v3-lock.json').read_text())['files']:z.write(c.ROOT/item['path'],item['path'])
 original=c.ROOT.parent/'attachment_inspect_425e/CaKoOD Soundtrack Inspiration.zip'
 z.write(original,'Original Source Archive/CaKoOD Soundtrack Inspiration.zip')
 for p in sorted((c.OLD/'source').rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(c.ROOT)))
 for p in sorted((c.OLD/'analysis').glob('B*.json')):z.write(p,str(p.relative_to(c.ROOT)))
 for name in ['source-inventory.json','curated-motifs.json']:z.write(c.OLD/'analysis'/name,str((c.OLD/'analysis'/name).relative_to(c.ROOT)))
 for name in ['score_v4_core.py','compose_full_score_v4.py','compose_verbal_music_v4.py','reduced_score_v4.py','render_full_score_v4.py','render_score.py','finalize_score_v4.py','test_full_score_v4.py','package_score_v4.py']:
  z.write(c.ROOT/'tools/music-production'/name,'tools/music-production/'+name)
 for name in ['generate.py','generate_density.py','profile_fluidsynth.py']:z.write(c.ROOT/'stock-sci/audio-proof'/name,'stock-sci/audio-proof/'+name)
 z.writestr('WAV MASTERS.txt','The 38 unnormalized44.1kHz stereo16-bit WAV masters are retained in the project. They are omitted from this compact integration archive. Their SHA256 hashes and relative paths are in assets/music-production/source-arrangements-v4-approved/analysis/render-validation.json. Each contains scored music plus 6 seconds of release.\n')
for p in [listen,tech]:
 with zipfile.ZipFile(p)as z:assert z.testzip()is None
receipt={'public_files':[str(tourfile),str(listen),str(guide)],'technical_file_contains_story_details':str(tech),'files':[{'file':p.name,'bytes':p.stat().st_size,'sha256':c.sha(p.read_bytes())}for p in[tourfile,listen,guide,tech]],'track_map_private':[{**x,'cue_id':r['cue_id'],'resource_id':r['resource_id']}for x,r in zip(rows,rs)]}
(D/'packaging-receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:v for k,v in receipt.items()if k!='track_map_private'},indent=2))
