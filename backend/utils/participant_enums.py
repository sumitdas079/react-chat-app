from enum import IntEnum

class ConversationType(IntEnum):
    ONE_ON_ONE = 1
    GROUP = 2

class ParticipantNumber(IntEnum):
    ONE_ON_ONE = 2
    GROUP = 100

def validate_conversation_type(value: int) -> ConversationType:
    try:
        return ConversationType(value)
    except ValueError:
        raise ValueError(f"Invalid conversation type: {value}. Valid types are: {[e.value for e in ConversationType]}")