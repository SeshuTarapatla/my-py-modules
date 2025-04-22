from datetime import datetime
from pathlib import Path

from adbutils import adb
from adbutils._device import AdbDevice  # type: ignore
from uiautomator2 import Device as _Device
from uiautomator2._selector import UiObject

from my_modules.process import wait_in_loop


class Device(_Device):
    """Class that extends uiautomator2 Device class functionality."""

    def __init__(self, serial: str = ""):
        """Init ADB device with serial.

        Args:
            serial (str, optional): ADB Device serial. Defaults to "".
        """        
        self.serial = serial
        self.adb: AdbDevice = adb.device(serial)
    
    def init(self) -> None:
        """Lazy init to handle emulator boot up."""
        started_at = datetime.now()
        while not (self.adb.getprop("sys.boot_completed") == "1" and self.adb.getprop("init.svc.bootanim") == "stopped"):
            wait_in_loop(started_at, err_message="Emulator not booted")
        super().__init__(self.serial)
        self.width, self.height = self.window_size()
    
    def __kwargs__(self, resourceId: str = "", text: str = "", **kwargs) -> dict[str, str]:
        """Helper function to handle optional kwargs."""
        if resourceId:
            kwargs["resourceId"] = resourceId
        if text:
            kwargs["text"] = text
        return kwargs
    
    def __call__(self, resourceId: str = "", text: str = "", **kwargs) -> UiObject:
        """Returns matching UiObjects."""
        kwargs = self.__kwargs__(resourceId, text)
        return super().__call__(**kwargs)

    def get_elements(self, resourceId: str = "", text: str = "", **kwargs) -> list[UiObject]:
        """Get a list of UiObjects that matches with input attributes."""
        kwargs = self.__kwargs__(resourceId, text)
        self(**kwargs).wait(timeout=5)
        return [element for element in self(**kwargs)]
    
    def dump_hierarchy(self, compressed=False, pretty=False, max_depth: int | None = None, filename="hierarchy.txt") -> str:
        """Dumps device ui hierarchy into a file."""
        data = super().dump_hierarchy(compressed, pretty, max_depth)
        Path(filename).write_text(data, encoding="utf-8", newline="")
        return "Dumped"

    def scroll_list(self, resourceId: str, border_threshold: int = 60, duration: float = 0.8) -> None:
        """Function to scroll lists.

        Args:
            resourceId (str): Ui element resource in the list.
            border_threshold (int, optional): last element minimum height in pixels. Defaults to 60.
            duration (float, optional): swipe duration in seconds. Defaults to 0.8.
        """
        def element_height(element: UiObject) -> int:
            """Helper function to calculate ui element height."""
            _,y1,_,y2 = element.bounds()
            return y2-y1

        elements = self.get_elements(resourceId)
        if len(elements) == 1:
            raise Exception("Not enough elements to scroll.")
        first = elements[0]
        last = elements[-1]
        # check if last element is below threshold
        if element_height(last) <= 60:
            if len(elements) == 2:
                raise Exception("Not enough elements to scroll.")
            # if yes replace it with last but one element
            last = elements[-2]
        self.swipe(*last.center(), *first.center(), duration=duration)
    
    def get_text(self, resourceId: str, default: str = "") -> str:
        """Get text of a given resourceId element if exists else return default.
        """
        if self(resourceId).exists:
            return self(resourceId).get_text()
        else:
            return default
    
    def animation_wait(self, timeout: float = 10) -> None:
        """Wait in loop until device animation completes."""
        started_at = datetime.now()
        last = None
        while (curr := self.screenshot()) != last:
            last = curr
            wait_in_loop(started_at, buffer=0.2, wait_limit=timeout, err_message="Invalid animation")
    
    def proper_child(self, child: UiObject, parent: UiObject) -> bool:
        """Checks if child element is a proper child of parent element by checking if child is inside bounds of parent.

        Args:
            child (UiObject): child element.
            parent (UiObject): parent element.

        Returns:
            bool: if child or not.
        """
        cx1, cy1, cx2, cy2 = child.bounds()
        px1, py1, px2, py2 = parent.bounds()

        return (
            cx1 >= px1 and
            cy1 >= py1 and
            cx2 <= px2 and
            cy2 <= py2
        )
    
