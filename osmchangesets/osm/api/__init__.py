import requests

from ..changeset import Changeset


class API:
    def get_changeset(self, changeset_id) -> Changeset | None:
        response = requests.get(
            f"https://api.openstreetmap.org/api/0.6/changeset/{changeset_id}.json"
        )
        response.raise_for_status()
        return Changeset.from_osm_api_json(response.text)
