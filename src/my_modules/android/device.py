from uiautomator2 import Device as _Device

__all__ = ["Device"]


class Device(_Device):
    def __init__(self, serial: str):
        super().__init__(serial)
