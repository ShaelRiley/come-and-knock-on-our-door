"""Small native dispatch/display/restore hooks for the independently typed source ledger."""
from source_tools import methods
from source_derivation import merge,insert,replace

def reader_hooks(output):
    mm=methods(output['main.sc']);hooks={}
    hooks['dialogueOpen']=insert(mm['dialogueOpen'],'(if (and p08 (p08 h8ReaderCheck: 2 arg1)) (return (p08 h8ReaderOpen: arg1)))')
    hooks['uiOpenReader']=insert(mm['uiOpenReader'],'(if (and p08 (p08 h8ReaderCheck: 2 arg1)) (return 0))')
    render=insert(mm['render'],'(if p08 (p08 h8ReaderFrame: 0))')
    before='''            L_141e: pushi 6
            pushi 12
            push0
            push0
            pushi 200
            pushi 320
            push1
            callk Graph, 12
            ldi 0
            aTop dirty'''
    after='''            L_141e: pToa p08
            bnt H8_reader_legacy_flush
            pushi #h8ReaderFrame
            push1
            push1
            pToa p08
            send 6
            jmp H8_reader_flush_done
            H8_reader_legacy_flush: pushi 6
            pushi 12
            push0
            push0
            pushi 200
            pushi 320
            push1
            callk Graph, 12
            H8_reader_flush_done: ldi 0
            aTop dirty'''
    hooks['render']=replace(render,before,after)
    hooks['dialoguePresented']=insert(mm['dialoguePresented'],'(if p08 (p08 h8ReaderPresented:))')
    hooks['uiHostClosed']=insert(mm['uiHostClosed'],'(if p08 (p08 h8ReaderClosed:))')
    hooks['bridgeBegin']=insert(mm['bridgeBegin'],'(if p08 (p08 h8ReaderRetire: 1))')
    hooks['hostRoomChanged']=insert(mm['hostRoomChanged'],'(if (and p08 (or (!= roomSeen location) (!= apronSeen onApron))) (p08 h8ReaderRetire: 1))')
    hooks['p05RetireTransient']=insert(mm['p05RetireTransient'],'(if p08 (p08 h8ReaderRetire: 4))')
    for name in ('uiBuildFocus','uiTurnPage','uiRender'):
        if 'ldi 234' in mm[name]:hooks[name]=replace(mm[name],'ldi 234','ldi 235')
    output['main.sc']=merge(output['main.sc'],hooks)
    mm=methods(output['module989.sc']);hooks={}
    supported=replace(mm['h8SupportedHistory'],'(< i S_PLACE_CERAMIC_CARRIER)','(< i S_SOURCE_CIRCULATION_PLAN)')
    supported=replace(supported,'(return 1))','(return (self h8ReaderRestore: 0)))')
    hooks['h8SupportedHistory']=supported
    hooks['h8RestoreFinish']=replace(mm['h8RestoreFinish'],'(= h8RestoreValid 1) (= h8Restoring 0) (= h8Enabled 1)',
        '(if (not (self h8ReaderRestore: 1)) (return (self h8RestoreReject:)))\n (= h8RestoreValid 1) (= h8Restoring 0) (= h8Enabled 1)')
    for name in ('h8LayoutRetire','h8LayoutMenu','h8LayoutChoice','h8LayoutRestore'):
        body=mm[name].replace('234)','235)')
        # Only the context upper bound changes; the overlap switch234 remains exact.
        hooks[name]=body
    menu=hooks['h8LayoutMenu']
    menu=replace(menu,'(if (== context 231) 4 else (if (== context 232) 2 else (if (== context 233) 6 else 5)))',
        '(if (== context 235) 3 else (if (== context 231) 4 else (if (== context 232) 2 else (if (== context 233) 6 else 5))))')
    menu=replace(menu,'(switch context','(switch context\n   (235 (= label (if (== i 1) (h8Host uiHostItemLabel: 53) else (if (== i 2) (h8Host uiHostItemLabel: 83) else (self h8LayoutLabel: 122)))))')
    hooks['h8LayoutMenu']=menu
    choice=hooks['h8LayoutChoice']
    choice=replace(choice,'(switch context','(switch context\n  (235 (if (<= value 3) (self h8ReaderAction: (+ 12 value))))')
    hooks['h8LayoutChoice']=choice
    first=replace(mm['h8LayoutFirst'],'(if (== object 122) (self h8LayoutMenu: 230 0 7) (return 1))',
        '(if (== object 122) (self h8LayoutMenu: (if (or (== verb 5) (== verb 2)) 235 else 230) 0 7) (return 1))')
    hooks['h8LayoutFirst']=first
    dispatch=replace(mm['h8LayoutDispatch'],'(if (== object 122) (self h8LayoutMenu: 230 0 7) (return 1))',
        '(if (== object 122) (self h8LayoutMenu: (if (or (== action 5) (== action 2)) 235 else 230) 0 7) (return 1))\n (if (and (== object 40) (== action 5) (not target)) (self h8ReaderAction: 5) (return 1))')
    hooks['h8LayoutDispatch']=dispatch
    output['module989.sc']=merge(output['module989.sc'],hooks)
    return output
