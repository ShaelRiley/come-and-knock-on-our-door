"""New narrow P04 handoff bridge; NOT recovered historical symbolic P04.

The seven named fields and final unused tuple follow P11's observed import and
positional test contract. The original eighth field name is not recovered.
Only the pinned numeric P04 owner changes gate/peg state. This projection is
read-only and contains no peg toggle, repair, completion or actor relocation.
"""
from dataclasses import dataclass
from dependencies.p04_numeric_model import P04, State, Gate


@dataclass(frozen=True)
class GateHandoff:
    peg_id: str
    peg_location: str
    tested: bool
    peg_available: bool
    peg_engaged: bool
    gate_open: bool
    wedge_in_gate: bool
    compatibility_tail: tuple = ()


def project_gate(owner: P04) -> GateHandoff:
    """Snapshot the validated accepted owner; this never grants P04 progress."""
    if type(owner) is not P04 or type(owner.state) is not State:
        raise ValueError("Expected the pinned numeric P04 owner")
    if any(type(value) is bool or not isinstance(value, int)
           for value in vars(owner.state).values()) or not owner.validate():
        raise ValueError("Invalid numeric P04 state")
    return GateHandoff("hold_open_peg", "L04_SIDE_PASSAGE", owner.tested,
                       owner.peg_available, bool(owner.state.peg),
                       owner.state.gate == Gate.OPEN, bool(owner.state.wedge))
