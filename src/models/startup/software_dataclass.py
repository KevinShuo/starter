import dataclasses
from typing import Optional


@dataclasses.dataclass
class SoftwareData:
    _id: int
    name: str
    path: str
    ico: str
    tab: str
    description: Optional[str] = None
    version: Optional[str] = None

    def __hash__(self):
        return hash((self._id, self.name, self.path, self.ico, self.tab, self.description, self.version))
