from typing import assert_type

import iso8601

from osmchangesets.osm.changeset import Changeset, Tag

valid_changeset_json = """
{
  "version": "0.6",
  "generator": "CGImap 0.8.10 (154593 spike-06.openstreetmap.org)",
  "copyright": "OpenStreetMap and contributors",
  "attribution": "http://www.openstreetmap.org/copyright",
  "license": "http://opendatacommons.org/licenses/odbl/1-0/",
  "elements": [
    {
      "type": "changeset",
      "id": 147937232,
      "created_at": "2024-02-26T15:30:59Z",
      "closed_at": "2024-02-26T15:30:59Z",
      "open": false,
      "user": "mvexel",
      "uid": 8909,
      "minlat": 40.7402267,
      "minlon": -111.817534,
      "maxlat": 40.740355,
      "maxlon": -111.817531,
      "comments_count": 0,
      "changes_count": 5,
      "tags": {
        "changesets_count": "22734",
        "comment": "Adding markings detail to crosswalk #maproulette mpr.lt/c/41675/t/217416625",
        "created_by": "iD 2.27.3",
        "hashtags": "#maproulette",
        "host": "https://www.openstreetmap.org/edit",
        "imagery_used": "Esri World Imagery",
        "locale": "en-US",
        "resolved:outdated_tags:incomplete_tags": "2"
      }
    }
  ]
}
"""


def test_changeset_from_json():
    changeset = Changeset.from_osm_api_json(valid_changeset_json)

    assert changeset.osm_id == 147937232
    assert changeset.created_at == iso8601.parse_date("2024-02-26T15:30:59Z")
    assert changeset.closed_at == iso8601.parse_date("2024-02-26T15:30:59Z")
    assert not changeset.is_open
    assert changeset.user == "mvexel"
    assert changeset.uid == 8909
    assert changeset.bounds.minlat == 40.7402267
    assert changeset.bounds.minlon == -111.817534
    assert changeset.bounds.maxlat == 40.740355
    assert changeset.bounds.maxlon == -111.817531
    assert changeset.comments_count == 0
    assert changeset.changes_count == 5
    assert len(changeset.tags) == 8
    for tag in changeset.tags:
        assert_type(tag, Tag)
        assert tag.key

    assert_type(changeset.bounds.area, float)
    if changeset.bounds.area is not None:
        assert changeset.bounds.area > 0
