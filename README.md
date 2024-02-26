# osmchangesets

A wrapper around the [native OSM changesets API](https://wiki.openstreetmap.org/wiki/API_v0.6#Changesets_2) that makes working with changeset metadata just a little easier.

## Installing

This project is in early development so it's not on PyPi yet. In the meantime, clone the project and install it locally with `pip` or `poetry`.

## Usage

### Get a changeset

```python
from osmchangesets.osm.api import API
api = API()
changeset = api.get_changeset(147937232)
```

This returns a Changeset instance. The Changeset class is a Python `dataclass`, so you can trivially get a plain Python `dict`:

```python
from dataclasses import asdict
asdict(changeset)
```

There is currently one additional `Changeset` property `area` that returns the area of the changeset's bounding box in square meters. This can come in handy to filter out changesets that cover a huge area, which happens if mappers forget to upload their changes before starting to edit in a completely different area of the world ([example](https://www.openstreetmap.org/changeset/147900904))