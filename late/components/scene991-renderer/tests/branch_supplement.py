#!/usr/bin/env python3
"""Targeted valid-range owner-error/null and actor-presence paint branches."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests')]
from paint_matrix import Matrix
from derive import dump,sha

def run():
 m=Matrix();snaps=m.snapshots()
 m.update({'location':0,'onApron':0,'houseEntered':0,'bunnyReady':0},{'presentationAudio':{'lane':1,'speaker':2,'mouth':1}})
 m.compare('porch-bunny-speaking-not-ready','h6BaseDrawWorld')
 m.reset(snaps);m.update(objects={'p05State':{'hFailure':1}})
 m.compare('owner-error-world','h6BaseDrawWorld')
 m.reset(snaps);m.update(objects={'p06State':{'h6FrankieRoom':6}})
 m.compare('owner-frankie-away','livingPerson',3,pure=True)
 m.reset(snaps);m.update(objects={'p05State':{'hBunnyRoom':5}})
 m.compare('owner-bunny-away','livingPerson',2,pure=True)
 m.reset(snaps);m.update({'p08':0},{'p03State':{'p03Ready':1}})
 m.compare('pre-p08-original-kitchen-service','drawKitchen')
 # Save supplemental coverage separately; do not replace the completed broad run.
 original=H/'evidence/matrix-coverage.json';saved=original.read_bytes();data=m.coverage();original.write_bytes(saved)
 dump(H/'evidence/supplement-coverage.json',data)
 dump(H/'evidence/branch-supplement.json',{'status':'PASS_FOUR_WAY','cases':m.cases,'compile_receipt_sha256':sha(H/'build/coherent/compile-receipt.json'),'scope':'Isolated paint fixtures using original owner properties and methods; no story grant or native claim','native_acceptance':False})
 print('PASS_BRANCH_SUPPLEMENT',len(m.cases))
if __name__=='__main__':run()
