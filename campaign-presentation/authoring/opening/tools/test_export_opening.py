"""Focused gates; temporary fixture pixels can never become production assets."""
import json
from pathlib import Path
import struct
import tempfile
import unittest
from PIL import Image, ImageDraw

from export_opening import Art, CAST, budget, registered_poses, export_one, separate_stable_prop
from inspect_view import ViewFormatError, decode_view
from view_writer import Cel, encode_view

HERE=Path(__file__).resolve().parent

def fixture():
    # Eight deliberately abstract shapes, not cast portraits or stand-in art.
    sheet=Image.new('RGBA',(960,800),(0,0,0,0))
    for i in range(8):
        x=(i%4)*240;y=(i//4)*400;d=ImageDraw.Draw(sheet)
        d.rectangle((x+100,y+70,x+139,y+381),fill=(51,117,106,255))
        d.rectangle((x+140,y+170,x+151+i*4,y+185),fill=(233,210,163,255))
    return sheet

def specification(slug='felix'):
    return {'slug':slug,'master':'fixture.png','prompt':'fixture-prompt.txt','master_version':'TEST_ONLY_ABSTRACT_PIXELS','registration_reviewed':True,'upright_height_source':312,'target_upright_height':78,'source_anchors':[[119.5,381]]*8,'screen_anchor':[118,134]}

class ExportGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.art=Art()

    def test_registration_preserves_scale_and_common_bounds(self):
        cels,union,screen,records=registered_poses(fixture(),specification(),self.art)
        self.assertEqual(len({im.size for im in cels}),1)
        self.assertEqual(len({r['uniform_scale'] for r in records}),1)
        self.assertEqual(records[0]['uniform_scale'],.25)
        self.assertEqual(screen,[118,134])
        self.assertEqual(union[3],135)
        self.assertEqual(union[3]-union[1],78)
        for im in cels:self.assertTrue(set(im.tobytes())<=set(range(218))|{255})

    def test_crouch_is_not_normalized(self):
        sheet=fixture();d=ImageDraw.Draw(sheet)
        d.rectangle((340,70,379,109),fill=(0,0,0,0))
        cels,union,_,records=registered_poses(sheet,specification(),self.art)
        self.assertEqual(records[1]['screen_opaque_bbox'][1]-records[0]['screen_opaque_bbox'][1],10)
        self.assertEqual(cels[0].size,cels[1].size)

    def test_refuses_unreviewed_or_scale_tradeoff(self):
        spec=specification();spec['registration_reviewed']=False
        with self.assertRaisesRegex(ValueError,'Review measured'):registered_poses(fixture(),spec,self.art)
        spec=specification();spec['target_upright_height']=70
        with self.assertRaisesRegex(ValueError,'tradeoff'):registered_poses(fixture(),spec,self.art)

    def test_refuses_clipping_and_duplicates(self):
        sheet=fixture();ImageDraw.Draw(sheet).point((0,70),fill=(1,2,3,255))
        with self.assertRaisesRegex(ValueError,'touch source cell border'):registered_poses(sheet,specification(),self.art)
        sheet=fixture();first=sheet.crop((0,0,240,400));sheet.paste(first,(240,0))
        with self.assertRaisesRegex(ValueError,'Duplicate native'):registered_poses(sheet,specification(),self.art)
        spec=specification();spec['screen_anchor']=[1,134]
        with self.assertRaisesRegex(ValueError,'outside320x144'):registered_poses(fixture(),spec,self.art)

    def test_original_font_bits_exact(self):
        data=(self.art.reference_dir/'000.font.bin').read_bytes()
        for char in set('Jackie TreeBunny EasterFrankie MaplewoodMr. StringerMilo PennantVivian VossRita StringerFelix BuntCome and Knockon Our Door'):
            at=struct.unpack_from('<H',data,6+2*ord(char))[0]
            w,h=data[at:at+2];raw=data[at+2:at+2+h*((w+7)//8)]
            expected=[self.art.ink if raw[y*((w+7)//8)+x//8]&(0x80>>(x%8)) else 255 for y in range(h) for x in range(w)]
            actual=self.art.lettering(char)
            self.assertEqual(actual.size,(w,h));self.assertEqual(actual.tobytes(),bytes(expected))

    def test_quantization_respects_threshold_and_pinned_range(self):
        im=Image.new('RGBA',(4,1));im.putdata([(255,255,255,0),(1,2,3,127),(1,2,3,128),(0,0,0,255)])
        indexed=self.art.index(im);p=indexed.tobytes()
        self.assertEqual(p[:2],bytes([255,255]));self.assertLess(p[2],218);self.assertLess(p[3],218)

    def test_codec_budget_and_strict_decoder(self):
        loops=[[Cel(78,80,bytes([255])*6240) for _ in range(8)],[Cel(20,30,bytes([12])*600)]]
        encoded=encode_view(loops);decoded=decode_view(encoded)
        self.assertEqual(decoded[1][0]['pixels'],bytes([12])*600)
        with self.assertRaises(ViewFormatError):decode_view(encoded[:-1])
        bad=bytearray(encoded);bad[-1:]+=b'\0'
        with self.assertRaises(ViewFormatError):decode_view(bytes(bad))
        bad=bytearray(encoded);struct.pack_into('<I',bad,18+2*16+28,1)
        with self.assertRaises(ViewFormatError):decode_view(bytes(bad))
        with self.assertRaisesRegex(ValueError,'65535'):encode_view([[Cel(320,144,bytes(320*144))]*2])

    def test_all_eight_exports_reproducible_and_title_exact(self):
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=HERE) as tmp:
            tmp=Path(tmp);fixture().save(tmp/'fixture.png');(tmp/'fixture-prompt.txt').write_text('TEST ONLY abstract pixels, never production art.\n')
            specs=[specification(slug) for slug,*_ in CAST];config=tmp/'config.json';config.write_text(json.dumps({'characters':specs}))
            for spec in specs:
                report,g=export_one(spec,tmp,tmp/'output',self.art,config)
                again,_=export_one(spec,tmp,tmp/'again',self.art,config)
                self.assertEqual(report['resource_sha256'],again['resource_sha256'])
                self.assertEqual(report['loops'],[8,1,1,1] if spec['slug']=='vivian' else [8,1,1])
                self.assertTrue(report['independent_decode_byte_equal'])
                self.assertFalse(report['native_animation_verified'])
                self.assertLessEqual(report['resource_bytes'],65535)
                if spec['slug']=='milo':self.assertEqual(g['background_view'],304)
                if spec['slug']=='vivian':
                    decoded=decode_view((tmp/'output/resources/250.view.bin').read_bytes())
                    self.assertEqual((decoded[3][0]['width'],decoded[3][0]['height']),(288,72))
                    self.assertEqual(decoded[3][0]['pixels'],self.art.title().tobytes())

    def test_stable_prop_partition_is_lossless_and_rejects_overlap(self):
        cels,union,_,_=registered_poses(fixture(),specification(),self.art)
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=HERE) as tmp:
            tmp=Path(tmp);keep=Image.new('L',(320,144),255);ImageDraw.Draw(keep).rectangle((0,130,319,143),fill=0);keep.save(tmp/'actor.png')
            prop=Image.new('L',(320,144));ImageDraw.Draw(prop).rectangle((0,130,319,143),fill=255);prop.save(tmp/'prop.png')
            spec={'stable_prop':{'source_cel':0,'separation_reviewed':True,'actor_keep_masks':['actor.png']*8,'source_prop_mask':'prop.png'}}
            actors,bounds,stable,record=separate_stable_prop(cels,union,spec,tmp,self.art)
            self.assertTrue(record['source_cel0_exact_recomposition'])
            self.assertEqual(stable.height,5)
            self.assertEqual(len({im.tobytes() for im in actors}),8)
            replacement=Image.new('RGBA',(100,100));ImageDraw.Draw(replacement).rectangle((12,12,90,90),fill=(145,78,45,255));replacement.save(tmp/'new-prop.png');(tmp/'new-prop.txt').write_text('TEST_ONLY newly generated prop fixture.\n')
            spec['stable_prop'].update(replacement_master='new-prop.png',replacement_prompt='new-prop.txt',replacement_new_reconstruction=True,replacement_uniform_scale=.25,replacement_source_anchor=[12,12],replacement_screen_anchor=[50,90])
            replaced,replaced_bounds,new_prop,new_record=separate_stable_prop(cels,union,spec,tmp,self.art)
            self.assertEqual(replaced_bounds,bounds)
            self.assertEqual([im.tobytes() for im in replaced],[im.tobytes() for im in actors])
            self.assertIsNone(new_record['source_cel'])
            self.assertIn('NEW_GENERATED',new_record['status'])
            Image.new('L',(320,144),255).save(tmp/'actor.png')
            with self.assertRaisesRegex(ValueError,'overlap'):separate_stable_prop(cels,union,spec,tmp,self.art)

if __name__=='__main__':unittest.main(verbosity=2)
