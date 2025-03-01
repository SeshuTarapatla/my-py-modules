from adbutils import adb, AdbError


class NoDeviceFound(AdbError):
    """No android/adb devices connected to the pc."""


class ADB:
    """Common adb methods"""

    @staticmethod
    def list_device() -> list[str]:
        """Returns a list of serials of connected adb devices."""
        return [device.serial for device in adb.device_list()]

    @staticmethod
    def is_connected(serial: str) -> bool:
        """Checks of given serial is connected or not."""
        return serial in ADB.list_device()

    @staticmethod
    def default_device() -> str:
        """Returns serial of the first device connected. Raises `NoDeviceFound` exception if no devices are connected."""
        if devices := ADB.list_device():
            return devices[0]
        raise NoDeviceFound("No adb devices connected.")
    