import logging

import pylandroidcloud

_LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = "1"
CLIENT_SECRET = r"nCH3A0WvMYn66vGorjSrnGZ2YtjQWDiCvjg7jNxK"
USERNAME = "markus.haack@gmail.com"
PASSWORD = "natnyb-Vyjjiz-2piqqy"

API = pylandroidcloud.LandroidAPI(CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD)
_LOGGER.debug(f"Got auth {API}")

MOWERS = pylandroidcloud.LandroidMowerList(API)
_LOGGER.debug(f"Got mowers {len(MOWERS.mowers)}")

M = pylandroidcloud.LandroidMower(API, "30173702170204017460", 60)
_LOGGER.debug(f"Got mower {M.mower.name}")

for mower in MOWERS.mowers:
    mower_state = pylandroidcloud.LandroidMowerState(API, mower.serial_number)
    _LOGGER.debug(f"Got mower state {mower_state}")
    if mower_state.state is not None:
        _LOGGER.debug(f"Got mower state code {mower_state.state.status_code}")
        _LOGGER.debug(f"Got mower battery {mower_state.state.battery.level}")
