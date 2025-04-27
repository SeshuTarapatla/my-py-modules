from pathlib import Path
from uiautomator2 import Device as _Device

__all__ = ["Device"]


class Device(_Device):
    def __init__(self, serial: str):
        super().__init__(serial)

    def dump_hierarchy(
        self,
        compressed=False,
        pretty=False,
        max_depth: int | None = None,
        dest: Path = Path("./hierarchy.txt"),
    ) -> str:
        """Modified dump_hierarchy to dump to file instead of console."""
        data = super().dump_hierarchy(compressed, pretty, max_depth)
        dest.write_text(data)
        return "dumped"

    def search_hierarchy(self, text: str) -> list[str]:
        """Search wrapper that returns lines in ui hierarchy dump that contains given text content."""
        data = super().dump_hierarchy().splitlines()
        return [line.strip().split(" checkable")[0] + ">" for line in data if text in line]
