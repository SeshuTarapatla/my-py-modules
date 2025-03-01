from uiautomator2 import Device as BaseDevice

from .adb import ADB


class Device(BaseDevice):
    """uiautomator2 device class with extended functionality."""

    def __init__(self, serial: str | None = None):
        """Create uiautomator2 device object.

        Args:
            serial (str, optional): device serial to connect. Defaults to None.
        """
        if serial is None:
            serial = ADB.default_device()
        super().__init__(serial)
