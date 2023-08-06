from functools import lru_cache
from .chromecast import get_chromecasts


@lru_cache()
def get_devices():
    devices = {}
    for obtain_devices in [get_chromecasts]:
        devices.update(obtain_devices())
    return devices
