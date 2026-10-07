from support import *
class EventProof(Scenario):
 def test_01_current_commit_only_and_all_encounters(self):
  for n in range(1,5):
   v=self.vm();d,w=self.enter(v,n,1,32767);saved=list(w)
   self.assertEqual(v.status(9),n);self.assertEqual(v.status(10),1);self.assertEqual(v.status(11),32767)
   self.assertEqual(v.proc('rbEvent',1,d,0),0);self.assertEqual(list(w),saved)
   for flag in('vcBusy','vcLoading','vcUncertain'):
    d.p[flag]=1;self.assertEqual(v.proc('rbEvent',2,d,1),0);d.p[flag]=0
 def test_02_prepared_preview_claims_do_not_commit_music(self):
  v=self.vm();d,w=self.enter(v);before=[v.status(i)for i in range(24)]
  for operation in(0,1,2,5,7,10,11,12,99):self.assertEqual(v.proc('rbHostCommitted',operation,d),0)
  self.assertEqual(before,[v.status(i)for i in range(24)])
 def test_03_response_once_and_exact_identity(self):
  v=self.vm();d,w=self.enter(v,2,2,1);w[92]=3;w[99]=1
  self.assertEqual(v.proc('rbEvent',2,d,1),1);w[92]=5;w[95]=1
  w[2]=1;self.assertEqual(v.proc('rbEvent',3,d,0),0);w[2]=2
  self.assertEqual(v.proc('rbEvent',3,d,0),1);self.assertEqual(v.proc('rbEvent',3,d,0),0)
  self.assertEqual(v.status(16),1);self.assertEqual(v.status(17),0)
 def test_04_true_ko_and_nonko_concession_are_distinct(self):
  v=self.vm();d,w=self.enter(v);w[92]=7;w[102]=1;w[101]=2;w[96]=3;w[97]=3
  self.assertEqual(v.proc('rbEvent',4,d,0),0);self.assertEqual(v.status(17),0)
  w[101]=1;self.assertEqual(v.proc('rbEvent',4,d,0),0);w[97]=0
  self.assertEqual(v.proc('rbEvent',4,d,0),1);self.assertEqual(v.proc('rbEvent',4,d,0),0)
  w[92]=8;w[104]=1;self.assertEqual(v.proc('rbEvent',5,d,0),1);self.assertEqual(v.status(2),151)
 def test_05_concession_exits_without_ko_event(self):
  v=self.vm();d,w=self.enter(v);w[92]=8;w[102]=1;w[101]=2;w[104]=1
  self.assertEqual(v.proc('rbEvent',5,d,0),1);self.assertEqual(v.status(17),0);self.assertEqual(v.status(2),151)
 def test_06_menu_and_chooser_never_exit(self):
  v=self.vm();d,w=self.enter(v);v.proc('rbPreference',62,0,1);self.assertEqual(v.status(15),0)
  self.assertEqual(v.proc('rbBeforeChooser'),1);self.assertEqual(v.status(15),0)
  self.assertEqual(v.proc('rbAfterChooser'),1);self.assertEqual(v.status(15),0)
 def test_07_actual_domain_prepare_commit_response_and_ko(self):
  v=self.vm();d=v.objects['contestState'];d.call('vcInit');d.call('vcBindGeneration',0,1);w=v.domain_words();w[6]=1
  for i in range(10,22):w[i]=1
  self.assertEqual(d.call('vcEnter',1,0,7,1),1);self.assertEqual(v.proc('rbHostCommitted',3,d),0);d.call('vcCommit');self.assertEqual(v.proc('rbHostCommitted',3,d),1)
  def ack():
   while w[126]:
    at=w[130];self.assertEqual(d.call('vcSetInput',0,1,w[4],w[5],4,at,w[132+at],w[136+at]),1);self.assertEqual(d.call('vcAcknowledge'),1);d.call('vcCommit');v.proc('rbHostCommitted',9,d)
  for slot in range(1,4):
   d.call('vcSetInput',0,1,w[2],w[3],1,0,0,0);self.assertEqual(d.call('vcBeginTurn'),1);d.call('vcCommit');self.assertEqual(v.proc('rbHostCommitted',4,d),1);ack()
   response=w[106+w[95]];d.call('vcSetInput',0,1,w[2],w[3],2,w[99],0,0);self.assertEqual(d.call('vcChoose',response),1);d.call('vcCommit');self.assertEqual(v.proc('rbHostCommitted',5,d),0)
   d.call('vcSetInput',0,1,w[2],w[3],2,w[99],0,0);self.assertEqual(d.call('vcCommitResponse'),1);self.assertEqual(v.proc('rbHostCommitted',6,d),0);d.call('vcCommit');before=list(w)
   self.assertEqual(v.proc('rbHostCommitted',6,d),1);self.assertEqual(v.proc('rbHostCommitted',6,d),0);self.assertEqual(list(w),before);ack()
  self.assertEqual(w[92],6);d.call('vcSetInput',0,1,w[2],w[3],3,0,0,0);self.assertEqual(d.call('vcCommitKO'),1);self.assertEqual(v.proc('rbHostCommitted',8,d),0);d.call('vcCommit');self.assertEqual(v.proc('rbHostCommitted',8,d),1);ack()
  self.assertEqual(v.status(15),1);self.assertEqual(v.status(16),3);self.assertEqual(v.status(17),1)
 def test_08_generation_exhaustion_stale_poll_and_highwater(self):
  v=self.vm();hi,lo=v.status(3),v.status(4);d,w=self.enter(v)
  before=len(v.sound_trace);self.assertEqual(v.proc('rbPoll',hi,lo,d),0);self.assertEqual(len(v.sound_trace),before)
  a=v.arrays(943);a['rbGenerationHi'][0]=32767;a['rbGenerationLo'][0]=32767
  self.assertEqual(v.proc('rbRequest',151),0);self.assertEqual(v.status(5),9);self.assertEqual(v.proc('rbAvailable'),0)
 def test_09_actual_domain_whole_concession_remains_nonko(self):
  v=self.vm();d=v.objects['contestState'];d.call('vcInit');d.call('vcBindGeneration',0,1);w=v.domain_words();w[6]=1
  for i in range(10,22):w[i]=1
  self.assertEqual(d.call('vcEnter',1,0,7,1),1);d.call('vcCommit');v.proc('rbHostCommitted',3,d)
  d.call('vcSetInput',0,1,w[2],w[3],1,0,0,0);self.assertEqual(d.call('vcYieldContest'),1);d.call('vcCommit');self.assertEqual(v.proc('rbHostCommitted',7,d),0)
  d.call('vcSetInput',0,1,w[2],w[3],3,0,0,0);self.assertEqual(d.call('vcCommitKO'),1);d.call('vcCommit')
  self.assertEqual(w[101],2);self.assertEqual(w[102],1);self.assertGreater(w[96],0);self.assertGreater(w[97],0);self.assertEqual(v.proc('rbHostCommitted',8,d),0)
  while w[126]:
   i=w[130];d.call('vcSetInput',0,1,w[4],w[5],4,i,w[132+i],w[136+i]);self.assertEqual(d.call('vcAcknowledge'),1);d.call('vcCommit');v.proc('rbHostCommitted',9,d)
  self.assertEqual(w[92],8);self.assertEqual(v.status(15),1);self.assertEqual(v.status(17),0)
