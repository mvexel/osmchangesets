import requests
from ..changeset import Changeset


class API:
    def get_changeset(self, changeset_id) -> Changeset | None:
        """
        Get a changeset by its ID

        parameters:
        changeset_id: int

        returns:
        Changeset
        """
        response = requests.get(
            f"https://api.openstreetmap.org/api/0.6/changeset/{changeset_id}.json"
        )
        response.raise_for_status()
        return Changeset.from_osm_api_json(response.text)

    def get_changesets(self, changeset_ids: list[int]) -> list[Changeset]:
        """
        Get multiple changesets by their IDs

        parameters:
        changeset_ids: list[int]

        returns:
        list[Changeset]
        """
        changesets = []
        for changeset_id in changeset_ids:
            changesets.append(self.get_changeset(changeset_id))
        return changesets

    def query_changesets(
        self,
        display_name: str | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        closed: bool = True,
    ) -> list[Changeset]:
        """
        Query changesets

        parameters:
        display_name: str|None
        bbox: tuple[float]|None
        closed: bool

        returns:
        list[Changeset]
        """
        query_params = []
        if display_name:
            query_params.append(f"display_name={display_name}")
        if bbox:
            # see if this is a valid bounds
            if len(bbox) != 4:
                raise ValueError("bbox must be a tuple of 4 floats")
            if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
                raise ValueError(
                    "bbox must be in the form (minlon, minlat, maxlon, maxlat)"
                )
            query_params.append(f"bbox={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}")
        if closed:
            query_params.append("closed=true")

        query_url = f"https://api.openstreetmap.org/api/0.6/changesets.json?{'&'.join(query_params)}"
        response = requests.get(query_url)
        response.raise_for_status()
        changesets = []
        for changeset in response.json().get("changesets", []):
            changesets.append(Changeset.from_osm_api_json(changeset))
        return changesets

    def latest_changesets(self, limit: int = 100) -> list[Changeset]:
        """
        Get the latest changesets

        parameters:
        limit: int (default 100)

        returns:
        list[Changeset]
        """
        response = requests.get(
            f"https://api.openstreetmap.org/api/0.6/changesets.json?limit={limit}"
        )
        response.raise_for_status()
        changesets = []
        for changeset in response.json().get("changesets", []):
            changesets.append(Changeset.from_osm_api_json(changeset))
        return changesets
