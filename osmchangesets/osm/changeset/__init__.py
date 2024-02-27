from datetime import datetime
import json
from dataclasses import dataclass
from typing import Self, ClassVar

import iso8601


class ChangesetError(Exception):
    pass


class InvalidChangesetJson(ChangesetError):
    pass


@dataclass
class Bounds:
    minlat: float
    minlon: float
    maxlat: float
    maxlon: float

    @property
    def is_valid(self) -> bool:
        return (
            self.minlat is not None
            and self.minlon is not None
            and self.maxlat is not None
            and self.maxlon is not None
            and self.maxlat - self.minlat > 0
            and self.maxlon - self.minlon > 0
        )

    @property
    def area(self) -> float:
        if not self.is_valid:
            return 0.0

        from pyproj import Geod

        geod = Geod(ellps="WGS84")
        lons = [self.minlon, self.maxlon, self.maxlon, self.minlon]
        lats = [self.minlat, self.minlat, self.maxlat, self.maxlat]
        area, _ = geod.polygon_area_perimeter(lons, lats)
        return area

    @property
    def wkt(self) -> str | None:
        if not self.is_valid:
            return None

        return f"POLYGON(({self.minlon} {self.minlat},{self.maxlon} {self.minlat},{self.maxlon} {self.maxlat},{self.minlon} {self.maxlat},{self.minlon} {self.minlat}))"

    @property
    def geojson(self) -> dict:
        return {
            "type": "Polygon",
            "coordinates": [
                [
                    [self.minlon, self.minlat],
                    [self.maxlon, self.minlat],
                    [self.maxlon, self.maxlat],
                    [self.minlon, self.maxlat],
                    [self.minlon, self.minlat],
                ]
            ],
        }


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
    created_at: datetime
    closed_at: datetime
    is_open: bool
    user: str
    uid: int
    bounds: Bounds
    comments_count: int
    changes_count: int
    tags: list[Tag]

    @classmethod
    def from_osm_api_json(cls, data: str) -> Self:
        # this could be a dict or a string
        if isinstance(data, dict):
            changeset = data
        else:
            try:
                changeset = json.loads(data).get("elements")[0]
            except (KeyError, IndexError):
                try:
                    changeset = json.loads(data)
                except (KeyError, IndexError):
                    raise InvalidChangesetJson

        # parse ISO8601 dates
        if "created_at" in changeset:
            changeset["created_at"] = iso8601.parse_date(
                changeset.get("created_at", None)
            )

        if "closed_at" in changeset:
            changeset["closed_at"] = iso8601.parse_date(
                changeset.get("closed_at", None)
            )

        # bounds can be defined by minlat, minlon, maxlat, maxlon or min_lat, min_lon, max_lat, max_lon depending on the API call
        if "minlat" in changeset:
            changeset["min_lat"] = changeset.pop("minlat")
            changeset["min_lon"] = changeset.pop("minlon")
            changeset["max_lat"] = changeset.pop("maxlat")
            changeset["max_lon"] = changeset.pop("maxlon")
        return cls(
            osm_id=changeset.get("id", None),
            created_at=changeset.get("created_at", None),
            closed_at=changeset.get("closed_at", None),
            is_open=changeset.get("open", False),
            user=changeset.get("user", None),
            uid=changeset.get("uid", None),
            bounds=Bounds(
                minlat=changeset.get("min_lat", None),
                minlon=changeset.get("min_lon", None),
                maxlat=changeset.get("max_lat", None),
                maxlon=changeset.get("max_lon", None),
            ),
            comments_count=changeset.get("comments_count", 0),
            changes_count=changeset.get("changes_count", 0),
            tags=[Tag(key=k, value=v) for k, v in changeset.get("tags", {}).items()],
        )
