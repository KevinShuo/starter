import dataclasses


@dataclasses.dataclass
class SoftwareData:
    _id: int
    name: str
    path: str
    ico: str
    tab: str

    def __hash__(self):
        return hash((self._id, self.name, self.path, self.ico, self.tab))
