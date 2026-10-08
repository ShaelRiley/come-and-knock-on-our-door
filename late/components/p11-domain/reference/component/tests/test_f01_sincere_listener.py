"""Review02 regressions for independently reproduced listener finding F01.

Continuous Felix presence is the explicitly accepted implementation reading of
the reciprocal scene, not a quoted canonical per-unit listener requirement.
"""
from dataclasses import replace
import itertools
import json
import unittest

from cakood.p04_model import project_gate
from cakood.p11_model import P11World, P11Context, PREREQUISITES, SIDE_PASSAGE, PORCH, CONSERVATORY, RECORD_UNITS
from test_current_contract import repaired_gate


def staged(pre_engaged):
    owner=repaired_gate()
    if pre_engaged:owner.set_peg(1)
    c=P11Context(SIDE_PASSAGE,project_gate(owner),flags=PREREQUISITES)
    w=P11World();w.lift(c)
    if not pre_engaged:
        w.request_peg(c);owner.set_peg(1);c=replace(c,gate=project_gate(owner))
        w.acknowledge_peg(c,w.pending_peg_request_id)
    w.release_catch(c);w.pull_handle(c);w.stage_display(c)
    return w,c


class SincereListenerRegression(unittest.TestCase):
    def test_f01_final_jackie_reply_blocks_when_felix_left(self):
        w,c=staged(True)
        p=w.begin_presentation(c,'sincere')
        units=RECORD_UNITS['P11.DIALOGUE.002']
        w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=units[:5])
        away=replace(c,felix_room=CONSERVATORY)
        w.validate_context(away)
        before=w.save()
        result=w.acknowledge_presentation(away,p.presentation_id,speech_unit_ids=units[5:])
        self.assertEqual(result.code,'felix_required')
        self.assertEqual(w.save(),before)
        self.assertFalse(w.sincere_complete or w.contest_eligible)
        self.assertEqual(w.journal_units(),units[:5])
        self.assertEqual(away.felix_room,CONSERVATORY)
        self.assertEqual((result.text,result.line_ids,result.events),('',(),()))
        w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=units[5:])
        self.assertTrue(w.sincere_complete and w.contest_eligible)

    def test_every_partial_prefix_blocks_and_resumes_after_return_or_load(self):
        units=RECORD_UNITS['P11.DIALOGUE.002']
        for pre_engaged,posture,prefix,reload in itertools.product(
                (False,True),('staged','set_back'),range(6),(False,True)):
            with self.subTest(pre_engaged=pre_engaged,posture=posture,prefix=prefix,reload=reload):
                if posture=='staged':w,c=staged(pre_engaged)
                else:
                    owner=repaired_gate()
                    if pre_engaged:owner.set_peg(1)
                    c=P11Context(SIDE_PASSAGE,project_gate(owner),flags=PREREQUISITES)
                    w=P11World();w.lift(c)
                p=w.begin_presentation(c,'sincere')
                if prefix:w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=units[:prefix])
                if posture=='set_back':w.set_back(c)
                old=p.presentation_id
                if reload:
                    w=P11World.load(json.loads(json.dumps(w.save())),context=c)
                    self.assertEqual(w.acknowledge_presentation(c,old,
                        speech_unit_ids=units[prefix:prefix+1]).code,'stale_presentation')
                    p=w.resume_presentation(c,'sincere')
                away=replace(c,felix_room=CONSERVATORY);w.validate_context(away);before=w.save()
                for operation in (
                    lambda:w.resume_presentation(away,'sincere'),
                    lambda:w.begin_presentation(away,'sincere'),
                    lambda:w.acknowledge_presentation(away,p.presentation_id,speech_unit_ids=units[prefix:prefix+1]),
                    lambda:w.acknowledge_presentation(away,p.presentation_id,record_id='P11.DIALOGUE.002')):
                    self.assertEqual(operation().code,'felix_required')
                    self.assertEqual(w.save(),before)
                    self.assertEqual(w.journal_units(),units[:prefix])
                self.assertFalse(w.sincere_complete or w.contest_eligible)
                self.assertEqual(away.felix_room,CONSERVATORY)
                pending=w.resume_presentation(c,'sincere')
                w.acknowledge_presentation(c,pending.presentation_id,record_id='P11.DIALOGUE.002')
                self.assertTrue(w.sincere_complete)
                self.assertEqual(w.contest_eligible,posture=='staged')

    def test_bunny_presence_remains_independently_required_after_felix_returns(self):
        w,c=staged(False);p=w.begin_presentation(c,'sincere')
        units=RECORD_UNITS['P11.DIALOGUE.002']
        w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=units[:5])
        before=w.save();away=replace(c,bunny_room=CONSERVATORY)
        self.assertEqual(w.acknowledge_presentation(away,p.presentation_id,
            speech_unit_ids=units[5:]).code,'bunny_at_porch_required')
        self.assertEqual(w.save(),before);self.assertEqual(away.bunny_room,CONSERVATORY)
        self.assertEqual(c.bunny_room,PORCH)
        w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=units[5:])
        self.assertTrue(w.contest_eligible)

if __name__=='__main__':unittest.main(verbosity=2)
