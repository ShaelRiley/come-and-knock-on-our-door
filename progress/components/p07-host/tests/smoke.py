from host import *
h,d,a,p,q,r=setup();s=h.vm.objects['p07State'];print('INIT',s.p['h7Enabled'],s.call('h7PhysicalValid'),s.call('h7Context'),s.call('h7SaveReady'));frame(h)
act(h,0,12);print('KITCHEN',h.p['location']);frame(h)
print('controls',h.p['uiControlCount']);h.call('hostActNow',5,86,0);print('READ',h.p['uiPanel'],h.p['uiDocument'],s.p['h7LastCode'],s.p['h7PendingPages']);frame(h);print('FIRST',s.p['h7SeenCount'],s.call('p07Projection',0));h.call('uiTurnPage',1);frame(h);print('SECOND',s.p['h7SeenCount'],s.call('p07Projection',0),s.p['h7LastCode']);close(h)
for v,o,t in [(7,87,92),(7,89,90)]:act(h,v,o,t);print('ACT',v,o,t,h.p['uiPanel'],h.p['uiChoiceContext'],s.p['h7LastCode'])
choice(h,227,2);print('MEASURE',s.p['h7LastCode']);
for v,o,t in [(7,90,92),(7,88,92),(7,94,0),(7,94,0),(7,91,92),(3,93,0)]:act(h,v,o,t);print('ACT',v,o,t,s.p['h7LastCode'],s.call('p07Projection',7),s.call('p07Projection',0))
print('DONE',s.call('h7SaveReady'),s.p['h7ReadyEvents'],h.vm.steps)
