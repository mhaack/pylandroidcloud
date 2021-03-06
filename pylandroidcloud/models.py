from datetime import datetime
from typing import Any, Dict, List, Optional, cast

from pylandroidcloud.states import MowerCode, MowerErrorCode

# pylint: disable=unused-argument,line-too-long,too-many-instance-attributes


class Mower:
    __slots__ = "id", "serial_number", "name", "mac_address", "online", "locked"

    def __init__(
        self,
        *,
        id: int,
        serial_number: str,
        mac_address: str,
        name: str,
        online: bool,
        locked: bool,
        **kwargs: Any
    ):
        self.id = id
        self.serial_number = serial_number
        self.name = name
        self.mac_address = mac_address
        self.online = online
        self.locked = locked


class MowerStatus:
    __slots__ = (
        "status_code",
        "error_code",
        "config",
        "battery",
        "statistics",
        "orientation",
        "wifi_rsi",
        "last_update",
    )

    def __init__(self, cfg: Dict[str, Any], dat: Dict[str, Any], **kwargs: Any):
        self.status_code = MowerCode(cast(int, dat.get("ls")))
        self.error_code = MowerErrorCode(cast(int, dat.get("le")))
        self.config = Config(str(dat.get("fw")), **cfg)
        self.battery = Battery(dat.get("bt"))
        self.statistics = Statistics(**dat.get("st"))  # type: ignore
        self.orientation = Orientation(cast(List[float], dat.get("dmp")))
        self.wifi_rsi = dat.get("rsi")
        self.last_update = datetime.strptime(
            str(cfg.get("dt")) + " " + str(cfg.get("tm")), "%d/%m/%Y %H:%M:%S"
        )


class Config:
    __slots__ = "rain_delay", "serial_number", "firmware"

    def __init__(self, fw: str, rd: int, sn: str, **kwargs: Any):
        self.rain_delay = rd
        self.serial_number = sn
        self.firmware = fw


class Battery:
    __slots__ = "temperature", "voltage", "level", "carching", "charge_cycle"

    def __init__(self, battery_data: Optional[Any]):
        if battery_data is not None:
            self.temperature = battery_data.get("t")
            self.voltage = battery_data.get("v")
            self.level = battery_data.get("p")
            self.carching = battery_data.get("c")
            self.charge_cycle = battery_data.get("nr")


class Statistics:
    __slots__ = "blade_time", "work_time", "total_distance"

    def __init__(self, b: int, d: int, wt: int):
        self.blade_time = b
        self.work_time = wt
        self.total_distance = d


class Orientation:
    __slots__ = "pitch", "yaw", "roll"

    def __init__(self, dmp: List[float]):
        self.pitch = dmp[0]
        self.yaw = dmp[1]
        self.roll = dmp[2]
