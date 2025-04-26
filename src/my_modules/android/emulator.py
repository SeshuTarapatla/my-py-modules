from datetime import datetime
from subprocess import check_output, run
from time import sleep
from typing import cast

import pyautogui as ag
from pygetwindow import Win32Window, getWindowsWithTitle

from my_modules.android.device import Device
from my_modules.process import spawn_windows_process, wait_in_loop


class Emulator:
    """Emulator class to control avd instance."""

    def __init__(self, avd: str = "emulator", serial: str = "emulator-5554") -> None:
        """Create emulator instance.

        Args:
            avd (str, optional): avd name. Defaults to "emulator".
            serial (str, optional): adb serial. Defaults to "emulator-5554".
        """
        self.avd: str = avd
        self.serial: str = serial
        self.console: str = "emulator-console"
        self.window: str = f"Android Emulator - {self.serial.replace('-', ':')}"

    def start(self, buffer: float = 10):
        """Start emulator as a separate process.

        Args:
            buffer (float, optional): Buffer wait after boot. Defaults to 10.
        """
        if self._is_running():
            return
        spawn_windows_process(
            cmd=f"emulator -avd {self.avd} -no-audio -gpu host -no-snapshot",
            title=self.console,
            minimized=True,
        )
        started_at = datetime.now()
        while not self._windows_exists():
            wait_in_loop(started_at, wait=180, err_msg="Failed to start the emulator.")
        self.snap_to_zone()
        while not self._boot_complete():
            wait_in_loop(started_at, wait=150, err_msg="Failed to start the emulator.")
        sleep(buffer)

    def stop(self) -> None:
        """Stop running emulator instance."""
        if emulator := self._emulator_window():
            emulator.close()
        if console := self._console_window():
            console.close()
        started_at = datetime.now()
        while self._windows_exists():
            wait_in_loop(started_at, wait=60, err_msg="Failed to kill the emulator.")

    def restart(self, buffer: float = 5):
        """Restart the emulator instance.

        Args:
            buffer (float, optional): Buffer wait between stop and start. Defaults to 5.
        """
        if self._is_running():
            self.stop()
            sleep(buffer)
        self.start()

    def snap_to_zone(self):
        """Snap window to right fancy zone."""
        window = self._emulator_window()
        if window.isMinimized:
            window.restore()
        window.activate()
        if window.top < 0:
            ag.click(window.left + 2, window.bottom - 2)
            ag.sleep(0.5)
        if not window.box == (1866, 0, 685, 1537):
            ag.keyDown("shift")
            ag.moveTo(window.left + 50, window.top + 30)
            ag.mouseDown()
            ag.moveTo(2000, 500)
            ag.mouseUp()
            ag.keyUp("shift")

    def get_device(self) -> Device:
        """Start emulator if not running and return uiautomator2 Device instance."""
        self.start()
        return Device(self.serial)

    def _is_running(self) -> bool:
        """Checks if emulator instance is up and running."""
        return self._windows_exists() and self._boot_complete()

    def _console_window(self) -> Win32Window:
        """Get Win32Window of emulator console."""
        window: list[Win32Window]
        if window := getWindowsWithTitle(self.console):
            return window[0]
        return cast(Win32Window, None)

    def _emulator_window(self) -> Win32Window:
        """Get Win32Window of emulator window."""
        window: list[Win32Window]
        if window := getWindowsWithTitle(self.window):
            return window[0]
        return cast(Win32Window, None)

    def _windows_exists(self) -> bool:
        """Checks if Android emulator and console windows exists."""
        return all([bool(x()) for x in (self._console_window, self._emulator_window)])

    def _boot_complete(self) -> bool:
        """Checks if sys.boot_completed is 1."""
        if self.serial in check_output("adb devices", text=True):
            return (
                run(
                    f"adb -s {self.serial} shell getprop sys.boot_completed",
                    text=True,
                    capture_output=True,
                ).stdout.strip()
                == "1"
            )
        return False

    def __str__(self) -> str:
        return f"Emulator(serial={self.serial}, avd={self.avd})"

    def __repr__(self) -> str:
        return self.__str__()
