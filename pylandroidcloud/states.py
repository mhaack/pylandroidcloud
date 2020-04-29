from enum import IntEnum


class MowerCode(IntEnum):
    UNKNOWN = -1
    IDLE = 0
    HOME = 1
    START_SEQUNCE = 2
    LEAVING_HOME = 3
    FOLLOW_WIRE = 4
    SEARCHING_HOME = 5
    SEARCHING_WIRE = 6
    MOWING = 7
    LIFTED = 8
    TRAPPED = 9
    BLADE_BLOCKED = 10
    DEBUG = 11
    REMOTE_CONTROL = 12
    GOING_HOME = 30
    ZONE_TRAINING = 31
    BORDER_CUT = 32
    SEARCHING_ZONE = 33
    PAUSE = 34


class MowerErrorCode(IntEnum):
    UNKNOWN = -1
    NO_ERROR = 0
    TRAPPED = 1
    LIFTED = 2
    WIRE_MISSING = 3
    OUTSIDE_WIRE = 4
    RAINING = 5
