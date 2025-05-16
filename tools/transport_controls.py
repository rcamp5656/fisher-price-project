# transport_controls.py
"""
Interpret Axiom 25 transport buttons (Record, Play, Rewind) via CC messages.
"""
# Axiom CC numbers for transport
CC_PLAY = 115
CC_RECORD = 117
CC_REWIND = 114


def is_control(event: tuple[int,int,int], cc_num: int) -> bool:
    """Return True if the event is a Control Change cc_num with value > 0."""
    status, ctrl, value = event
    return (status & 0xF0) == 176 and ctrl == cc_num and value > 0


def handle_transport(event: tuple[int,int,int], state: dict):
    """Toggle or trigger record/play/rewind flags in state."""
    if is_control(event, CC_RECORD):
        state['record'] = not state.get('record', False)
    elif is_control(event, CC_PLAY):
        state['play'] = True
    elif is_control(event, CC_REWIND):
        state['rewind'] = True
