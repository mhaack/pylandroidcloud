# pylandroidcloud
REST API client for the Worx Landroid API

This is an unofficial REST API client for controlling Worx Landroid lawnmowers.

## Supported devices
All cloud connected Worx Landroid lawnmowers.

## Example

```
import logging
import pylandroidcloud

_LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = "1"
CLIENT_SECRET = r"nCH3A0WvMYn66vGorjSrnGZ2YtjQWDiCvjg7jNxK"
USERNAME = "<username>"
PASSWORD = "<passwors>"

API = pylandroidcloud.LandroidAPI(CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD)
_LOGGER.debug(f"Got auth {API}")

MOWERS = pylandroidcloud.LandroidMowerList(API)
_LOGGER.debug(f"Got mowers {len(MOWERS.mowers)}")

M = pylandroidcloud.LandroidMower(API, "30173702170204017460", 60)
_LOGGER.debug(f"Got mower {M.mower.name}")

for mower in MOWERS.mowers:
    mower_state = pylandroidcloud.LandroidMowerState(API, mower.serial_number,)
    _LOGGER.debug(f"Got mower state {mower_state}")

```

## Credits

The initial idea for this project started with the plan to create some native Home Assistant integration for connected Worx Landroid lawnmowers. A [Domoticz forum post](https://easydomoticz.com/forum/viewtopic.php?t=8246) gave the information for the first prototype. They get the credit for reverse engineering the API.

@tetienne with his [somfy-open-api](https://github.com/tetienne/somfy-open-api) also was a very good inspiration to bootstrap this project.
