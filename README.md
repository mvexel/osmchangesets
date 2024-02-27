# osmchangesets

A wrapper around the [native OSM changesets API](https://wiki.openstreetmap.org/wiki/API_v0.6#Changesets_2) that makes working with changeset metadata just a little easier.

**This is a toy project I started to build experience with some of the newer Python features. Do not use it for anything other than learning purposes**

Some of the topics I'll be studying: 
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/) (Introduced in 3.5)
- [Typing Spec](https://typing.readthedocs.io/en/latest/spec/)
- [PEP 646 – Variadic Generics](https://peps.python.org/pep-0646/) (Introduced in 3.11)
- [PEP 526 – Syntax for Variable Annotations](https://peps.python.org/pep-0526/) (Introduced in 3.7)
- [PEP 557 – Data Classes](https://peps.python.org/pep-0557/) and [reference implementation](https://github.com/ericvsmith/dataclasses) (Introduced in 3.7)
- [PEP 572 – Assignment Expressions](https://peps.python.org/pep-0572/) (Introduced in 3.8)
- [PEP 570 – Python Positional-Only Parameters](https://peps.python.org/pep-0570/) (Introduced in 3.8)
- [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec)
- [Testing](https://realpython.com/python-testing/) in general


## Installing

This project is in early development so it's not on PyPi yet. In the meantime, clone the project and install it locally with `pip` or `poetry`.

## Usage

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

You can also get multiple changesets:

```python
changesets = api.get_changeset(1,2,3,4,5)
```

And you can query

```python
changesets = api.query_changesets(display_name="mvexel", bbox=(3.2, 50.8, 7.2, 53.6))
```

Finally, you can get the latest changesets committed:

```python
changesets = api.latest_changesets()
```

## Limitations

OpenStreetMap's `/changesets` API endpoint is quite limited. It will only return a maximum of 100 changesets, and there is no pagination support. For the `query_changesets` endpoint, this means that you'll get 100 results if the result set is greater than or equal than 100. `latest_changesets` will also only get you 100 changesets. 

There is currently one additional `Changeset` property `area` that returns the area of the changeset's bounding box in square meters. This can come in handy to filter out changesets that cover a huge area, which happens if mappers forget to upload their changes before starting to edit in a completely different area of the world ([example](https://www.openstreetmap.org/changeset/147900904))