import json
from dataclasses import dataclass
from typing import Self, ClassVar

import iso8601


class ChangesetError(Exception):
    pass


class InvalidChangesetJson(ChangesetError):
    pass


@dataclass
class Tag:
    changeset_id: ClassVar[int]
    key: str
    value: str

    def __dict__(self) -> dict:
        return {self.key: self.value}


@dataclass
class Changeset:
    osm_id: int
    created_at: int
    closed_at: int
    open: bool
    user: str
    uid: int
    minlat: float
    minlon: float
    maxlat: float
    maxlon: float
    comments_count: int
    changes_count: int
    tags: list[Tag]

    @classmethod
    def from_osm_api_json(cls, data: str) -> Self:
        try:
            changeset = json.loads(data).get("elements")[0]
        except (KeyError, IndexError):
            raise InvalidChangesetJson(data)

        # parse ISO8601 dates
        if "created_at" in changeset:
            changeset["created_at"] = iso8601.parse_date(changeset["created_at"])

        if "closed_at" in changeset:
            changeset["closed_at"] = iso8601.parse_date(changeset["closed_at"])

        return cls(
            osm_id=changeset["id"],
            created_at=changeset["created_at"],
            closed_at=changeset["closed_at"],
            open=changeset["open"],
            user=changeset["user"],
            uid=changeset["uid"],
            minlat=changeset["minlat"],
            minlon=changeset["minlon"],
            maxlat=changeset["maxlat"],
            maxlon=changeset["maxlon"],
            comments_count=changeset["comments_count"],
            changes_count=changeset["changes_count"],
            tags=[
                Tag(key=k, value=v)
                for k, v in changeset.get("tags", {}).items()
            ],
        )

    @property
    def area(self) -> float | None:
        if not all([self.minlat, self.minlon, self.maxlat, self.maxlon]):
            return None

        from pyproj import Geod

        geod = Geod(ellps="WGS84")
        lons = [self.minlon, self.maxlon, self.maxlon, self.minlon]
        lats = [self.minlat, self.minlat, self.maxlat, self.maxlat]
        area, _ = geod.polygon_area_perimeter(lons, lats)
        return area
