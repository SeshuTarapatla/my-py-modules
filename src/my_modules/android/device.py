from pathlib import Path
from uiautomator2 import Device as _Device
from uiautomator2._selector import UiObject

__all__ = ["Device"]


class Device(_Device):
    def __init__(self, serial: str):
        super().__init__(serial)

    def __call__(
        self, resourceId: str = "", *, text: str = "", description: str = "", **kwargs
    ) -> UiObject:
        kwargs = self.__handle_kwargs__(resourceId, text, description, **kwargs)
        return super().__call__(**kwargs)

    def __handle_kwargs__(
        self, resourceId: str = "", text: str = "", description: str = "", **kwargs
    ) -> dict[str, str]:
        """Helper function to handle input kwargs."""
        if resourceId:
            kwargs["resourceId"] = resourceId
        if text:
            kwargs["text"] = text
        if description:
            kwargs["description"] = description
        return kwargs

    def get_elements(
        self, resourceId: str = "", text: str = "", description: str = "", **kwargs
    ) -> list[UiObject]:
        """Return a list of ui elements matching input args."""
        kwargs = self.__handle_kwargs__(resourceId, text, description)
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
