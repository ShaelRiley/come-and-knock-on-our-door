"""Typed offline contract model, not SCI or permission to integrate."""
from dataclasses import dataclass

@dataclass
class Broker:
    owner: int = 151
    desired: int = 151
    generation: int = 0
    state: str = 'bed'
    paused: bool = False
    muted: bool = False
    chooser: bool = False
    preference: int = 100
    bridge: int | None = None
    bridge_generation: int | None = None
    clock: int = 12
    last_settled: int = 151
    retired: int = 0
    replayed_transients: int = 0
    static_valid: bool = True

    def request(self,target):
        if target not in (151,152):raise ValueError('Unsupported target')
        self.generation+=1;self.desired=target
        return self.generation

    def poll(self,gate,observed,second,request_generation,context_valid=True):
        if self.state!='bed' or self.desired==self.owner:return False
        if self.paused or self.muted or self.chooser or not self.static_valid:return False
        if not context_valid or request_generation!=self.generation:return False
        if not gate['dispatch_first']<=observed<=second<=gate['dispatch_last']:return False
        # Atomic model transaction: exactly one owner replaced, never two parsers.
        self.retired+=1;self.bridge=gate['bridge_resource'];self.owner=self.bridge
        self.bridge_generation=self.generation;self.state='bridge';self.clock=0
        return True

    def finish_bridge(self,all_keys_released,context_valid=True):
        if self.state!='bridge' or self.paused or self.chooser:return False
        if not all_keys_released or not context_valid or not self.static_valid:return False
        self.retired+=1;self.owner=self.desired;self.last_settled=self.owner
        self.bridge=None;self.bridge_generation=None;self.state='bed';self.clock=0
        return True

    def before_chooser(self):
        if self.chooser:return False
        self.chooser=True;return True

    def cancel_chooser(self):
        if not self.chooser:return False
        self.chooser=False;return True

    def restore(self,validated_target,fresh_static_valid):
        # Transient one-shots are discarded; committed domain reconciliation supplies target.
        self.generation+=1;self.static_valid=fresh_static_valid;self.bridge=None
        self.bridge_generation=None;self.chooser=False;self.clock=0
        if not fresh_static_valid:self.state='unavailable';self.owner=0;return False
        if validated_target not in (151,152):raise ValueError('Unvalidated family')
        self.owner=self.desired=self.last_settled=validated_target;self.state='bed'
        return True
