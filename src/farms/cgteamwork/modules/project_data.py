import dataclasses


@dataclasses.dataclass
class ProjectData:
    name: str
    full_name: str
    status: str
    database: str
    image: str
    frame_rate: int
    resolution: str

    def __str__(self):
        return (f"{'=' * 40}\n"
                f"项目名: {self.name}\n"
                f"数据库: {self.database}\n"
                f"图片: {self.image}\n"
                f"帧数: {self.frame_rate}\n"
                f"分辨率: {self.resolution}\n"
                f"{'=' * 40}\n\n")

    def __eq__(self, other):
        if not isinstance(other, ProjectData):
            return NotImplemented
        return (self.name == other.name and
                self.full_name == other.full_name and
                self.status == other.status and
                self.database == other.database and
                self.image == other.image and
                self.frame_rate == other.frame_rate and
                self.resolution == other.resolution)

    def __repr__(self):
        return (f"ProjectData(name={self.name!r}, full_name={self.full_name!r}, status={self.status!r}, "
                f"database={self.database!r}, image={self.image!r}, frame_rate={self.frame_rate!r}, "
                f"resolution={self.resolution!r})")

    def __hash__(self):
        return hash(
            (self.name, self.full_name, self.status, self.database, self.image, self.frame_rate, self.resolution))
