from pathlib import Path
from PIL.Image import Image
from uiautomator2 import Device as _Device
from uiautomator2._selector import Selector, UiObject as _UiObject

__all__ = ["Device", "UiObject"]


def __handle_kwargs__(
    resourceId: str = "", text: str = "", description: str = "", **kwargs
) -> dict[str, str]:
    """Helper function to handle input kwargs."""
    if resourceId:
        kwargs["resourceId"] = resourceId
    if text:
        kwargs["text"] = text
    if description:
        kwargs["description"] = description
    return kwargs


class UiObject(_UiObject):
    def __init__(self, session, selector: Selector):
        super().__init__(session, selector)
        self._bounds = None
    
    def __getitem__(self, instance: int):
        object = super().__getitem__(instance)
        return UiObject(object.session, object.selector)

    def bounds(self) -> tuple[int, int, int, int]:
        if not self._bounds:
            self._bounds = super().bounds()
        return self._bounds
    
    @property
    def height(self) -> int:
        _,y1,_,y2 = self.bounds()
        return y2-y1
    
    @property
    def width(self) -> int:
        x1,_,x2,_ = self.bounds()
        return x2-x1
    
    @property
    def dimensions(self) -> tuple[int, int]:
        x1,y1,x2,y2 = self.bounds()
        width = x2-x1
        height = y2-y1
        return (width, height)

    def sibling(self, resourceId: str = "", *, text: str = "", description: str = "", **kwargs):
        kwargs = __handle_kwargs__(resourceId, text, description, **kwargs)
        object = super().sibling(**kwargs)
        return UiObject(object.session, object.selector)

    def get_text(self, timeout=None, default: str = ""):
        if self.exists:
            return super().get_text(timeout)
        else:
            return default


class Device(_Device):
    def __init__(self, serial: str):
        super().__init__(serial)

    def __call__(
        self, resourceId: str = "", *, text: str = "", description: str = "", **kwargs
    ) -> UiObject:
        kwargs = __handle_kwargs__(resourceId, text, description, **kwargs)
        return UiObject(self, Selector(**kwargs))

    def get_elements(
        self, resourceId: str = "", *, text: str = "", description: str = "", **kwargs
    ) -> list[UiObject]:
        """Return a list of ui elements matching input args."""
        kwargs = __handle_kwargs__(resourceId, text, description, **kwargs)
        return [element for element in self(**kwargs)]

    def dump_hierarchy(
        self,
        compressed=False,
        pretty=False,
        max_depth: int | None = None,
        dest: Path = Path("./hierarchy.txt"),
    ) -> str:
        """Modified dump_hierarchy to dump to file instead of console."""
        data = super().dump_hierarchy(compressed, pretty, max_depth)
        dest.write_text(data, encoding="utf-8", newline="")
        return "dumped"

    def search_hierarchy(self, text: str) -> list[str]:
        """Search wrapper that returns lines in ui hierarchy dump that contains given text content."""
        self.dump_hierarchy()
        data = super().dump_hierarchy().splitlines()
        return [
            line.strip().split(" checkable")[0] + ">" for line in data if text in line
        ]
    
    def screenshot(self, filename: str | None = None, format="pillow", display_id: int | None = None) -> Image:
        """Get screenshot of current ui display."""
        return super().screenshot(filename, format, display_id)

    def scroll_list(self, batch: list[UiObject], duration: float = 1) -> None:
        """Scroll a continous list of Ui elements.

        Args:
            batch (list[UiObject]): ui elements in list.
            duration (float, optional): swipe duration in seconds. Defaults to 1.
        """        
        if len(batch) < 2:
            return
        first = batch[0]
        last = batch[-1]
        self.swipe(*last.center(), *first.center(), duration=duration)
